def dehex(x):
    return ''.join(x.split()).decode('hex')

passkey = dehex('''
16 c5 fd 6f 2a c5 fd 6f 01 c5 fd 6f 52 c5 e5 41
48 89 f8 55 ff 72 e0 41 83 e4 08 48 54 24 4c 8d
ed eb 60 c5 6f 62 c5 fd f9 f1 c5 cd 75 db c5 fd
d9 d9 c5 cd d5 f5 c5 ed e4 cd c5 ed 46 60 7d 6f
f0 c5 cd 75 de c5 e5 fd 0f c5 71 d3 c5 e5 eb e4
c5 bd d5 cc c5 3d e4 fc c5 bd 5e 40 7d 6f d5 c5
6f 56 c5 fd db ee c5 ed 00 00 c0 00 6f aa c5 7d
75 c8 c5 f5 5a 40 25 fd cf c5 35 f9 cf c5 b5 d9
''')

constants = dehex('''
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00 80 00 80 00 80 00 80 00 80 00 80 00 80 00 80 00 80 00 80 00 80 00 80 00 80 00 80 00 80 00 80
2d 00 2d 00 2d 00 2d 00 2d 00 2d 00 2d 00 2d 00 2d 00 2d 00 2d 00 2d 00 2d 00 2d 00 2d 00 2d 00
05 06 07 00 01 02 03 04 0d 0e 0f 08 09 0a 0b 0c 05 06 07 00 01 02 03 04 0d 0e 0f 08 09 0a 0b 0c
50 ef a8 77 d4 3b ea 1d 50 ef a8 77 d4 3b ea 1d 50 ef a8 77 d4 3b ea 1d 50 ef a8 77 d4 3b ea 1d
86 f4 43 7a 37 bd 8d de 86 f4 43 7a 37 bd 8d de 86 f4 43 7a 37 bd 8d de 86 f4 43 7a 37 bd 8d de
cb 49 f3 a4 6f d2 21 e9 cb 49 f3 a4 6f d2 21 e9 cb 49 f3 a4 6f d2 21 e9 cb 49 f3 a4 6f d2 21 e9
04 9c 02 4e 01 27 96 93 04 9c 02 4e 01 27 96 93 04 9c 02 4e 01 27 96 93 04 9c 02 4e 01 27 96 93
05 c1 94 e0 4a 70 25 38 05 c1 94 e0 4a 70 25 38 05 c1 94 e0 4a 70 25 38 05 c1 94 e0 4a 70 25 38
8c 11 c6 08 63 04 27 82 8c 11 c6 08 63 04 27 82 8c 11 c6 08 63 04 27 82 8c 11 c6 08 63 04 27 82
ed 18 60 8c 30 46 18 23 ed 18 60 8c 30 46 18 23 ed 18 60 8c 30 46 18 23 ed 18 60 8c 30 46 18 23
fd 8e 68 c7 b4 63 da 31 fd 8e 68 c7 b4 63 da 31 fd 8e 68 c7 b4 63 da 31 fd 8e 68 c7 b4 63 da 31
b8 ee 5c 77 ae 3b d7 1d b8 ee 5c 77 ae 3b d7 1d b8 ee 5c 77 ae 3b d7 1d b8 ee 5c 77 ae 3b d7 1d
06 ea 03 75 97 ba 5d dd 06 ea 03 75 97 ba 5d dd 06 ea 03 75 97 ba 5d dd 06 ea 03 75 97 ba 5d dd
e6 a1 f3 50 6f a8 21 d4 e6 a1 f3 50 6f a8 21 d4 e6 a1 f3 50 6f a8 21 d4 e6 a1 f3 50 6f a8 21 d4
52 1f a9 0f c2 87 e1 43 52 1f a9 0f c2 87 e1 43 52 1f a9 0f c2 87 e1 43 52 1f a9 0f c2 87 e1 43
06 07 00 01 02 03 04 05 0e 0f 08 09 0a 0b 0c 0d 06 07 00 01 02 03 04 05 0e 0f 08 09 0a 0b 0c 0d
04 05 06 07 00 01 02 03 0c 0d 0e 0f 08 09 0a 0b 04 05 06 07 00 01 02 03 0c 0d 0e 0f 08 09 0a 0b
02 03 04 05 06 07 00 01 0a 0b 0c 0d 0e 0f 08 09 02 03 04 05 06 07 00 01 0a 0b 0c 0d 0e 0f 08 09
''')

