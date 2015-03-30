## weak_enc - Crypto 200 Problem - Writeup by Robert Xiao (@nneonneo)

This is a bit of a weird crypto implementation. First they take your input, prepend a "salt", and LZW-compress the whole thing (which immediately suggests some kind of compression length attack). They then use the salt to construct a "one-time" key which is xored against the LZW-compressed input to produce the ciphertext.

Since the ciphertext length is exactly the length of the LZW-compressed input, the goal is to leak the salt (or at least enough information about it) to decrypt the provided ciphertext.

The salt is all lowercase, so we can use any uppercase letter to supply "uncompressible" input (input that cannot appear in the salt). Encrypting an empty string shows that the LZW output for the salt is 11 entries long.

We can figure out how many unique letters `n` there are in the salt by encrypting the message `Xc` for each letter `c`. This produces an LZW string ending in the code for `X` and the code for `c`. If `c` is in the salt, the code will be one of the first `n` values; otherwise, the code will be `n+1` (since `X` is `n`). Since the XOR key is fixed (since the salt doesn't change), the result is that the last ciphertext byte will either be the same as the one from encrypting e.g. `XY` (if `c` is not in the salt) or different. We collect all the `c`s appearing in the salt (which happens to be the four letters `niko` for the server's salt), compute `n`, and then actually calculate the xor key at that position (from knowing `n+1`). So this gives us the start of the dictionary (and the string):

    n=0 i=1 k=2 o=3

Knowing `n` lets us recover the XOR key for any message byte: we simply encrypt `ABCDEFGHIJKLMNOPQRSTUVWXYZ`, which must LZW to the sequence `n, n+1, n+2, n+3, ...`. We can thus get the plaintext bytes for the ciphertext:

    [11, 10, 13, 4]

So we just need to know the corresponding entries in the LZW dictionary. No problem: we can bruteforce it since we can basically decrypt any message to get the LZW dictionary entries. We simply encrypt every `Xs` for each string `s` composed of at most 4 letters from `niko`. If the result is 13 bytes (indicating that `s` compressed to a single number) we can recover the corresponding dictionary entry (after correcting for the one-byte shift from the `X`).

From this we determine that the entries are

    {0: 'n', 1: 'i', 2: 'k', 3: 'o', 4: 'ni', 5: 'ik', 6: 'ko', 7: 'on', 8: 'nik', 9: 'kon', 10: 'nin', 11: 'niko', 12: 'oni', 13: 'iko'}

and thus our desired decrypted string (flag) is

    nikoninikoni

