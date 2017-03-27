## EasiestPrintf - Pwnable Challenge

We are given a 32-bit binary with NX/full RELRO that:

1) Leaks 4 bytes of an user-provided address
2) Reads and calls `printf` on 159 bytes read from the user (on the
   stack).
3) calls `exit(0)`

We exploited this by overwriting:
1) Use the 4 byte leak to find the libc base address
2) Write "sh\0" to stdout
3) Write the address of `system` to a writable address
4) Overwrite the address of `stdout`'s function pointer table so that
  `system` appears in the right place for outputting a character.

In the course of `printf`, the implementation calls a function pointer
via `stdout`'s function pointer table to output a character. At this
point, it calls `system("sh")`.