keys = dehex('''
16 c5 fd 6f 2a c5 fd 6f 01 c5 fd 6f 52 c5 e5 41
48 89 f8 55 ff 72 e0 41 83 e4 08 48 54 24 4c 8d
ed eb 60 c5 6f 62 c5 fd f9 f1 c5 cd 75 db c5 fd
d9 d9 c5 cd d5 f5 c5 ed e4 cd c5 ed 46 60 7d 6f
f0 c5 cd 75 de c5 e5 fd 0f c5 71 d3 c5 e5 eb e4
c5 bd d5 cc c5 3d e4 fc c5 bd 5e 40 7d 6f d5 c5
6f 56 c5 fd db ee c5 ed 00 00 c0 00 6f aa c5 7d
75 c8 c5 f5 5a 40 25 fd cf c5 35 f9 cf c5 b5 d9
f1 ef 56 4e 64 38 c1 30 98 ba e2 d7 b0 1a fb 5f
1d 4d e6 7a e3 0e b5 fd 2e dc a2 54 17 62 d1 ff
21 f0 61 6b e3 62 81 4c b3 b3 25 f1 b0 3b c3 71
45 72 af 05 75 89 c1 ba c6 bc b1 73 f9 77 d0 ee
1d 4f 93 83 68 7f ae a5 8f a9 17 53 aa 9f 6c 37
58 63 d0 05 9c 40 49 8e 61 fd c7 24 11 61 d1 bb
ad d9 76 e5 46 a6 8b 2f d8 70 06 59 43 b6 a1 b5
ce 57 d9 30 71 fe a9 b3 3a db 4b ed 5e 1d 74 b3
e3 22 00 cb 2f 22 bd 71 fa cb ea e9 f3 85 63 a7
6c f5 85 5f 8c 31 e2 1b 9d 22 1f 71 f6 b3 2d 50
76 4e 1f 98 da 25 78 53 28 ce 8d ea 06 35 b0 fa
f7 94 15 97 bd 24 76 00 bb 0b ff 57 19 f3 22 ec
1a 25 6c e6 5a af 49 57 12 84 a5 69 d9 1a ab aa
d8 bd f1 cf 02 f9 f0 7d 7a 7e 8b c5 22 b9 6e f0
b5 93 86 a4 6e 3a 24 bb 85 92 5f 4e 74 8a d5 80
34 33 46 fc ce 64 22 3f 76 e3 f1 88 b2 5a fb c1
81 f7 8b 57 2b ee 3b 27 89 62 f6 e8 55 9e 1a 5b
45 3f 7a 6c 7b 84 31 6f fc a6 27 e8 ff 9a 89 e5
85 ca 13 6f 8a 3e a8 5c 81 52 15 1c 8b 9d e6 0d
75 bf 73 16 5a 1f fa 35 e2 50 eb 37 b6 a6 93 fe
97 68 9c 5b e9 b1 3d 0d 00 9d 17 10 8f 9e a6 ca
43 f6 9e fe 19 35 69 d7 30 19 84 f6 b1 42 bb 5b
66 8c ca e6 4d 8a d9 5d 64 02 25 f4 44 d9 ed a9
a8 60 dd 82 cc 1a b1 74 dd 85 c4 73 1c c8 28 8c
a5 07 e0 87 f0 24 4a 1c 41 01 1e fa b6 94 29 2e
b9 34 18 34 3f 7a 9c 55 f6 d0 90 fc 99 8c b1 19
bd 6b f6 d6 72 f0 5d a3 1f da 3e 1e 98 90 1c 57
10 35 32 48 fb 85 0b 1d e3 7b 7c 07 4f 4e b6 2d
46 35 6e 9f 58 72 77 ca e5 94 b6 17 78 5b 9f 9f
99 c4 27 2a c2 d8 09 92 19 4d f1 7c d0 d0 b0 ea
4e 8f ff 5e 66 46 32 08 24 a6 80 14 d0 96 98 87
9a b9 2b 4f 61 5f ad bb 26 4a 6e ad d3 ae 7e 07
aa d0 4e 7d b1 ad 12 fe 85 0b 5f 5b 43 5a 62 b1
51 6a 8b 24 1a 77 af 0f fc 1c ca 83 ab 5f 19 c5
e4 97 a0 65 66 c0 8c 74 2e fd f8 d5 87 b2 eb cf
92 bd de a8 73 ba 46 23 83 85 6c f6 f4 75 93 10
8a c2 7f 1d fd d1 ab 51 a6 74 dc 68 8a 4a 2b 92
91 31 ef d9 92 6f b9 53 e4 0d 74 79 dd 97 f9 8a
10 e5 bf e0 f3 b4 39 8d 8f 8b a5 3c 96 c3 3c ce
42 35 49 8c 0b 1b 8d 8b dc 91 c1 00 19 b3 9c 90
9b 7f 3b 6f bb 9e b8 8a 56 0b 3a 83 41 35 39 14
bc 47 bd 7c 19 ff b5 96 73 9e 36 99 bf 0b b4 e2
d1 7a c4 72 d2 69 de 33 7e 7d 4f 63 b6 45 d7 c2
00 04 6a 06 6b 34 22 6c e2 12 40 24 13 5c b2 3b
57 cf 8c d5 de a1 e1 7c 3d c8 6e 87 cf a2 e5 27
c7 99 8d 6a 79 ce 88 2b d2 dc 7c f9 91 7b 10 2d
78 ef 29 d7 a7 b2 33 21 cf f2 32 e9 76 92 3f a4
51 b4 67 33 82 80 91 92 2f ae a2 9b bc 23 2c 7c
3c ab 39 33 b5 4b 54 24 33 36 a9 cc 4a bb c0 19
1a 54 e9 4e b5 b3 89 95 f2 9a f4 fe 29 33 d9 86
2e 3c ba 2d 97 51 a0 0f fe 3b 32 a2 ff ac 9f e0
a2 65 61 80 a1 c1 78 ae 23 d2 b2 d2 d7 74 fe e4
08 75 a7 f3 82 b4 ab f5 53 58 39 a3 6c 61 dd 1d
4a 22 d8 fd 13 29 f2 2c a8 40 88 c1 da 5e 6d 1f
e7 51 ea 7b 2c c1 c2 f0 50 9f 54 8f 03 16 44 f0
e4 fc 2d ea 5d dd a7 54 68 83 de cb d9 41 40 36
ba 01 0f 24 8d 2b b7 cd 21 68 c9 11 94 8f 1a 07
69 dd 1a 38 a9 a7 c3 58 a3 58 32 fe 6e 63 91 79
0d 3d af af 82 38 ab de 15 e7 af ea 8e 9a 24 54
e9 db c0 ab fd 0f 2c 84 22 85 23 f5 4e 16 db 8c
0d 8c de 36 4b 75 33 06 16 e5 b9 a9 de 41 3e dd
ac 48 91 15 94 57 40 d0 5b d5 3d 47 55 cb 79 f4
82 12 55 5a 2e d0 39 6f 7f bd 16 8a 64 50 b6 1a
68 e1 bb 9f d5 41 e8 37 2d ce 3c dc 3d 81 61 5b
ae 49 92 6a 9b 23 64 f5 b0 5d 98 4e f1 66 40 53
ef 48 5b b5 c9 d6 67 88 d5 c7 49 c2 8c d6 fa 60
fb 1c a1 1f bd 5a 67 f9 1d 27 35 eb ea 78 58 19
6f 24 7f 16 c6 bd 19 90 7a 9a b4 48 e6 cb 55 39
8a 6c 76 05 b0 ac 4c 49 2a ca e8 73 6c cf b4 ea
8f c7 24 54 b7 23 81 ab e2 d4 a6 90 6b ff 15 c3
37 36 26 9c 2d c0 a4 7d c4 48 1e 89 ef 10 84 d3
64 ad 58 72 eb ab 1e 77 6a 47 d5 30 94 02 e1 b4
59 6f d1 79 0d fb 20 59 c1 87 4b c4 9a d5 86 2e
e5 8e 37 6e c2 e5 08 7e 56 82 79 05 85 5c 77 69
c6 b8 af 4e f4 07 68 e6 91 f9 f4 be d6 d6 40 e9
1b be e3 08 7b 1f 97 20 49 3e f0 4b f7 1a 96 2f
5e 5f 37 bf 16 b2 f5 a9 f4 c6 9e 9f d1 f5 ca b2
df b5 c7 24 56 99 7c d2 fa f3 2b 31 dd 05 70 7d
08 d2 ec 30 a0 ed b9 98 9c 44 94 f7 5e eb 6d 25
4d 1a 09 32 af 05 87 07 cf 57 07 3d 68 9e 63 86
67 af 8a 48 a2 d9 c2 41 5c ce 55 c2 d8 7e 10 9e
56 81 9c 68 06 29 c8 84 cb 94 aa 49 e2 38 58 e6
c0 43 2a 2e 07 a4 1c e1 48 27 61 3d dc 3f 0e 59
f4 f0 74 d5 ba d4 6a e7 c1 4d 4b 5f 45 ae 01 9e
1d 95 8e a6 1e fd 98 54 6a 0b 5a 4c fe 92 37 d7
0d e8 bd 8e b8 93 19 04 b1 a0 af df 56 91 eb b4
7e 30 45 c8 da 0f 90 8e 19 84 64 7f 66 c5 ef 33
f4 e4 de 0a 72 c9 bd b2 8e 9f 84 e0 55 b9 c9 73
f6 f4 73 7d 86 fa 27 c5 33 2e 20 d8 12 21 0b f6
ac 00 27 8a 05 d6 08 f6 e3 04 0b 6e 4b c8 34 3d
91 6c c4 c4 b4 de 7d b5 fe 8b 35 89 5e d9 70 f1
7f 59 90 89 3a 04 7b ea d0 27 ca e3 00 58 fc 55
e9 e8 aa c9 56 66 bc 93 a1 ae e4 99 81 0d 14 9b
c0 35 44 bf 9e 0a 37 00 47 51 9b 3b a1 4e 70 cb
2a c9 a0 07 f8 d2 e9 e6 ff e9 1d 47 b1 ca 37 95
15 fa 70 0b 71 27 84 15 65 c2 20 f1 63 51 df 90
''')

