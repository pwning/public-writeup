from pwn import *
from z3 import *
import z3

def solve_1():
    return xor(''.join([chr(ord(i)-7) for i in  'DuMb']), '\x04\x131v5r&I'[::-1]+'\x4e\x5e')

def solve_2():
    c = [0x95CB8DBD,
    0xF84CC79,
    0xB899A876,
    0xA5DAB55,
    0x9A8B3BBA,
    0x70B238A7,
    0x72B53CF1,
    0xD47C0209]
    core = [0x43, 0x30, 0x52, 0x33]
    flag = [None]*8
    for i in range(4):
        constant0 = []
        constant4 = []
        k = 0
        for j in range(32):
            constant0.append((core[k & 3] + k) & 0xFFFFFFFF)
            k += 0x1337DEAD
            k &= 0xFFFFFFFF
            constant4.append((core[(k >> 11) & 3] + k) & 0xFFFFFFFF)
        chr0 = c[2*i]
        chr4 = c[2*i+1]
        for j in range(32)[::-1]:
            chr4 -= (((chr0 >> 5) ^ 16 * chr0) + chr0) ^ constant4[j];
            chr4 &= 0xFFFFFFFF
            chr0 -= (((chr4 >> 5) ^ 16 * chr4) + chr4) ^ constant0[j];
            chr0 &= 0xFFFFFFFF
        flag[i] = chr0
        flag[i+4] = chr4
    return(''.join(map(chr, flag)))

def solve_3():
    table = "*|-Ifnq20! \nAZd$r<Xo\\D/{KC~a4Tz7)Y^:x`\v}Ss1yOmiv#\r%]@[_N(Hj,VQug"
    check = "4`Q%A_A#T:Z%A/H}{%mSA[Q\v"
    s = ''
    for i in range(0, len(check), 4):
        c = map(lambda x: table.index(x), check[i:i+4])
        s += chr((c[0] << 2) | (c[1] >> 4))
        s += chr(((c[1] & 0xF) << 4) | (c[2] >> 2))
        s += chr(((c[2] & 0x3) << 6) | c[3])
    return s

def solve_4():
    flaglen = 0xc
    b = (
    '30645F7361336C50'.decode('hex')[::-1]+
    '353452635F74276E'.decode('hex')[::-1]+
    '21682B5F6E315F68'.decode('hex')[::-1]+
    '312B436E55665F73'.decode('hex')[::-1]+
    '6E30'.decode('hex')[::-1]
    )
    c = (
        '14DD43A0935D552B'.decode('hex')[::-1]+
        'E57D5243'.decode('hex')[::-1]
    )
    b = [ord(i) for i in b]
    c = [ord(i) for i in c]
    perm = list(range(246))
    k = 0
    for j in range(246):
        k = (b[j%34] + perm[j] + k) % 246
        perm[j], perm[k] = perm[k], perm[j]
    j = 0
    k = 0
    out = [None]*flaglen
    s = ''
    for i in range(flaglen):
        j = (j+1)%246
        k = (perm[j] + k) % 246
        perm[j], perm[k] = perm[k], perm[j]
        s += chr(c[i] ^ perm[(perm[j] + perm[k])%246])
    return s

def solve_5():
    polynomial = 0xEDB88320
    def crc32(data,size,prev=0):
	    crc = prev ^ 0xFFFFFFFF
	    for i in range(0,size,8):
		    crc = crc ^ (z3.LShR(data,i) & 0xFF)
		    for _ in range(8):
			    crc = If(crc & 1 == BitVecVal(1, size), z3.LShR(crc,1) ^ polynomial, z3.LShR(crc,1))
	    return crc 
    s = z3.Solver()
    data = z3.BitVec('data', 32)
    s.add(crc32(data, 32) == 0x29990129)
    if s.check() == z3.sat:
        return hex(int(str(s.model()[data])))[2:].decode('hex')[::-1]

s = 'hitcon{'
s += solve_1()
s += solve_2()
s += solve_3()
s += solve_4()
s += solve_5()
s += '}'
print(s)
