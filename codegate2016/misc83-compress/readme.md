## Compress – Misc 83

The compress challenge was to decode a flag string that had been encoded by a given python function.

In brief, the encode function combines letter pairs `[a-j]{2}` into one character (while leaving others untouched), and then xors that output with `md5(original_input[:4])`. Both these steps aren't generally invertible.

To solve the challenge, we took advantage of the fact that prefixes of a string will usually encode to prefixes of the encoded string. This was essentially a character-by-character brute-force, with the caveats that:

1. The first 4 characters (that determine the md5 xor mask) must be bruteforced as a unit.
2. Sometimes the next 2 characters must be bruteforced as a unit.
3. Mild human intuition is needed to choose between several candidate flags.

The attached solve script provides the exact details of our solution.