# ----------------------------------------------------------------------------------------
import struct
import operator

def tou16(v):
    return struct.unpack('<16H', v)

def fromu16(v):
    return struct.pack('<16H', *v)

def reorder(x):
    # implement reordering between input and output
    return fromu16(tou16(x)[::-1])

def getvec(s, off):
    return s[off:off+32]

def applyw(f, *vecs):
    return fromu16([f(*args) & 0xffff for args in zip(*map(tou16, vecs))])

def vpaddw(v1, v2):
    return applyw(operator.add, v1, v2)

def vpsubw(v1, v2):
    return applyw(operator.sub, v1, v2)

def vpxor(v1, v2):
    return applyw(operator.xor, v1, v2)

def vpsllw(v, a):
    return applyw(lambda x: (x << a), v)

def vpshufw(v, imm):
    i0, i1, i2, i3 = (imm & 3), (imm >> 2) & 3, (imm >> 4) & 3, (imm >> 6) & 3
    v = tou16(v)
    return fromu16([v[i0], v[i1], v[i2], v[i3],
                    v[i0+4], v[i1+4], v[i2+4], v[i3+4],
                    v[i0+8], v[i1+8], v[i2+8], v[i3+8],
                    v[i0+12], v[i1+12], v[i2+12], v[i3+12],
                   ])

