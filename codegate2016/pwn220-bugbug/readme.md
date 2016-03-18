## bugbug - Pwnable 220 Problem

We are given a lottery game. The game reads the player's name onto the
stack, prints it out again, then generates 6 unique random numbers via
rand (seeded with 4 bytes from /dev/urandom). If the user guesses these
numbers correctly, the program printfs the player's name, then calls
exit.

The name is not null terminated, so by giving a name of 64 As,
additional bytes will be printed past the end of the name. The srand
seed happens to be here, so when the seed does not contain any null
bytes, we can leak all of it out.

Using the seed, we compute the correct lottery number locally, which
gives us a standard printf vulnerability. The exploit leaks an address
in `__libc_start_main`, then overwrite exit's GOT entry with the address
of main. The exploit then cheats/wins the lotto again, this time
overwiting exit's GOT entry with the address of a stack lifting gadget
to get ROP. Then we call `system("/bin/sh");`.
