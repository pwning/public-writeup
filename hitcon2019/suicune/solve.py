import sys
from ctypes import CDLL, c_uint32, c_uint64
import math

# Load a compiled version of the PCG library
pcg = CDLL('./pcg_basic.so')
pcg.pcg32_srandom.argtypes = [c_uint64, c_uint64]
pcg.pcg32_random.restype = c_uint32
pcg.pcg32_boundedrand.argtypes = [c_uint32]
pcg.pcg32_boundedrand.restype = c_uint32

gflag = bytes.fromhex('04dd5a70faea88b76e4733d0fa346b086e2c0efd7d2815e3b6ca118ab945719970642b2929b18a71b28d87855796e344d8')
#gflag = bytes.fromhex('6825b254ef20e7a6e984411f49') # abcdefghijklm 1
#gflag = bytes.fromhex('c3e1bc4209218b483a') # hitcon{f} 461

def to_index(perm):
    alphabet = sorted(perm)
    n = len(perm)
    idx = 0
    for i, v in enumerate(perm):
        idx += math.factorial(n - i - 1) * alphabet.index(v)
        alphabet.remove(v)
    return idx

def from_index(alphabet, idx):
    alphabet = sorted(alphabet)
    n = len(alphabet)
    out = []
    for i in range(n):
        pos, idx = divmod(idx, math.factorial(n - i - 1))
        out.append(alphabet[pos])
        alphabet.remove(alphabet[pos])
    assert idx == 0
    return out

def calc_xor(key):
    pcg.pcg32_srandom(key, 0)
    flag = bytearray(gflag)

    for _ in range(16):
        # Fisher-Yates shuffle
        a = list(range(256))
        for i in range(255, 0, -1):
            j = pcg.pcg32_boundedrand(i+1)
            a[j], a[i] = a[i], a[j]

        a = a[:len(flag)]

        v = pcg.pcg32_random()
        v |= pcg.pcg32_random() << 32
        idx = to_index(a)
        new_idx = min(v + idx, math.factorial(len(flag))-1)
        a = from_index(a, new_idx)

        for i in range(len(flag)):
            flag[i] ^= a[i]
        flag = flag[::-1]

    return flag, key

import multiprocessing
p = multiprocessing.Pool(16)

for rflag, rkey in p.imap_unordered(calc_xor, range(65536)):
    if b'hitcon' in rflag.lower():
        print(rflag, rkey)

# hitcon{nth_perm_Ruby_for_writing_X_C_for_running}