def vpshufb(v1, v2):
    out = []
    for i in [0, 16]:
        for j in xrange(16):
            out.append(v1[i+ord(v2[i+j])])
    return ''.join(out)

def funky(a, b):
    # vpmullw, vpmulhuw, vpor, ..., vpaddw, vpsubw chain
    mul = a*b
    lw = mul & 0xffff
    hw = mul >> 16
    sub = (lw - hw) & 0xffff
    r1 = sub + (lw <= hw)
    r2 = (a | b) & ((sub == 0) * 0xffff)
    return (r1 - r2) & 0xffff

def mul65537(a, b):
    if a == 0:
        a = 65536
    if b == 0:
        b = 65536
    res = (a * b) % 65537
    if res == 65536:
        res = 0
    #assert res == funky(a, b)
    return res

def vmul65537(v1, v2):
    return applyw(mul65537, v1, v2)

def weird(a):
    if a & 0x8000:
        return 0x2d
    return 0

def vshufnet(v):
    x = vpshufw(v, 0x93)
    y = vpxor(x, v)
    z = vpxor(vpxor(x, vpsllw(y, 1)), vpshufw(y, 0x4e))
    res = vpxor(applyw(weird, y), z)
    return res

def encRound(invecs, keyoff):
    r0 = vmul65537(invecs[0], getvec(keys, keyoff + 0))
    r1 =    vpaddw(invecs[1], getvec(keys, keyoff + 0x20))
    r2 =    vpaddw(invecs[2], getvec(keys, keyoff + 0x40))
    r3 = vmul65537(invecs[3], getvec(keys, keyoff + 0x60))
    x0 = vpxor(r0, r2)
    x1 = vpxor(r1, r3)
    y0 = vmul65537(x0, getvec(keys, keyoff + 0x80))
    y1 = vmul65537(vshufnet(vpaddw(y0, x1)), getvec(keys, keyoff + 0xa0))
    y2 = vpaddw(y1, y0)

    o0 = vpxor(y1, r0)
    o1 = vpshufb(vpxor(y1, r2), getvec(constants, 0x200))
    o2 = vpshufb(vpxor(y2, r1), getvec(constants, 0x220))
    o3 = vpshufb(vpxor(y2, r3), getvec(constants, 0x240))

    return [o0, o1, o2, o3]

