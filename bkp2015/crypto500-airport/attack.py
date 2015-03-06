import sys
from socket import *
import time

TARGET = ('52.1.245.61', 1025)
#TARGET = ('localhost', 1234)

s = socket()
s.connect(TARGET)
s.settimeout(0.1)

def rd(*suffixes):
    out = ''
    while 1:
        try:
            x = s.recv(1)
            if not x:
                raise EOFError()
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
        if digest.endswith("\xff\xff\xff"):
            return start + s
    return None

answer = solve_challenge(s.recv(12))
s.send(answer)

SAFEPRIME = 27327395392065156535295708986786204851079528837723780510136102615658941290873291366333982291142196119880072569148310240613294525601423086385684539987530041685746722802143397156977196536022078345249162977312837555444840885304704497622243160036344118163834102383664729922544598824748665205987742128842266020644318535398158529231670365533130718559364239513376190580331938323739895791648429804489417000105677817248741446184689828512402512984453866089594767267742663452532505964888865617589849683809416805726974349474427978691740833753326962760114744967093652541808999389773346317294473742439510326811300031080582618145727L

def nth_root(x, r, p):
    q = (p-1)/2 # assume it is a safeprime
    return pow(x, pow(r, q-2, p-1), p)

def brute_key():
    cur = 0
    while 1:
        cand = cur*2+1
        t = time.time()
        pr(str(nth_root(4, cand, SAFEPRIME)))
        result = rd()
        elapsed = time.time() - t

        print
        print "time:", elapsed,
        if 1.2 <= elapsed <= 1.4:
            cur = cur*2 + 1
            print "(+1)"
        elif 0.2 <= elapsed <= 0.4:
            cur = cur*2
            print "(+0)"
        else:
            print "(out of range)"
        print "current:", bin(cur)

        # Sanity check
        if bin(cur).endswith('0' * 100):
            print "didn't see ones for a while: rolling back"
            cur >>= 105

brute_key()
