## Super Hexagon

Super Hexagon is a AArch64 bios that sets up a full OS stack---with code running at different privilege levels ("rings", in x86 terminology)---as well as making use of ARM's "TrustZone" features (which more-or-less just acts as a couple of additional privilege levels).

The qemu emulator running this bios has been modified with additional model-specific registers that contain a unique flag for each privilege level they are called from. So, there are six flags available in this challenge, and the goal is to gain code execution within each privilege level to read out the flag via the MSRs.

![AArch64 privilege levels](map.png)

#### Exploiting EL0

The EL0 component of Super Hexagon is an AArch64 ELF binary. (For readers following along, it can be extracted from `bios.bin` by finding `\x7FELF` and copying from there to the end of `bios.bin`). It has debug info and symbol names, so you don't really need to reverse the BIOS to figure out what its syscalls do. It's also clear from interacting with the Super Hexagon service that this is the first level of code that you interact with, so knowing exactly how the BIOS loads the ELF binary isn't required at this point.

Looking at the relatively small ELF, there's an obvious `gets()` call that fills a global buffer named "`input`" lying right before a function pointer (`cmd[0]`). This ELF has a `print_flag()` function available (that does the required register reading, and sends the result back over the network), and there's no ASLR or anything. So, to get the flag for EL0, you just:

1. Navigate to the point of the `gets()`
2. Write 256 junk chars to fill up `input`
3. Write the address of `print_flag` (0x400104).
4. End the line, then trigger `cmd[0]` to call `print_flag()`.

Just running `printf '1\n1\n%0256d\x04\x01\x40\x00\x00\x00\x00\n0\n0\n' | nc 127.0.0.1 6666` achieves this.


#### Actually exploiting EL0

Getting the flag for EL0 didn't require real code exec, but to proceed in this challenge does.

TODO


#### Exploiting S-EL0

TODO


#### Exploiting EL1

TODO


#### Exploiting EL2

TODO


#### Exploiting S-EL1 and S-EL3

We ran out of time in the CTF. DragonSector didn't, though, so go see their writeup!