def encrypt(inblock):
    vecs = [reorder(getvec(inblock, 0x20*i)) for i in xrange(4)]
    for i in xrange(8):
        vecs = encRound(vecs, i*0xc0)

    r0 = vmul65537(vecs[0], getvec(keys, 0x600))
    r1 =    vpaddw(vecs[1], getvec(keys, 0x620))
    r2 =    vpaddw(vecs[2], getvec(keys, 0x640))
    r3 = vmul65537(vecs[3], getvec(keys, 0x660))

    outblock = ''.join(reorder(v) for v in [r0, r1, r2, r3])
    return outblock

encdata = encrypt(bytearray([0, 0] + range(126)))
print encdata.encode('hex')
print '-' * 60

# ---------------------------------------
from Crypto.Util.number import inverse

def de_mul65537(res, a):
    if a == 0:
        a = 65536
    if res == 0:
        res = 65536
    b = (inverse(a, 65537) * res) % 65537
    if b == 65536:
        b = 0
    return b

def de_vmul65537(v1, v2):
    return applyw(de_mul65537, v1, v2)

def de_vpshufb(v1, v2):
    out = []
    for i in [0, 16]:
        for j in xrange(16):
            out.append(v1[i+v2[i:i+16].index(chr(j))])
    return ''.join(out)

def decRound(vecs, keyoff):
    o0 = vecs[0]
    o1 = de_vpshufb(vecs[1], getvec(constants, 0x200))
    o2 = de_vpshufb(vecs[2], getvec(constants, 0x220))
    o3 = de_vpshufb(vecs[3], getvec(constants, 0x240))

    x0 = vpxor(o0, o1)
    x1 = vpxor(o2, o3)
    y0 = vmul65537(x0, getvec(keys, keyoff + 0x80))
    y1 = vmul65537(vshufnet(vpaddw(y0, x1)), getvec(keys, keyoff + 0xa0))
    y2 = vpaddw(y1, y0)

    r0 = vpxor(o0, y1)
    r1 = vpxor(o2, y2)
    r2 = vpxor(o1, y1)
    r3 = vpxor(o3, y2)

    return [
        de_vmul65537(r0, getvec(keys, keyoff + 0)),
              vpsubw(r1, getvec(keys, keyoff + 0x20)),
              vpsubw(r2, getvec(keys, keyoff + 0x40)),
        de_vmul65537(r3, getvec(keys, keyoff + 0x60)),
    ]

def decrypt(outblock):
    vecs = [reorder(getvec(outblock, 0x20*i)) for i in xrange(4)]

    r0 = de_vmul65537(vecs[0], getvec(keys, 0x600))
    r1 =       vpsubw(vecs[1], getvec(keys, 0x620))
    r2 =       vpsubw(vecs[2], getvec(keys, 0x640))
    r3 = de_vmul65537(vecs[3], getvec(keys, 0x660))

    vecs = [r0, r1, r2, r3]

    for i in reversed(xrange(8)):
        vecs = decRound(vecs, i*0xc0)

    inblock = ''.join(reorder(v) for v in vecs)
    return inblock

print decrypt(encdata).encode('hex')

with open('ciphertext', 'rb') as inf, open('plaintext.jpg', 'wb') as outf:
    while 1:
        chunk = inf.read(0x80)
        if len(chunk) < 0x80:
            outf.write(chunk)
            break
        outf.write(decrypt(chunk))

# INS{XuejiaLai_StudentOfJim_YOUROCK}
