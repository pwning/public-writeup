from prog import prog

ops = {
    2: lambda x, y: (x - y) & 0xffffffff,
    11: lambda x, y: x & y,
    12: lambda x, y: x | y,
    13: lambda x, y: x ^ y,
    15: lambda x, y: y,
    21: lambda x, y: (x << y) & 0xffffffff,
    22: lambda x, y: (x >> y),
}

def emulate(pc, r0, r1):
    regs = [r0, r1] + [None] * 22
    stack = []
    while 1:
        amode, opc, x, y = prog[pc]
        if opc == 17:
            break

        if amode == 1:
            opy = y
        elif amode == 2:
            opy = regs[y]
        else: raise NotImplementedError(pc, prog[pc])

        if opc == 18:
            stack.append(regs[x])
        elif opc == 19:
            regs[x] = stack.pop()
        elif opc in ops:
            regs[x] = ops[opc](regs[x], opy)
        else: raise NotImplementedError(pc, prog[pc])

        pc += 1
    return (regs[0], regs[1])

f1_table = []
for i in range(1<<16):
    f1_table.append(emulate(0x0000, i, None)[0])

f2_table = []
for i in range(1<<16):
    f2_table.append(emulate(0x00c0, i, None)[0])

bits = [(1 << i, 0) for i in range(32)]
bits += [(0, 1 << i) for i in range(32)]
invbits = {v:k for k,v in enumerate(bits)}

f7_table = [invbits[emulate(0x0221, *bits[i])] for i in range(64)]

f8_table = [invbits[emulate(0x028d, *bits[i])] for i in range(64)]

def f3(r0, r1):
    r0 = (f2_table[r0 >> 16] << 16) | f1_table[r0 & 0xffff]
    r1 = (f1_table[r1 >> 16] << 16) | f2_table[r1 & 0xffff]
    return (r0, r1)

mem = [4, 7, 2, 1, 8, 0xb, 0xe, 0xd, 0xf, 0xc, 9, 10, 3, 0, 5, 6, 0xd, 3, 2, 0xc, 0, 0xe, 0xf, 1, 4, 10, 0xb, 5, 9, 7, 6, 8]

def apply_sbox(r0, r1, table):
    v = (r1 << 32) | r0
    res = 0
    for i in range(16):
        res |= table[(v >> (i * 4)) & 0xf] << (i * 4)
    return (res & 0xffff_ffff), res >> 32

def f6(r0, r1, r2):
    assert r2 in [0, 16]
    return apply_sbox(r0, r1, mem[r2:r2+16])

# validate the linearity of the sboxes
for r2 in (0, 16):
    c = mem[r2 + 0]
    b0 = mem[r2 + 1] ^ c
    b1 = mem[r2 + 2] ^ c
    b2 = mem[r2 + 4] ^ c
    b3 = mem[r2 + 8] ^ c
    for i in range(16):
        res = c
        if i & 1: res ^= b0
        if i & 2: res ^= b1
        if i & 4: res ^= b2
        if i & 8: res ^= b3
        assert res == mem[r2 + i]

def apply_bitmap(r0, r1, table):
    res = [0, 0]
    for i in range(64):
        m0, m1 = bits[i]
        if (r0 & m0) or (r1 & m1):
            b0, b1 = bits[table[i]]
            res[0] |= b0
            res[1] |= b1
    return (res[0], res[1])

def f7(r0, r1):
    return apply_bitmap(r0, r1, f7_table)

def f8(r0, r1):
    return apply_bitmap(r0, r1, f8_table)

# test
import random
r0 = random.getrandbits(32)
r1 = random.getrandbits(32)
assert f7(r0, r1) == emulate(0x0221, r0, r1)
assert f8(r0, r1) == emulate(0x028d, r0, r1)

