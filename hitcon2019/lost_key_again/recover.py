from pwn import *
from Crypto.Util.number import *

nn = []

r = remote('3.115.26.78', 31337)
print(r.recvline())
for i in range(30):
    print(i)
    data = chr(i).encode('hex')
    r.recvuntil('give me your X value: ')
    r.sendline(data)
    y = bytes_to_long(r.recvline().strip().decode('hex'))
    r.recvuntil('give me your X value: ')
    data = chr(i).encode('hex')
    r.sendline(data + '00')
    yx = bytes_to_long(r.recvline().strip().decode('hex'))
    r.recvuntil('give me your X value: ')
    data = chr(i).encode('hex')
    r.sendline(data + '0000')
    yxx = bytes_to_long(r.recvline().strip().decode('hex'))
    nn.append(y*yxx - yx*yx)

from sage.all import gcd
print("n = {}".format(gcd(nn)))
