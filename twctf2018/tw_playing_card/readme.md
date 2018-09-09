## tw playing card - Reversing Challenge - Writeup by Samuel Kim (@ubuntor)

### Description

We get a Nim binary that lets us play a small card game, with randomly generated
cards and opponents.

### Solution

Reversing shows that we have a check function at `0x4017B0` and a decrypt
function at `0x410960`.

The check function looks at our randomly generated cards and checks that they
are the following:
```
2 of Spades
11 of Hearts
6 of Spades
4 of Hearts
9 of Diamonds
```

If the check passes, then the decrypt function is run with the encrypted flag as
the ciphertext and a textual representation of our cards as the key.

We reversed the way the binary randomly generated our cards and found that it
seeded its RNG with `time(0)`. We then brute forced the time to use, but found
that it didn't work.

Further reversing showed that when it loaded its encrypted flag from `0x4113A0`,
it xored each character with `0x20` for some reason we haven't figured out yet.

Running the binary in a debugger and calling the decrypt function with a copy of
the encrypted flag that wasn't xored gave us the flag.
