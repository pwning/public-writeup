# Abyss

## Overview

This is a 3 stage problem with three flags.

We are given several x86-64 binaries:
 - hypervisor.elf: A Linux program which starts a VM using the KVM API.
 - kernel.bin: Code for the VM's kernel. Runs in the VM's ring 0.
 - user.elf: Dynamically linked Linux ELF implementing a simple stack based VM (no RELRO).
 - ld.so.2, libc.so.6: ld and libc from Ubuntu 18.04.

Each flag requires getting code execution in one of these binaries.

## High level reversing

hypervisor.elf runs the VM and handles hypercalls via I/O ports.

hypervisor.elf implements the following hypercalls:
 - `read(fd, paddr, size)`
 - `write(fd, paddr, size)`
 - `lseek(fd, offset, whence)`
 - `open(filename)` (only allows whitelisted files, including the first flag)
 - `close(fd)`
 - `fstat(fd, paddr)`
 - `exit(status)`
 - `access(status, mode)`
 - `ioctl(fd, req, paddr)`
 - `panic(str)`

At a high level, hypervisor.elf:

1. Sets up a KVM VM with 1 vCPU and 32 MiB of memory.
1. Copies kernel.bin at physical address 0x0
1. Sets up paging, maps virtual addr 0x0 (writable) to the kernel code
   at physical address 0x0.
1. Start running the VM, handling hypercalls as described above.

When kernel.bin starts running

1. Sets up an mapping of all physical memory at 0x8000000000.
1. Set up STAR/LSTAR MSRs (syscall entry point).
1. Map 4 KiB of user stack at 0x7fffffc000.
1, Copies arguments, loads ld.so.2.
1. "Return" to userspace using `sysret`.

The kernel and userspace mappings generally do not set the execute disable bit.

kernel.bin implements the following syscalls:
 - `read`
 - `write`
 - `open`
 - `close`
 - `fstat`
 - `mmap`
 - `mprotect`
 - `munmap`
 - `brk`
 - `writev`
 - `access`
 - `exit`
 - `prctl`
 - `fadvise`
 - `exit_group`
 - `openat`

The prototypes and syscall numbers match those of x86-64 Linux, though
they implement a subset of the functionality - basically the minimum
needed to load and execute user.elf.

Now, on to the individual binaries.

## user.elf

This binary implements a simple stack based VM. It reads a 1024 byte
program and executes it.

The layout of the VM state is:

```c
struct vm {
  int stack_ptr;
  int stack[1024];
  int program[1024];
};
```

Most operations check that the stack pointer is nonzero (the stack grows
up), but do not check whether the stack pointer is negative. There is
also a buggy swap operation which will swap `stack[stack_ptr - 1]`
and `stack[stack_ptr - 2]` without checking that these are in bounds.

Storing a constant at stack slot 0 and executing a swap instruction
places the constant into the stack pointer. To gain code execution, we
point the stack at the GOT entry for write and use VM operations to
point that entry to shellcode located after our program. We then execute
a write opcode, which calls this GOT entry.

We can send shellcode to open/read/print the flag.

Flag: `hitcon{Go_ahead,_traveler,_and_get_ready_for_deeper_fear.}`

## kernel.bin

The vulnerability is in the write syscall:

```c
int sys_write(int fd, const void *buf, size_t count) {
  ...
  void* heap_buf = kmalloc(count, 0);
  qmemcpy(pointer, buf, count);
  ...
}
```

For no apparent reason, the this call copies the data into a heap
buffer. The return value of `kmalloc` is not checked. If the allocator
runs out of memory, it returns NULL and the `memcpy` writes to the
kernel code page at 0x0.

To exploit this, exhaust memory by allocating a buffer of size 0x1000000
with mmap. We fill that buffer with shellcode and a trampoline to jump
to said shellcode. We then call the `write` syscall on that buffer,
which copies it over the kernel code at 0x0.

The shellcode can now directly use the `open` hypercall without being
subject to the file whitelist in the `open` syscall. We obtain the flag
by opening/reading/writing `flag2`.

Flag: `hitcon{take_out_all_memory,_take_away_your_soul}`

## hypervisor.elf

The third flag's filename is unknown, so we cannot just use our
arbitrary file read to read it.

We can however read `/proc/self/maps` to defeat ASLR in hypervisor.elf.

The vulnerability in hypervisor.elf is that it exposes an ioctl
hypercall for no apparent reason. Unlike the filesystem hypercalls, the
ioctl hypercall directly calls `ioctl` on the provided file descriptor
number without passing it through a translation table.

By using the `KVM_SET_USER_MEMORY_REGION` ioctl on the KVM VM fd, we can
expose arbitrary addresses from the hypervisor process into the VM's
physical memory. This gives us arbitrary read/write (after writing a
little code to map that physical address).

We use the `/proc/self/maps` leak to find the libc and the stack, read
it to locate the the current stack location, and then overwrite to ROP
to `system("/bin/sh")`.

Flag: `hitcon{first-grade-artifact:KVM-exploitor}`

See [exploit.py](https://github.com/pwning/public-writeup/blob/master/hitcon2018/abyss/exploit.py) for our full exploit.
