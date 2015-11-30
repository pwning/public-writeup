## calcpop - Exploitation 80 Problem - Writeup by Tim Becker (@tjbecker)

### Description

`calcpop` is a simple calculator application with a stack buffer overflow bug.

```
calcpop: ELF 32-bit LSB  executable, Intel 80386, version 1 (SYSV), dynamically linked (uses shared libs), for GNU/Linux 2.6.24, BuildID[sha1]=3b0773c4d23785ef3daae0b3a3505d8fa41403af, not stripped

CANARY    : disabled
FORTIFY   : disabled
NX        : disabled
PIE       : disabled
RELRO     : Partial
```

### Solution

Since no protections are enabled, we can simply overwrite the return address of `main`
with the address of our buffer, which is conveniently printed to us if our input does
not contain a space.

First we obtain this stack address, then we overflow and overwrite the return address with our buffer
address plus 8. This is to leave room for us to enter `exit` on the next iteration to trigger the return
from `main`.

See `solve.py` for the finished exploit.
