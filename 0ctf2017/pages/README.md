## EasiestPrintf - Pwnable Challenge

We are given a 64-bit binary that:

1) Generates 64 random bits
2) Forks. In the child:
   For i in [0, 64): mmaps 0x200000000 + 0x2000 * i + 0x1000 * `random_bits[i]`
   Reads shellcode from the user
   Enable seccomp, allowing only exit
   Runs shellcode
3) In the parent: Ptraces the child. Upon child exit, if it exited via a
   SIGTRAP, reads a specific 64 byte region of memory from the child. If
   it matches `random_bits`, output the flag.

Basically, the goal is determine whether or not a page is mapped without
using any syscalls.

To do this, we use the `prefetcht2` timing attack described in [this
paper](https://gruss.cc/files/prefetch.pdf). By timing the `prefetcht2`
instruction (wrapped in the appropriate `mfence` and `cpuid`
instructions to serialize the execution of the timing and prefetch
instruction), we can distinguish mapped and unmapped addresses.

Our implementation, which we compiled into shellcode can be seen in
`code.c`.

```
flag{rand0mPage_randomFl4g}
```
