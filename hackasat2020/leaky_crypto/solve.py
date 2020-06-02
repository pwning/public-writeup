# Run faster using pypy :)
# pip install pycryptodome && pip install tqdm

from Crypto.Cipher import AES
from tqdm import tqdm

with open('./provided/Readme.txt') as f:
    d = f.read().split('\n')
    enc_data = (
        [x for x in d if 'Encrypted Data' in x][0].split()[-1].decode('hex'))
    known_bytes = (
        [x for x in d if 'Key Bytes' in x][0].split()[-1].decode('hex'))

with open('./provided/test.txt') as f:
    d = [x.split(',') for x in f.read().strip().split('\n')]
    timing = {
        tuple(map(ord, x.decode('hex'))): int(y)
        for x, y in d
    }

print "[+] Finished reading %d timing values" % len(timing)
print "[ ] Starting correlation analysis"

max_timing = max(timing.values())

correlations = []
for i in tqdm(xrange(16)):
    for j in xrange(i + 1, 16):
        t = [0 for _ in xrange(256)]
        for k, v in timing.iteritems():
            p = k[i] ^ k[j]
            t[p] = max(t[p], v)
        m = min(t)
        assert m != 0
        if m != max_timing:
            top_bytes = t.index(m) & (0xff - 0x3)
            assert t.count(m) == 4
            assert all(i & (0xff - 0x3) == top_bytes
                       for i, x in enumerate(t) if x == m)
            correlations.append((i, j, t.index(m)))

print "[+] Found %d correlations" % len(correlations)

key = list(map(ord, known_bytes))
key += [None for _ in xrange(16 - len(key))]

for i, j, v in correlations:
    if key[i] is None:
        if key[j] is None:
            continue
        else:
            key[i] = key[j] ^ v
    else:
        if key[j] is None:
            key[j] = key[i] ^ v
        else:
            if (key[i] ^ key[j]) >> 2 != (v >> 2):
                print "Weird %d %d %d %d" % (i, j, key[i] ^ key[j], v)

for i in xrange(len(known_bytes), 16):
    if key[i] is not None:
        key[i] = key[i] & (0xff - 0x3)
        assert key[i] & 0x3 == 0, key[i]

partial_bytes = 16 - (len(known_bytes) + key.count(None))
unknown_bytes = key.count(None)
reqd_brute_bits = 2 * partial_bytes + 8 * unknown_bytes

print "[+] Inferred %d partial bytes. %d completely unknown bytes." % (
    partial_bytes, unknown_bytes
)
print "    %s" % repr(key)
print "[ ] Starting brute force of %d bits." % (
    reqd_brute_bits
)

for brute in tqdm(xrange(2 ** reqd_brute_bits)):
    key_guess = key[:]
    for i in xrange(len(known_bytes), 16):
        if key_guess[i] is None:
            key_guess[i] = (brute & 0x3f) << 2
            brute = brute >> 6
    for i in xrange(len(known_bytes), 16):
        key_guess[i] = key_guess[i] | (brute & 0x3)
        brute = brute >> 2
    assert brute == 0
    cipher = AES.new(''.join(map(chr, key_guess)), AES.MODE_ECB)
    res = cipher.decrypt(enc_data)
    if 'flag{' in res:
        print
        print "[+] Found flag: %s" % repr(res)

print "[+] Finished"
# Note: Result found at 53401956
