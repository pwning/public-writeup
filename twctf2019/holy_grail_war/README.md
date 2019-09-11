# Holy Grail War

This is a binary compiled with Substrate VM. We notice that the binary encrypts
input in blocks of 8 bytes, and each block doesn't affect any other block.

Reversing a bit, we see that the main encryption loop starts at `0x402EBD`,
where it uses a ARX Feistel cipher with keys/constants that depend only on the
index of the block to encrypt.

We dumped those keys with gdb for each block, and wrote a script to decrypt each
block. Solve script in [solve.py](solve.py).
