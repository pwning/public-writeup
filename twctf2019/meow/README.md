# meow

This is NekoVM bytecode. We disassembled and reversed enough to see that it only
encrypts 768x768 images, then we started encrypting random images to see what it
does.

We determined that all the encryption does is shuffle the columns in some static
way and xor a static pattern on top. We then encrypted images with a single
pixel moving to determine the column permutation, then used that to unshuffle
the encrypted flag image. We then encrypted a blank image to get the static
pattern to xor the flag image with.

Solve script in [solve.py](solve.py).
