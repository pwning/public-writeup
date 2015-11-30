## randbox - Cryptography 120 Problem

### Description

`randbox` has 10 levels of random simple encryption mechanisms. At the start
of each level, we are presented with ciphertext for some random plaintext in
hex. We then make plaintext queries and receive responses until we run out of
attempts, or our query matches the original plaintext.

Apparently by accident, this challenge has a fixed ordering of challenges,
it should not be too hard to modify a script to detect the encryption
mechanism and adjust accordingly.

### Solution

We wrote a Python script for solving this task, it can be found in this
folder under `solve.py`. This script works for the original ordering of
tasks, and can fail with 1/2 probability, I didn't bother to fix this 
during the competition.
