## oldschool - Pwnable 490 Problem

We are given a program with a trivial format string vulnreability. The
program reads user input into a buffer on the stack, calls printf on it,
then returns.

After the printf, the program will check a stack canary before
returning. We use the format string to leak a libc address and overwrite
the location where the stack canary is located in TLS (this location is brute
forceable, since this is a 32 bit program). The format string also
overwrites `__stack_chk_fail`'s GOT entry with the address a stack lift
gadget to get ROP. The ROP chain calls main again.

Now that we have libc addresses, the exploit sends another format string
to change the stack canary value. This time, the ROP chain calls
`system("/bin/sh");`.
