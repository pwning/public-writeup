import sys
from socket import *
TARGET = ('dub-key-t8xd5pn6.9447.plumbing', 9447)

s = socket()
s.connect(TARGET)

def rd(*suffixes):
    out = ''
    while 1:
        x = s.recv(1)
        if not x:
            raise EOFError()
        sys.stdout.write(x)
        sys.stdout.flush()
        out += x

        for suffix in suffixes:
            if out.endswith(suffix):
                break
        else:
            continue
        break
    return out

def pr(x):
    s.send(str(x))
    print "<%s" % x

prefix = s.recv(12)
print "solving challenge..."
from hashlib import sha1
from itertools import product
alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
for cand in product(alphabet, repeat=8):
    test = prefix + ''.join(cand)
    if sha1(test).digest().endswith('\x00\x00\x00'):
        s.send(test)
        break

data = rd('1) Sign something\n')
import re
tosign = re.findall(r'You need to sign:\n(.+)\n', data)[0].decode('base64')

def sign(x):
    import base64
    rd('of data\n')
    print "signing", x.encode('hex')
    pr('1\n')
    pr(base64.b64encode(x))
    return int(rd('\n'))

def edit(x, i, v):
    y = bytearray(x)
    y[i] = v
    return bytes(y)

# Find two unused points.
identity = bytearray(xrange(128, 256))
baseline = sign(bytes(identity))
t = []
for i in set(xrange(128, 256)) - set(bytearray(tosign)):
    newval = sign(edit(identity, i-128, 128))
    if newval == baseline * 2:
        t.append(i)
        if len(t) == 2:
            break

if len(t) < 2:
    print "FAILED"
    exit()

# Find the chain lengths for each unused point independently.
a = sign(edit(edit(tosign, t[0]-128, t[0]), t[1]-128, t[1]))
b = sign(edit(tosign, t[0]-128, t[0]))
c = sign(edit(tosign, t[1]-128, t[1]))
pr('2\n')
pr(str(a * (b//a) * (c//a)).zfill(620))
rd()

# 9447{Th1s_ta5k_WAs_a_B1T_0F_A_DaG}
