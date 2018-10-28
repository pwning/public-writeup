from Crypto.Util.number import *
from gmpy import *
from random import *
import sys,os

from math import floor, sqrt

from pwn import *

NUM_BITS = 1024

# s = process(['python', 'rsa.py'])
s = remote('18.179.251.168', 21700)
print s.recvline().strip()
raw = s.recvline().strip()
flag_encryption = bytes_to_long(raw.decode('hex'))
print flag_encryption

def cmd(t, v):
  print s.recv(),
  print t
  s.send(t + '\n')
  print s.recv(),
  print long_to_bytes(v).encode('hex')
  s.send(long_to_bytes(v).encode('hex') + '\n')
  return bytes_to_long(s.recvline().strip().decode('hex'))

# server-encrypt
def senc(v):
  return cmd('A', v)
# server-decrypt
def sdec(v):
  return cmd('B', v)

# Nothing special about these numbers, they're randomly chosen
msgA = 1<<512
msgB = 185919581
c1 = senc(msgA)
c2 = senc(msgB)
c1a = senc(msgA * msgA)
c2a = senc(msgB * msgB)
N = gcd(c1 * c1 - c1a, c2 * c2 - c2a)
print "got", N
small_primes = set([2, 3, 5, 7, 11, 13])
while any(N % p == 0 for p in small_primes):
  for p in small_primes:
    if N % p == 0:
      N = N / p

print "actual N", N
inv = senc(invert(256, N))
print "got inverse", inv
flag_bytes = []
for k in xrange(128):
  accum = (sum(flag_bytes[k] * pow(invert(256, N), len(flag_bytes)-k, N) for k in xrange(len(flag_bytes))) % N) % 256
  flag_bytes.append((sdec(flag_encryption) - accum) % 256)
  flag_encryption = (flag_encryption * inv) % N
print ''.join(map(chr, flag_bytes[::-1])).encode('hex')

