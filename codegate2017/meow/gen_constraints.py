def decrypt_test(keylen, datlen):
    # "symbolically" decrypt by using a bitset for the key
    key = [1 << (8 + i) for i in xrange(keylen)]
    dat = range(datlen)

    n = datlen
    ct = dat

    v9 = 0;
    j = 0;
    x3 = 4;
    x2 = 5;
    x1 = 3;
    n3 = 10;
    n2 = 5;
    n1 = 7;
    ka = 0;
    kb = n;
    b3 = [0] * n3
    b2 = [0] * n2
    b1 = [0] * n1
    for i in xrange(0, n, n1):
        for j in xrange(x1):
            b1[j] = ct[j + ka];
        for j in xrange(n1 - x1):
            b1[(j + x1)] = ct[x1 + kb - n1 + j];
        for j in xrange(n1):
            b1[j] ^= key[j];
        for j in xrange(x1):
            ct[j + ka] = b1[(j + n1 - x1)];
        for j in xrange(n1 - x1):
            ct[x1 + kb - n1 + j] = b1[j];
        ka += x1;
        kb -= n1 - x1;
        x1 += 2;
        if x1 == 9:
            x1 = 3;

    ka = 0;
    kb = n;
    for i in xrange(0, n, n2):
        for j in xrange(x2):
            b2[j] = ct[j + ka];
        for j in xrange(n2 - x2):
            b2[(j + x2)] = ct[x2 + kb - n2 + j];
        for j in xrange(n2):
            b2[j] ^= key[2 * j + 1];
        for j in xrange(x2):
            ct[j + ka] = b2[(j + n2 - x2)];
        for j in xrange(n2 - x2):
            ct[x2 + kb - n2 + j] = b2[j];
        ka += x2;
        kb -= n2 - x2;
        x2 -= 1
        if x2 == 0:
            x2 = 5;

    ka = 0;
    kb = n;
    for i in xrange(0, n, n3):
        for j in xrange(x3):
            b3[j] = ct[j + ka];
        for j in xrange(n3 - x3):
            b3[j + x3] = ct[x3 + kb - n3 + j];
        for j in xrange(n3):
            b3[j] ^= key[j];
        for j in xrange(x3):
            ct[j + ka] = b3[j + n3 - x3];
        for j in xrange(n3 - x3):
            ct[x3 + kb - n3 + j] = b3[j];
        ka += x3;
        kb -= n3 - x3;
        x3 += 1
        if x3 == 9:
            x3 = 4;

    ka = 0;
    kb = n;
    x3 = 4;
    for i in xrange(0, n, n3):
        for j in xrange(x3):
            b3[j] = ct[j + ka];
        for j in xrange(n3 - x3):
            b3[j + x3] = ct[x3 + kb - n3 + j];
        for j in xrange(n3):
            b3[j] ^= key[j];
        for j in xrange(x3):
            ct[j + ka] = b3[j + n3 - x3];
        for j in xrange(n3 - x3):
            ct[x3 + kb - n3 + j] = b3[j];
        ka += x3;
        kb -= n3 - x3;
        x3 += 1
        if x3 == 9:
            x3 = 4;

    return dat

cat_encrypted = ''.join('''
F1 64 72 4A 4F 48 4D BA  77 73 1D 34 F5 AF B8 0F
24 56 11 65 47 A3 2F 73  A4 56 4F 70 4A 13 57 9C
3F 6F 06 61 40 90 AF 39  10 29 34 C3 00 7A 40 3D
4E 3F 0E 2A 2F 20 7F 73  89 7D 4B 1D 09 AA D0 00
21 89 4D 2A 67 7C 18 3B  39 F2 8D 1C A7 71 57 2E
31 14 67 48 3C 7D AF 70  AE 10 31 68 D1 26 05 C8
25 F2 62 F5 5D 38 34 F2  20 0E 7E 9F FB 57 72 26
57 67 15 10 15 13 B9 3E  79 89 5D 24 12 01 98 7B
18 25 E0 DF 7C 24 1B 2D  44 B0 10 3D 57 3D 62 B4
21 1D 3E D1 10 D7 45 74  96 2B 6D 3B ED 10 00 67
31 DF 6C B8 86 1A 7C 6B  64 78 C6 37 76 E6 61 A0
AD BE 4C BA A7 0D
'''.split()).decode('hex')

local_encrypted = ''.join('''
61 48 D9 4A 73 48 4D 2A 07 7C 18 A5 F5 AF 73 67
24 56 59 B8 CC 2A 00 C7 95 6F DF 38 23 34 39 24
5C 4F 6E 18 45 32 83 EC B5 5B 58 4A 00 A0 14 6F
24 BE AD BE 4C 2C A7 0D
'''.split()).decode('hex')

# use our symbolic decryptor to generate constraints
for i, c in enumerate(decrypt_test(10, 0xb6)):
    print 'cat[%d] =' % i, ' ^ '.join('k[%d]' % ki for ki in xrange(11) if c & (1 << (8+ki))) + ' ^ ' + '0x%02x' % ord(cat_encrypted[c & 0xff])

for i, c in enumerate(decrypt_test(10, 0x38)):
    print 'local[%d] =' % i, ' ^ '.join('k[%d]' % ki for ki in xrange(11) if c & (1 << (8+ki))) + ' ^ ' + '0x%02x' % ord(local_encrypted[c & 0xff])
