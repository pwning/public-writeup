# EscapeMe

## Overview

This is a 3 stage problem with three flags.

We are given three x86-64 binaries:
 - kvm.elf: A Linux program which starts a VM using the KVM API.
 - kernel.bin: Code for the VM's kernel. Runs in the VM's ring 0.
 - memo-static.elf: Statically linked ELF implementing a "secret memo
   service"

Each flag requires getting code execution in one of these binaries.

We are also given a launcher script for the binaries, pow.py. This
requests a hashcash proof-of-work, then starts the problem, allowing the
user to specify additional "modules" (filenames) that may be loaded by
kvm.elf.

## High level reversing

kvm.elf runs the VM with `KVM_GUESTDBG_SINGLESTEP` and intercepts
`syscall` and `vmmcall` instructions. `vmmcall` instructions
(hypercalls) are handled by code in kvm.elf, and `syscall` instructions
are handled by running code in kernel.bin in ring 0 inside the VM.

kvm.elf implements the following hypercalls:
 - `read(vaddr, size, require_user_addr)`: Read from stdin.
 - `write(vaddr, size, require_user_addr)`: Write to stdout.
 - `palloc(paddr, size)`: Allocate physical pages.
 - `pfree(paddr)`: Free physical pages.
 - `load_file(fileno, paddr, off, size)`: Load a file (module) into a
   physical address.

At a high level, kvm.elf:

1. Opens all of the module files.
2. Sets up a KVM VM with 1 vCPU and 4 MiB of memory.
3. Loads kernel.bin at physical address 0x0.
4. Enables seccomp with an odd policy (see below).
5. Enter long mode, and start running the VM, handling `syscall` and
   `vmmcall` instructions.

When kernel.bin starts running, it does the following:

