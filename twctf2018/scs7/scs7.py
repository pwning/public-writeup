from pwn import *
import base59

alpha = '123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

LEN = 47

r = remote('crypto.chal.ctf.westerns.tokyo',14791)
target = r.recvline().split()[2]

def doit(s):
    r.sendline(s)
    l = r.recvline_contains('ciphertext')
    x = l.split()[-1]
    return x

plain = ''
cipher = ''

import random
for i in range(10):
    s = ''.join(random.choice(alpha) for i in range(LEN))
    pp = base59.b59encode(s)
    plain += pp
    cc = doit(s)
    cipher += cc
    print(pp)
    print(cc)

print(len(plain))
print(len(cipher))

import string

x = target.translate(string.maketrans(cipher, plain))
print(x)
print(base59.b59decode(x))
