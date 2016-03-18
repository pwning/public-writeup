## Fl0ppy - Pwnable 315 Problem

This is a x86 PIE binary with an array of two floppy structures that can be
written, read, and modified. The structures are approximately:
```
struct floppy {
    int is_usable;
    char *data_buf;
    char desc[10];
    int data_len;
};
```

In order to make a floppy usable, you issue a write command to that floppy.
Each floppy can only be written to once, but you can use the modify command
to change the description or the data.

There is a bug when modifying the description. It uses strncpy but it uses
the length of the attacker-controlled string instead of the buffer length.
This means that we can overflow the description buffer. While there is nothing
intresting after the description buffer in the structure, if we modify one of 
the floppy description we can overwrite the data_buf of the other floppy. Or
we can overwrite the pointer to the current floppy, which is next on the stack.

Basic overview of exploit:
 - Make floppy 1 usable by writing to it once
 - Modify floppy 1 description to overwrite the least significant byte of the
   current floppy pointer with a NUL
 - Read the floppy 1 description which is now pointing to some random stack
   data
   - This stack data contains a stack pointer which we will use next
   - We subtract 4 so that the pointer points to main return address
 - Make floppy 2 usable by writing to it once
 - Modify floppy 2 description to overwrite the *data_buf* pointer of floppy 1
   with the stack address we leaked
 - Read the data of floppy 1 which is the return address of main, which points
   into **libc_start_main**.
 - Calculate the address of **system** using this pointer
 - Modify the data of floppy 1 so that the return address of **main** is now
   **system**, followed by */bin/sh* as the first argument
 - Quit, so main returns and we get a shell

The exploit sometimes will fail if a pointer randomly contains a NUL byte. So
we may have to run it a couple of times for it to succeed.

Complete exploit is in *exploit.py*.
