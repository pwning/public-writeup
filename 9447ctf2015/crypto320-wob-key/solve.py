import sys
from socket import *
TARGET = ('wob-key-e1g2l93c.9447.plumbing', 9447)

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

sigs = {}
def sign(x):
    if x in sigs:
        return sigs[x]

    import base64
    rd('of data\n')
    print "signing", x.encode('hex')
    pr('1\n')
    pr(base64.b64encode(x))
    res = int(rd('\n'))
    sigs[x] = res
    return res

def edit(x, i, v):
    y = bytearray(x)
    y[i] = v
    return bytes(y)

# Find an uninvolved point (a point that is not in the secret).
identity = bytearray(xrange(128, 256))
baseline = sign(bytes(identity))
t = []
for i in set(xrange(128, 256)):
    newval = sign(edit(identity, i-128, 128))
    if newval == baseline * 2:
        t.append(i)
        if len(t) == 1:
            break

if len(t) < 1:
    # very unlikely
    print "FAILED"
    exit()

# OK, we have our baseline + an uninvolved point. Figure out cycle lengths.
cycles = {}
for i in xrange(0, 128):
    res = sign(edit(identity, t[0]-128, i))
    assert res % baseline == 0
    cycles[i] = (res // baseline) - 1
    # e.g. 130->0->140 = 2
    # e.g. 130->0->2->0 = 2
    # e.g. 130->0->0 = 1

# Now figure out which cycles exit to the second half ("external")
shift_order = [x for x in xrange(128, 256) if x not in t]
shift = identity[:]
shift[shift_order[0] - 128] = shift_order[0]
for i in xrange(len(shift_order)-1):
    shift[shift_order[i+1] - 128] = shift_order[i]
baseline2 = sign(bytes(shift))

cycles2 = {}
for i in xrange(0, 128):
    res = sign(edit(shift, t[0]-128, i))
    assert res % baseline2 == 0
    print i, res//baseline2
    cycles2[i] = (res // baseline2) - 1
    # e.g. 130->0->140->139->138->...->128

sec1 = {} # idx -> (exit, cyclen)
for i in xrange(0, 128):
    d = cycles2[i] - cycles[i]
    if d == 0:
        sec1[i] = (None, cycles[i])
    else:
        sec1[i] = (shift_order[d], cycles[i]-1)

# Resolve chains
from collections import defaultdict
secrev = defaultdict(list)
for i in sec1:
    secrev[sec1[i]].append(i)

sec2 = {}
for i in xrange(0, 128):
    end, cyclen = sec1[i]
    if end is None:
        # internal cycle; record only length
        sec2[i] = -cyclen
        continue
    if cyclen == 1:
        # directly connects to the end
        sec2[i] = end
        continue
    possible = secrev[end, cyclen-1]
    assert possible
    if len(possible) == 1:
        # only one possible path to the end
        sec2[i] = possible[0]
        continue

    tosign = edit(identity, end-128, i)
    baseline3 = sign(tosign)

    # disambiguate between possible paths
    for j in possible[:-1]:
        # either i->j, in which case we get
        #   spare->j->...->end->i->j
        # or i-/>j in which case
        #   spare->j->...->end->i->k->...->end (longer)
        # and so we can determine whether i->j directly.
        res = sign(edit(tosign, t[0]-128, j))
        assert res % baseline3 == 0
        if cyclen == res//baseline3-2:
            sec2[i] = j
            break
    else:
        sec2[i] = possible[-1]

sec2 = [sec2[i] for i in xrange(0, 128)]

print "USED %d ATTEMPTS" % len(sigs)

def cycle_len(x, i):
    seen = set()
    count = 0
    while i not in seen:
        if i < 0:
            count += -i-1
            break
        seen.add(i)
        count += 1
        i = x[i]
    return count

def mysign(x):
    # Compute a signature using sec2
    x = sec2 + map(ord, x)
    res = 1
    for i in xrange(256):
        res *= cycle_len(x, i)
    return res

for x in sigs:
    assert mysign(x) == sigs[x]

# Ready to sign stuff for real!!
pr('2\n')
for i in xrange(17):
    rd('to sign:\n')
    data = rd('\n').strip().decode('base64')
    assert len(data) == 128
    pr(str(mysign(data)).zfill(620))

rd()

# Easy: 9447{S1gning_15_HaRD_0Bvi0Usly}
# Hard: 9447{Alth0ugh_be1Ng_sm4rt_iS_eVen_b3tter}