1. Allocate 4 KiB of physical pages for kernel stack.
2. Set up paging. Maps:
   - 4 KiB of kernel code at 0x8000000000, 
   - 4 KiB of kernel BSS at 0x8000200000, 
   - 2 MiB of RW direct physical mapping at 0x8040000000. It appears to be
     an unintentional bug that this does not direct map the entire 4 MiB of
     physical memory. Looking at the [challenge author's code](https://github.com/shift-crops/EscapeMe/blob/master/kernel/memory/sysmem.c#L34),
     it looks like it mistakenly expected the ternary operator to bind
     more tightly than addition.
   - 4 KiB of kernel stack at 0xffffffc000.
3. Set up the GDT.
4. Set up STAR/LSTAR MSRs (syscall entry point).
5. Map 4 KiB of user stack at 0x7fffffc000.
6. Load the `memo-static.elf` ELF (using the `load_file` hypercall).
7. "Return" to userspace using `iret`.

None of the kernel or userspace mappings set the execute disable bit.

kernel.bin implements the following syscalls:
 - `read`
 - `write`
 - `mmap`
 - `mprotect`
 - `munmap`
 - `brk`
 - `exit`
 - `flag1`

Apart from `flag1`, the prototypes and syscall numbers match those of
x86-64 Linux, though they implement a subset of the functionality.

The `flag1` system call maps a page into the user address space
containing the first flag.

Now, on to the individual binaries.

## memo-static.elf

This binary implements a "secret memo service." For our convenience, the
author made the binary's syscalls compatible with Linux. This made it
possible to debug and exploit this as a standalone Linux binary, keeping
in mind that we can assume no ASLR or NX.

### Reversing

This is a fairly standard menu-based service. The binary supports the
following functions:
 - Allocate a memo (may only have up to 16)
 - Edit a memo (may only do so once per memo)
 - Delete a memo

There is no way to print a memo, but this isn't a problem, since there
is no ASLR.

A memo is represented by the following structure:

```c
struct memo {
  char *buf;  // heap-allocated buffer of size 0x28
  int edited;
};
```

At startup, the binary mmaps a page for the array of memos and stores it
in a global variable. The memo buffers are heap-allocated, using what
appears to be a modified ptmalloc. The biggest difference is the lack of
fastbins. Otherwise, the `malloc_chunk` structure and unlink checks
appear identical to ptmalloc.

### The Bug

The allocation function does:

```c
memo->buf = calloc(0x28, 1);
memo->edited = 0;
...
read(0, memo->buf, 0x28);
```

This does not guarantee null termination. The edit function does:

```c
read(0, memo[i].buf, strlen(memo[i].buf));
```

This allows us to overwrite the size field of the malloc chunk after the
memo buffer.

### Exploitation

Since we know the address of the memo array (which contains pointers to
the heap-alocated buffers), we can bypass the free list unlink checks
and overwrite a memo's buffer pointer with an address inside the memo
array. This will give us arbitrary write.

The goal is to free a fake malloc block that we control. To achieve
this, we setup the following allocations:


```
+-------------------------------+
| head | target | fake1 | fake2 |
+-------------------------------+
```

`fake1` and `fake2` contain a fake malloc chunk which when unlinked,
will overwrite `fake1`'s entry in the memo array with a pointer inside
of the memo array.

Next, we edit `head` to overwrite `target`'s size such that the next
chunk of target appears to be the fake chunk inside of `fake1` and
`fake2`.

Finally, we free `target`. The fake next chunk appears to be free, so
the allocator consolidates it with `target`. In doing so, it unlinks the
fake chunk and  overwrites `fake1`'s memo's buffer pointer to point
inside the memo array.

Since the buffer in `target`'s memo slot how now been zeroed out, we
allocate a memo containing shellcode. This fills `target`'s slot in the
memos array.

At this point, by editing `fake1`, we can modify the buffer address of
`target`'s memo slot. However, due to the `strlen` call, we can only
overwrite the buffer address with a 3 byte address (since the heap uses
`brk`). Since the program is statically linked, there aren't any useful
function pointers (like GOT entries) in that address range. Instead, we
target the stack (which has a 5 byte long address).

To gain the ability to write to these addresses, we start by overwriting
the global variable (in BSS) that stores the pointer to the array of
memos. First we allocate a fake memos array that will allow us to write
to the stack. Then we edit `fake1` to set the buffer address of
`target`'s slot to the address of the memo array global variable. We add
one to this address because the value of the global variable starts with
a null byte, and edit uses strlen to decide how much to read.

Finally, we overwrite the global variable to point before our fake memos
array. This gives us the ability to write to the stack. We write a
pointer to shellcode over a return address to gain code execution.

To get the first flag, the shellcode invokes the `flag1` syscall. This
maps a page containing the first flag, but without the User/Supervisor
flag set on the page table entry. To render the flag readable, we call
`mprotect`, which allows setting U/S flag from 0 to 1 on PTEs
(unfortunately, it does properly check the U/S flag on PML4/PDPT/PDT
entries).

Flag: `TWCTF{fr33ly_3x3cu73_4ny_5y573m_c4ll}`

## kernel.bin

The kernel binary has a relatively small attack surface - just the 8
syscalls listed above.

### Reversing

Reversing the kernel binary, we found that the
`mmap`/`munmap`/`mprotect` system calls correctly refuse to operate on
PML4/PDPT/PDT entries without the U/S flag set.

Tracing the `read` and `write` system calls through into hypercalls in
`kvm.elf`, we found that those calls also correctly refuse to access
kernel memory when `require_user_addr` is set (which they are in the
syscall handlers).

The main interesting (and seemingly unnecessary) aspect of this program
is that physical page allocation is handled by `kvm.elf` rather than the
kernel itself.

### The Bug

Finding the bug actually involved reversing `kvm.elf` as well. The
`munmap` syscall releases pages to the physical page allocator by
calling the `pfree` hypercall: `pfree(paddr, 0x1000)`.

However, looking at the implementation of `pfree` in `kvm.elf`, we see
that it ignores the size parameter:

```c
  case HYPERCALL_PFREE:
    res = pfree(regs.rbx);
```

it turns out that `kvm.elf` uses yet another modified `ptmalloc` for its
physical page allocator, and the sizes of allocations are tracked in
metadata associated with the allocation. This means that
`pfree(paddr, 0x1000)` can actually free more physical pages than expected.

### Exploitation

To exploit this, we do the following:

```c
// Allocates physical pages using palloc(0x2000)
mmap(0xd0000000, 0x2000, ...);

// Frees the entire 0x2000 allocation, but leaves the PTE for 0xd0001000
// in place, pointing to a freed physical page.
munmap(0xd0000000, 0x1000);

// 0xe0000000 is chosen to require a new page table (but use the same
// PDPT and PDT as 0xd0000000).
//
// Allocates 0x1000 out of the just-freed freed 0x2000 allocation for
// the requested mapping. Also allocates a new page table for 0xe0000000.
// That page table is allocated at the freed physical page that backs
// 0xd0001000.
mmap(0xe0000000, 0x1000, ...);
```

We can then control a page table by writing to 0xd0001000.

Our exploit writes shellcode over some kernel code that is run on exit,
then triggers it.

To obtain the 2nd flag, we pass `flag2.txt` to the launcher script and
use the `load_file` hypercall to read the contents of the file into
memory.

Flag: `TWCTF{ABI_1nc0n51573ncy_l34d5_70_5y573m_d357ruc710n}`

## kvm.elf

### Reversing

We've already looked at the physical page allocation hypercalls. The
only remaining interesting ones are the `read` and `write`.

These hypercalls take a virtual address and translate it to a physical
address by walking the VM's page tables (obtained by reading `cr3`). The
physical address is used as an index into the VM's physical memory
(which is an mmapped region in kvm.elf's address space).

### The Bug

The page table walking function only validates the returned physical
address in the code path that handles page table entries. However, there
is a second code path for handling page directory table entries that map
a 4 MiB page (by setting the Page Size bit). The physical address from
such entries are returned with no validation.

This gives out of bounds read/write of the VM's physical memory.

### Exploitation

The exploit sets up a little RPC handler so that the relative read/write
primitive can be driven by Python code rather than assembly.

The physical memory mapping is immediately before libc. Using the fact
that `main_arena.next` points to `&main_arena` in libc, we turn the
relative read/write into an absolute read/write.

Using the arbitrary read/write, we read a stack address via the
`environ` variable in libc, search for the program's stack, then write a
ROP chain to obtain code execution in `kvm.elf`.

Unfortunately, we cannot just spawn a shell due to the odd seccomp
policy that is enabled on the process (disassembled using
`scmp_bpf_disasm` from [libseccomp](https://github.com/seccomp/libseccomp/)):

```
 line  OP   JT   JF   K
=================================
 0000: 0x20 0x00 0x00 0x00000004   ld  $data[4]
 0001: 0x15 0x01 0x00 0xc000003e   jeq 3221225534 true:0003 false:0002 # 0xc000003e
 0002: 0x06 0x00 0x00 0x00000000   ret KILL
 0003: 0x20 0x00 0x00 0x00000000   ld  $data[0]
 0004: 0x35 0x00 0x01 0x40000000   jge 1073741824 true:0005 false:0006 # 0x40000000
 0005: 0x06 0x00 0x00 0x00000000   ret KILL
 0006: 0x15 0x00 0x01 0x00000000   jeq 0    true:0007 false:0008 # read
 0007: 0x06 0x00 0x00 0x7fff0000   ret ALLOW
 0008: 0x15 0x00 0x01 0x00000001   jeq 1    true:0009 false:0010 # write
 0009: 0x06 0x00 0x00 0x7fff0000   ret ALLOW
 0010: 0x15 0x00 0x01 0x00000003   jeq 3    true:0011 false:0012 # close
 0011: 0x06 0x00 0x00 0x7fff0000   ret ALLOW
 0012: 0x15 0x00 0x01 0x00000008   jeq 8    true:0013 false:0014 # lseek
 0013: 0x06 0x00 0x00 0x7fff0000   ret ALLOW
 0014: 0x15 0x00 0x01 0x0000000c   jeq 12   true:0015 false:0016 # brk
 0015: 0x06 0x00 0x00 0x7fff0000   ret ALLOW
 0016: 0x15 0x00 0x01 0x000000e7   jeq 231  true:0017 false:0018 # exit_group
 0017: 0x06 0x00 0x00 0x7fff0000   ret ALLOW
 0018: 0x15 0x00 0x01 0x00000010   jeq 16   true:0019 false:0020 # ioctl
 0019: 0x20 0x00 0x00 0x00000018   ld  $data[24] # arg[1]
 0020: 0x15 0x05 0x00 0x0000ae01   jeq 44545 true:0026 false:0021 # 0xae01 (KVM_CREATE_VM)
 0021: 0x15 0x04 0x00 0x0000ae41   jeq 44609 true:0026 false:0022 # 0xae41 (KVM_CREATE_VCPU)
 0022: 0x20 0x00 0x00 0x00000010   ld  $data[16] # arg[0]
 0023: 0x54 0x00 0x00 0x000000ff   and 0x000000ff
 0024: 0x35 0x01 0x00 0x00000009   jge 9    true:0026 false:0025 # 3 + 3 + argc - 1
 0025: 0x06 0x00 0x00 0x7fff0000   ret ALLOW
 0026: 0x06 0x00 0x00 0x00000000   ret KILL
```

The seccomp policy explicitly allows a particular set of syscalls, and
for some reason, only allows other syscalls if `arg[0] & 0xff < 9`.
During the CTF, we used `getdents64` to determine the filename of the
third flag, then repeated the flag2 exploit with that filename.

We later realized that the seccomp filter could be bypassed almost
entirely by passing 0x100 nonexistent files as modules.

Flag: `TWCTF{Or1g1n4l_Hyp3rc4ll_15_4_h07b3d_0f_bug5}`

See [exploit.py](https://github.com/pwning/public-writeup/blob/master/twctf2018/escapeme/exploit.py) for our full exploit.
