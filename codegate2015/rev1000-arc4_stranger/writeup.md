# arc4_stranger (1000pts)

This reversing challenge was a "DesignWare ARC" ELF binary, which implements a relatively
small and straightforward custom VM interpreter.

My first clue to what was happening in this binary was a giant string of UTF-8 "HEXAGRAM" characters,
at 0x3D8C. Since there are 64 UTF-8 hexagram characters and this was a CTF, naturally I tried interpreting
them as base64. It's rather suggestive looking, including a "WIN" string. Also noteworthy is the byte
distribution: it mostly uses the same low bytes, but includes a variety off one-off higher bytes.
In a CTF reversing challenge, these are both hallmarks of bytecode for a custom VM.

Obviously, you need to reverse the VM implementation before you can start reversing the VM bytecode.
Unfortunately, the VM implementation is in ARC, which is apparently the most well supported GNU-architecture
that no one has ever heard of. There's no qemu support or freely available simulator I could find for ARC,
so I settled for [http://me.bios.io/images/c/c6/ARC4._Programmers_reference.pdf](http://me.bios.io/images/c/c6/ARC4._Programmers_reference.pdf).
Some ARC peculiarities include hardware-assisted loops and configurable branch delay slots.

ARC is mostly supported by IDA. The main thing IDA doesn't get is that ARC, a 4-byte fixed-width instruction
architecture, uses function pointers in a shifted `fp >> 2` format. Finding the main processing loop can be
done by x-refing the hexagram/vm-bytecode string, and then noticing that one of the results, `sub_C88`, is a
direct child of `start` (some of the extraneous results look like dead code left over from an inlining optimization).

In `sub_C88`, the code from 0x0CF4-0x0DB0 and 0x0EE0-0x0F84 is a loop over the hexagram UTF-8 buffer,
decoding it in a base64-style fashion. Note how `r20` iterates over the UTF-8 buffer, and how each
character is assigned its value by iterating through a list of strings (`r17` iterating over the `chr**`
at 0x6DE8), calling `memcmp()` (`sub_207C`) to find its index in the list, which winds up in `r16`. As the
iteration proceeds, bits from that index are aggregated into `r15`, and completed bytes are stored to `[r5]`
(which is an offset into a .bss array at 0x000477D8).

The other part of `sub_C88`, 0x0DB4-0x0EDC, is the VM dispatch loop. It reads 4 bytes of the decoded input,
as an instruction & arguments. Instructions are implemented as a function lookup from the table of function
pointers at 0x6CE8.

At this point, I implemented in python what I'd seen (see the attached file), and implemented the first couple
functions from 0x6CE8. Most are simple: addition, xor, some conditional-jump instructions. The VM bytecode
doesn't use all of them, so I left most of these as NYI stubs and just implemented them on-demand. The only
hard-to-reverse functions that needed implementing were IO functions, but I didn't actually need to reverse those:
You could guess that they were IO from the fact that 1. VMs need some sort of IO and 2. they call big subroutines
that look like they're from a library. The IO output function is an "output ASCII character Y at column X",
which was fairly obvious from just printing out the args it gets called with. The VM program outputs junk
characters and replaces them, which is a CTF-style obfuscation.

There seems to be some sort of IO input function, and from printing out instructions it's clear that your input
is getting `strcmp()`ed. But, it looks like your input gets compared to a string that I was already printing as
VM output, at which point I realized that I already had the flag -_-

I never did see the VM use that "WIN!!!" string that I saw at the beginning of the problem, and my script just
loops printing the flag over and over, so clearly I have something wrong... meh. Doesn't matter; captured flag.
