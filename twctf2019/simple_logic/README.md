# Simple Logic

We have a cipher that repeatedly adds and xors the plaintext with a key.

Note that carry bits from the addition only propagate towards the MSB, so we can
just bruteforce key candidates starting from the LSB, and grow our candidates
bit by bit.

Solution script in [solve.py](solve.py). Run with `pypy3` for speed.
