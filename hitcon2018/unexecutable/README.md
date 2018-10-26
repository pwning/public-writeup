## unexecutable

The server asks us to send it an ELF file, but it carefully checks the ELF file
to make sure none of the segments are executable. This should prevent us from
running our own code, so instead we need to chain together gadgets from the
provided libraries, e.g. libc.so.6.

Due to ASLR, we do not know the base address of libc.so.6 plus we want to be
able to run multiple gadgets, so something like modifying the ELF entry point
is not useful. Instead, we can use libc's support for init functions combined
with the dynamic linker to execute our gadgets.

Concretely, we can compile a simple C program like:

```
#include <stdlib.h>

static void (*const preinit_array []) () __attribute__ ((used, section (".preinit_array"), aligned (sizeof (void *)))) = {
    exit, exit, exit, exit,
    exit, exit, exit, exit,
    exit, exit, exit, exit,
    exit, exit, exit, exit,
    exit, exit, exit, exit,
    exit, exit, exit, exit,
    exit, exit, exit, exit,
    exit, exit, exit, exit,
    exit, exit, exit, exit,
    exit, exit, exit, exit,
};

int main()
{
    return 0;
}
```

This will produce an ELF file with the libc.so.6 _exit_ symbol called many
times in a row by libc's initialization code.

Next, we use lief to modify the ELF file so that the segments are
non-executable and to offset the resolved symbol by adding an _addend_ to the
relocations. This _addend_ turns the array of _exit_ pointers into the
chain of gadgets. See [gen_exploit.py](gen_exploit.py).

Aside: lief has a bug that causes it to produce an ELF file with the wrong
number of segments. This is trivially fixed manually with a hex editor.

When constructing the gadget chain, we take advantage of the registers that are
used when iterating through the initialization array. Specifically, we assume
that the normal arguments to the functions are: _argc_, _argv_, and _envp_.

The chain we ended up constructing is:

 - _dup_ - reopens STDIN by duping ```fd = argc = 1```
 - ```add ebp, eax``` - _ebp_ contains the saved _argc_, _eax_ contains pointer to ```preinit_array```, the effect is that _ebp_ has ```READ_IMPLIES_EXEC``` flag set
 - _personality_ - sets personality with the modified _argc_, e.g. ```READ_IMPLIES_EXEC```, so all new allocations will be executable
 - ```add ebp, eax; add ebp, eax; ...``` - increment _argc_ by a large amount
 - _brk_ - allocate modified _argc_ (e.g. a large value) of heap memory, it will be RWX
 - gets - read from STDIN into _argc_, which likely points into the heap memory we just allocated
 - ```jmp rdi``` - calls _argc_ which points to the data we just read in

At this point, we have almost arbitrary shellcode running. Since the server is
running inside of a jail, we cannot use the shell, so our shellcode must be
list the directory and read files using system calls or functions within
libc.so.6 (e.g. listdir and readdir).

The name of the flag file was: "flag-e596f6971e03815673c4c28574fbebe2".

The flag was: "hitcon{relocation-is-an-elf-in-ELF!}".
