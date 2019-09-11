# fill in s with the output of:
# break *0x402ee1
# x/32x $rdi+0x10
# for the block it's currently encrypting

s = '''
0x78e068:	0x83f19eee	0xda45ed22	0x0f746d84	0x5956ab6d
0x78e078:	0x8917c0ef	0x7a5cf3b6	0x796712dd	0x6009fb1f
0x78e088:	0x6a5bc569	0x376c57d3	0xe9ba0d38	0xbe82e078
0x78e098:	0x77856cc1	0xa273cfee	0xd4142c83	0x017374a6
0x78e0a8:	0xa3aeae68	0x02b52304	0x0e3d4b9e	0x1eb080bf
0x78e0b8:	0x30a8374b	0x84f10f0f	0x02823509	0xd0dabfab
0x78e0c8:	0xc85353c6	0x768e268e	0x0cdd1b42	0xddf3d584
0x78e0d8:	0xfbdba0d4	0xa15d7381	0x83f4a3f6	0xd4eac3ea
'''.strip()

s = ' '.join(i.split(':')[1].strip() for i in s.split('\n'))

constants = map(lambda x: int(x,0), s.split())[:26][::-1]

v1 = 0xd4f5f0aa # 1st half of block
v2 = 0x8aeee7c8 # 2nd half of block

def ror(x, y):
    return ((x >> y) | (x << (32-y))) & 0xFFFFFFFF

state = [v2, v1]
for i in range(24):
    v2, v1 = state
    v2 = (v2 - constants[i] + 0x100000000) & 0xFFFFFFFF
    v2 = ror(v2, v1 & 0x1f)
    v0 = v1 ^ v2
    state = [v1, v0]
f2 = (state[0] - constants[24]) & 0xFFFFFFFF
f1 = (state[1] - constants[25]) & 0xFFFFFFFF

from pwn import *
print(p32(f1, endian='big') + p32(f2, endian='big'))

'''
blocks:
d4f5f0aa8aeee7c8
3cd8c039fabdee62
47d0f5f36edeb24f
f9d5bc10a1bd16c1
2699d29f54659267

TWCTF{Fat3_Gr4nd_Ord3r_1s_fuck1n6_h07}
'''
