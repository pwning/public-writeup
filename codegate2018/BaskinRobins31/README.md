## BaskinRobins31 - Pwnable Challenge

This service implements some sort of guessing game. We did not reverse
further than the first read call because it is a trivial buffer
overflow.

The exploit ROPs to `puts` to leak the address of `strtoul`. It then
returns to `main`. The base address of libc is computed based on the
address of `strtoul` (annoying, the libc binary was not provided - it
turned out to be the latest Xenial libc). The vulnerability is then
retriggered to call `system("/bin/sh");`.
