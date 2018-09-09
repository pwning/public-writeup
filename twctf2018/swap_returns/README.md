# Swap Returns — Pwnable Challenge — Writeup by Corwin de Boor (@strikeskids)

## Description

In a choice-action style problem, you can set up two addresses or swap the memory values between
addresses you've set up.

## Solution

First, we need to get a leak. Swapping `atoi` and `printf` in the `.got` allows us to print out
a stack address by sending `%p` as the number. We can't just do a `printf` exploit because we only
have 2 characters (smart thinking).

By setting the second address to the location of the first address in memory, we are able to write
an arbitrary character into `.bss`. Namely

	addr1 = &bss[ch];
	addr2 = &addr1;

writes `ch` into `bss + ch`. We grab the libc address of `printf` from the `.got`, overwrite the low
three bytes with a one-gadget, and put it back into the `.got`. Note that this requires a 12-bit brute
force for the high three nibbles. We moved on from that problem while the brute-force ran, and eventually
got the flag.

Solution script in [exploit.py].