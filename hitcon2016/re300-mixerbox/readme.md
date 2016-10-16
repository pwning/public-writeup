## MixerBox - Reversing 300

### Description

Mixed-arch, mixerbox

### Writeup

As the description states, the goal is to reverse engineer a Linux binary that uses both 32-bit and 64-bit code. We used gdb and IDA Pro to statically analyze the binary and then confirm our hypotheses by running the program.

The program implements some basic cryptographic primitives: swap columns, swap rows, swap blocks, rotate, mix, etc. We spent most of our time reimplementing the algorithm in python. Once our python implementation was correct, we inversed every operation. With the inverse algorithm, we were able to extract the secret.

Solution: [exploit.py](exploit.py)
