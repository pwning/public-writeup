v = bytearray(b'\x8ec\xcd\x12KX\x15\x17Q"\xd9\x04Q,\x19\x15\x86,\xd1L\x84. \x06\x00')
for i in range(24):
    r = i % 4
    if r == 0:
        v[i] -= 30
    elif r == 1:
        v[i] = (v[i] ^ 7) + 8
    elif r == 2:
        v[i] = ((v[i] + 4) ^ 68) - 44
    elif r == 3:
        v[i] = v[i] ^ (172 & 20) ^ 101

print(v)

# plis-g1v3-me33-th3e-f14g
# hitcon{R3vers3_Da_3moj1}
