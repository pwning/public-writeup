## aarm_encrypt - Reversing 191 Problem - Writeup by Robert Xiao (@nneonneo)

Here, we get an AArch64 binary which implements a simple encryption scheme, and the following encrypted text:

```
BLuKJbcqai83,/0h`vvh_monqu"kglgh_soh13dhr/duquu
```

The program takes a numeric key (a "UNIX Timestamp") and a plaintext to encrypt, and outputs encrypted text.

Reversing the program shows that it consists of two parts: an encryption step where it takes the input and encrypts each character using the key, and a postprocessing step where it adds a prefix and suffix.

The prefix and suffix are derived directly from the key by mapping the first and second halves of the numeric key through the table "0123456789" -> "uBldLuKJqJ". Therefore, reversing this obfuscation tells us that the key for the given ciphertext is 1406730800.

The encryption parts look kind of gnarly, however, and reversing them might be annoying. Luckily, they encrypt each character independently (the result is dependent only on the plaintext character, its position within the plaintext and the key). Thus, we can just bruteforce a lookup table by testing each character in each position.

The attached script `brute.py` implements that attack. One subtlety is that some characters have multiple preimages (notably the space character ` ` and the letter `i`), so we disambiguated by guessing.

Once run, we extract the flag: `aarch64... but almost like arm 32bit.`