def encrypt(r01, r23):
    r0 = r01 & 0xffffffff
    r1 = r01 >> 32
    r2 = r23 & 0xffffffff
    r3 = r23 >> 32

    r4 = 0x4c414355
    r5 = 0x43415241

    r0 ^= r4 ^ r2
    r1 ^= r5 ^ r3
    r0, r1 = f6(r0, r1, 0)
    r0, r1 = f3(r0, r1)
    r0, r1 = f7(r0, r1)

    r0 ^= r4 ^ 0x3707344
    r1 ^= r5 ^ 0x13198a2e
    r0, r1 = f6(r0, r1, 0)
    r0, r1 = f3(r0, r1)
    r0, r1 = f7(r0, r1)

    r0 ^= r4 ^ 0x299f31d0
    r1 ^= r5 ^ 0xa4093822
    r0, r1 = f6(r0, r1, 0)
    r0, r1 = f3(r0, r1)
    r0, r1 = f7(r0, r1)

    r0 ^= r4 ^ 0xec4e6c89
    r1 ^= r5 ^ 0x82efa98
    r0, r1 = f6(r0, r1, 0)
    r0, r1 = f3(r0, r1)
    r0, r1 = f7(r0, r1)

    r0 ^= r4 ^ 0x38d01377
    r1 ^= r5 ^ 0x452821e6
    r0, r1 = f6(r0, r1, 0)
    r0, r1 = f3(r0, r1)
    r0, r1 = f7(r0, r1)

    r0 ^= r4 ^ 0x34e90c6c
    r1 ^= r5 ^ 0xbe5466cf
    r0, r1 = f6(r0, r1, 0)
    r0, r1 = f3(r0, r1)
    r0, r1 = f6(r0, r1, 16)

    r0 ^= r4 ^ 0xfd955cb1
    r1 ^= r5 ^ 0x7ef84f78
    r0, r1 = f8(r0, r1)
    r0, r1 = f3(r0, r1)
    r0, r1 = f6(r0, r1, 16)

    r0 ^= r4 ^ 0xf1ac43aa
    r1 ^= r5 ^ 0x85840851
    r0, r1 = f8(r0, r1)
    r0, r1 = f3(r0, r1)
    r0, r1 = f6(r0, r1, 16)

    r0 ^= r4 ^ 0x25323c54
    r1 ^= r5 ^ 0xc882d32f
    r0, r1 = f8(r0, r1)
    r0, r1 = f3(r0, r1)
    r0, r1 = f6(r0, r1, 16)

    r0 ^= r4 ^ 0xe0e3610d
    r1 ^= r5 ^ 0x64a51195
    r0, r1 = f8(r0, r1)
    r0, r1 = f3(r0, r1)
    r0, r1 = f6(r0, r1, 16)

    r0 ^= r4 ^ 0xca0c2399
    r1 ^= r5 ^ 0xd3b5a399
    r0, r1 = f8(r0, r1)
    r0, r1 = f3(r0, r1)
    r0, r1 = f6(r0, r1, 16)

    r16 = ((r3 << 31) & 0xffffffff) | (r2 >> 1)
    r18 = ((r2 << 31) & 0xffffffff) | (r3 >> 1)
    r0 ^= r16 ^ r4 ^ (r3 >> 31) ^ 0xc97c50dd
    r1 ^= r18 ^ r5 ^ 0xc0ac29b7
    return (r1 << 32) | r0

## Everything is linear, so the result should also be linear
c = encrypt(0, 0)
consts = []
for i in range(64):
    consts.append(encrypt(1 << i, 0) ^ c)
inputs = []
for i in range(64):
    inputs.append(encrypt(0, 1 << i) ^ c)

def fast_encrypt(r01, r23):
    res = c
    for i in range(64):
        if r01 & (1 << i):
            res ^= consts[i]
    for i in range(64):
        if r23 & (1 << i):
            res ^= inputs[i]
    return res

res = encrypt(0x3D9BC459_96D0E48B, int.from_bytes(b"codegate", "big"))
assert res == 0x30E7997D_41A1E05C
res = fast_encrypt(0x3D9BC459_96D0E48B, int.from_bytes(b"codegate", "big"))
assert res == 0x30E7997D_41A1E05C

from gf2 import transpose, num2vec, solve_gf2
M = transpose([num2vec(c, 64) for c in inputs])
def invsolve(res, r01):
    res ^= c
    for i in range(64):
        if r01 & (1 << i):
            res ^= consts[i]
    rv = next(solve_gf2(M, num2vec(res, 64)))
    return sum((v << i) for i, v in enumerate(rv))

assert invsolve(0x30E7997D_41A1E05C, 0x3D9BC459_96D0E48B).to_bytes(8, "big") == b"codegate"

print(invsolve((0x7163E0F5 << 32) | 0x57D21D0, (0x959DB87D << 32) | 0xD5DB2C94).to_bytes(8, "big"))
print(invsolve((0xD18F4E13 << 32) | 0x2D47D458, (0x7F920AC7 << 32) | 0xE1D9AB69).to_bytes(8, "big"))
print(invsolve((0x273B255C << 32) | 0xE83B0109, (0xCADCA511 << 32) | 0x740C6CD5).to_bytes(8, "big"))
print(invsolve((0x3ECB6289 << 32) | 0x7AE86AFE, (0x24C49DD1 << 32) | 0x9147A5EF).to_bytes(8, "big"))
print(invsolve((0x73C81102 << 32) | 0x124C8D25, (0xEB531A28 << 32) | 0xADE26435).to_bytes(8, "big"))
print(invsolve((0x80C87931 << 32) | 0xA4FC371C, (0xB5D7D555 << 32) | 0x343E0B03).to_bytes(8, "big"))
print(invsolve((0x8F743074 << 32) | 0x9CEBAD55, (0xCA65A03E << 32) | 0x237CD1E).to_bytes(8, "big"))
print(invsolve((0xF9404F51 << 32) | 0x1C899FBB, (0xA551DBED << 32) | 0xE9B3362E).to_bytes(8, "big"))

# codegate2024{B45IC_i5_n07_d34d_4nd_n3v3r_wi11_b3_2024_MQCJAb4Wr}
