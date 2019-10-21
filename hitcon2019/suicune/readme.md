## suicune - reversing challenge - 15 solves (305 points)

`suicune` is a reversing problem written in [Crystal](https://crystal-lang.org/). It implements a simple encryption program which takes two arguments - a string and a numeric key - and outputs a hex-encoded encryption of that string. We're also given an `output` file which presumably contains the encryption of the flag under some key.

If you run `suicune` with a moderately long string, it takes quite a long time to produce an output - 11 characters takes 15 seconds, and 12 characters takes over 3 minutes. Clearly, it'll be impractical to run it on a 49-character string (the length of the encrypted output). So, we've gotta reverse it.

Crystal programs look a lot like Ruby, but are compiled down to native code. The entire logic is in `crystal_main` and the program is not stripped, so there are _lots_ of symbols. The symbols themselves are pretty verbose, encoding the type of each argument *and* the return type, making reversing easier. However, loads of functions are inlined, so that `crystal_main` ends up being several thousand lines of decompiled C. Reversing it was thus still pretty painful.

Using Crystal's source code, we were able to match up bits in `crystal_main` with the random number generator (PCG32) and `shuffle!`. This told us that, first, the program used the low 16 bits of the key to seed an RNG, then shuffled an array containing the numbers 0 to 255 using the RNG. It took the first `n` elements of the array (where `n` was the length of the key), and apparently sorted that sub-array using a very complex and slow procedure. It finally `xor`ed the input buffer with this array, reversed the result, and repeated the entire procedure (except RNG seeding) 15 more times.

We reimplemented it in Python and simply replaced the slow sort with a standard one, and found it mirrored the implementation perfectly for short strings. But, it failed to find the flag when brute-forcing all 65536 possible keys. Going back to the complex sort, I had guessed it was a simple "bogo-sort" implementation (try every permutation and see if it's sorted). But, on closer examination, I realized it only checked permutations up to a certain (random) limit. Thus, instead of sorting the list I wrote some code to convert a permutation into an index and vice-versa, and thereby successfully got the flag:

`hitcon{nth_perm_Ruby_for_writing_X_C_for_running}`

See [`solve.py`](solve.py) for the final solver.
