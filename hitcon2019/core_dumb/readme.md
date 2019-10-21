# Core Dumb

We only get a core dump. Luckily, we can easily load it and start reversing it.

The binary processes the flag in 5 chunks, where it decrypts a function
using a fixed XOR key then runs the function with the flag chunk.

## Chunk 1 (10 bytes)
This function XORs the flag chunk with a fixed XOR key, then checks it against
a fixed value. We can just XOR the fixed value with the key to recover the
flag chunk.

## Chunk 2 (8 bytes)
This function runs a Feistel-cipher like encryption on the flag chunk, where we
split the chunk into two parts, then use 1 part to encrypt the other and
keep alternating. We can reverse the cipher to recover the flag chunk.

## Chunk 3 (18 bytes)
This function encodes the flag with a custom Base64 alphabet, then checks it
against a known value. We can easily reverse the Base64 to recover the flag
chunk.

## Chunk 4 (12 bytes)
This function encrypts the flag with a RC4-like stream cipher, where we shuffle
a permutation using a key and use the permutation to generate a keystream.

We can run the stream cipher again to generate the keystream and decrypt the
flag chunk.

## Chunk 5 (4 bytes)
This function computes the CRC32 of the flag chunk (without the final bit
inversion) then checks it against a fixed value.
We used a implementation of CRC32 in Z3 to recover the flag chunk.

Solve script in [solve.py](solve.py).
