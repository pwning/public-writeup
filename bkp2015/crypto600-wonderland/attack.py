import sys
from socket import *
import time

TARGET = ('54.86.168.156', 40638)
#TARGET = ('localhost', 40638)

def rd(*suffixes):
    out = ''
    while 1:
        try:
            x = s.recv(1)
            if not x:
                break
            sys.stdout.write(x)
            sys.stdout.flush()
            out += x
        except timeout:
            if out:
                return out
            continue

        for suffix in suffixes:
            if out.endswith(suffix):
                break
        else:
            continue
        break
    return out

def pr(x):
    s.send(x)
    print "<%s" % x

def solve_challenge(s):
    from hashlib import sha1
    import itertools

    start = s.split(" ")[-1]
    print "Generating challenge response..."

    chrs = map(chr, xrange(256))

    for i, s in enumerate(itertools.product(chrs, repeat=8)):
        if i % 131072 == 0:
            print "tested: ", i
        s = ''.join(s)
        ha = sha1()
        ha.update(start + s)
        digest = ha.digest()
        if digest.endswith("\xff\xff"):
            return start + s
    return None

def test_pt(n):
    global s
    s = socket()
    s.connect(TARGET)
    s.settimeout(0.1)

    answer = solve_challenge(s.recv(12))
    s.send(answer)

    pr(str(n))
    res = int(rd())
    print
    return res

from server import multiply, square, normalize, power
BASE = 8
SORDER = 1461501637330902918203685651179313124738649676760
factors = [5, 7, 31, 5857, 3280967, 68590573243, 308648791439, 413879086189]

def epow(x, n):
    return normalize(power((x, 1), n))

def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a / b
        a, b = b, a%b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1
 
def chinese_remainder(n, a, lena):
    p = i = prod = 1; sm = 0
    for i in range(lena): prod *= n[i]
    for i in range(lena):
        p = prod / n[i]
        sm += a[i] * mul_inv(p, n[i]) * p
    return sm % prod

def dlog(P, b, n):
    ta = {}
    tb = {}
    i = 0
    base = 7
    # a = iP
    # b = (base**j)nP
    # thus: n = i * (base**j)^-1
    res = None
    for i in xrange(n):
        if i % 10000 == 0:
            print '<...%d...>' % i,
            sys.stdout.flush()
        a = epow(P, i)
        ta[a] = i
        tb[b] = i
        if b in ta:
            res = ta[b], i
            break
        if a in tb:
            res = i, tb[a]
            break
        b = epow(b, base)
        i += 1
    if res is None:
        return (0,)
    ai, bi = res
    v = ai * pow(pow(7, bi, n), n-2, n)
    return (v%n, (-v)%n)

results = [[(8, 0)]]

for f in factors:
    P = epow(BASE, SORDER / f)
    # (f+1)P = P
    nP = test_pt(P)
    print f,
    out = dlog(P, nP, f)
    print out
    results.append([(f, x) for x in out])

checkP = 2
check = test_pt(checkP)

import itertools
for k in itertools.product(*results):
    nn, aa = zip(*k)
    n = chinese_remainder(nn, aa, len(nn))
    print n
    if epow(checkP, n) == check:
        print "FLAG:", hex(n)
