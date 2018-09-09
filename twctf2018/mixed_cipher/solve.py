from pwn import *
from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes
from mersennetwister import MT19937

BLOCK_SIZE = 16
def unpad(s):
    n = ord(s[-1])
    return s[:-n]

def aes_decrypt(s, aeskey):
    iv = s[:BLOCK_SIZE]
    aes = AES.new(aeskey, AES.MODE_CBC, iv)
    return unpad(aes.decrypt(s[BLOCK_SIZE:]))
    #return aes.decrypt(s[BLOCK_SIZE:])

def gcd(a, b):
    while b != 0:
        (a, b) = (b, a%b)
    return a

e = 65537

r = remote('crypto.chal.ctf.westerns.tokyo',5643)
#r = process('python2 server.py', shell=True)
print(r.recvuntil('encrypted key'))
r.recvline()

r.sendline('4')
r.recvline()
enc_key = int(r.recvline().strip(), 16)
r.recvuntil('encrypted key')
r.recvline()

r.sendline('1')
r.recvuntil(': ')
r.sendline('\x02')
n2 = int(r.recvline().strip().split()[-1],16)
r.recvuntil('encrypted key')
r.recvline()

r.sendline('1')
r.recvuntil(': ')
r.sendline('\x03')
n3 = int(r.recvline().strip().split()[-1],16)
r.recvuntil('encrypted key')
r.recvline()

r.sendline('1')
r.recvuntil(': ')
r.sendline('\x05')
n5 = int(r.recvline().strip().split()[-1],16)
r.recvuntil('encrypted key')
r.recvline()

r.sendline('1')
r.recvuntil(': ')
r.sendline('\x07')
n7 = int(r.recvline().strip().split()[-1],16)
r.recvuntil('encrypted key')
r.recvline()

N = gcd(gcd(gcd(pow(2, e) - n2, pow(3, e) - n3), pow(5, e) - n5), pow(7, e) - n7)
if N > 2 ** 1024:
    for i in [2,3,5,7,11]:
        if N % i == 0:
            N //= i

def lsb_oracle(t):
    r.sendline('2')
    t = hex(t)[2:]
    if t[-1] == 'L':
        t = t[:-1]
    if len(t) % 2 == 1:
        t = '0'+t
    r.sendline(t)
    r.recvline()
    x = int(r.recvline().strip().split()[-1],16)
    r.recvuntil('encrypted key')
    r.recvline()
    return x & 0xFF

LB = 0
UB = N
tmp = enc_key

last_byte = lsb_oracle(tmp) # ???

for i in range(1024-128-3):
    tmp = (tmp * pow(2, e, N)) % N
    UB = (UB + LB) / 2

# [LB, UB)
while True:
    tmp = (tmp * pow(2, e, N)) % N
    if lsb_oracle(tmp) & 1 == 0:
        print('got 0')
        UB = (UB + LB) / 2
    else:
        print('got 1')
        LB = (UB + LB) / 2
    print "diff", hex(UB - LB)[2:]
    print(hex((UB+LB)//2)[2:])
    if UB == LB:
        break
print(hex(last_byte))
aeskey = UB & (~0xFF)
aeskey += last_byte
aeskey = hex(aeskey)[2:]
aeskey = ('0'*(32-len(aeskey)) + aeskey).decode('hex')

vals = []

for i in range(624/4):
    print(i*4)
    r.sendline('1')
    r.recvuntil(': ')
    r.sendline('A')
    r.recvline()
    x = r.recvline().strip().split()[-1]
    for j in range(32,0,-8):
        vals.append(int(x[j-8:j],16))
    r.recvuntil('encrypted key')
    r.recvline()

print(vals)

n = MT19937()
n.seed_via_clone(vals)

r.sendline('3')
r.recvline()
r.recvline()
enc_flag = r.recvline().strip().decode('hex')
r.recvuntil('encrypted key')
r.recvline()

iv = ''
for i in range(4):
    iv = p32(n.next())[::-1] + iv
enc_flag = iv + enc_flag[16:]

print(iv.encode('hex'))

flag = aes_decrypt(enc_flag, aeskey)
print(repr(flag))

r.interactive()
