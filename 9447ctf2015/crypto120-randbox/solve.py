import socket
import telnetlib

s = socket.create_connection(('randBox-iw8w3ae3.9447.plumbing', 9447))

def read_until(st):
  buf = ''
  while st not in buf:
    buf += s.recv(1)
  print buf
  return buf

#addition, round 1
read_until("encrypts to '")
enc = read_until("'")[:-1]
s.send("0\n")
read_until("\n")
read_until("\n")
key = read_until("\n")

dec = ''.join(["%x"%( (int(c, 16) - int(key, 16))&0xf ) for c in enc])
s.send(dec +"\n")

#next round is permutation of some sort, round 2
#this was written to handle arbitrary bytewise permutation
#it turns out the server actually did nibble-wise rotation
#so this was both under-kill and over-kill
#this will fail with 1/2 probability, so you may need to run
#this script several times
read_until("encrypts to '")
enc = read_until("'")[:-1]
s.send("000102030405060708090a0b0c0d0e0f"+"\n")
read_until("\n")
read_until("\n")
p1 = read_until("\n")[:-1]

perm = map(ord,p1.decode("hex"))
print 'permutation',perm
print enc

dec = [0 for _ in xrange(16)]
for i, idx in enumerate(perm):
  dec[idx] = enc[2*i:2*i+2]

dec = ''.join(dec)
print dec

s.send(dec + "\n")

#now xor? round 3
read_until("encrypts to '")
enc = read_until("'")[:-1]
s.send("0"+"\n")
read_until("\n")
read_until("\n")
key = read_until("\n")

print enc, key

dec = ''.join(["%x"%( (int(c, 16) ^ int(key, 16))&0xf ) for c in enc])
print dec
s.send(dec +"\n")

#addition? round 4 
read_until("encrypts to '")
enc = read_until("'")[:-1]
s.send("0\n")
read_until("\n")
read_until("\n")
key = read_until("\n")

dec = ''.join(["%x"%( (int(c, 16) - int(key, 16))&0xf ) for c in enc])
s.send(dec +"\n")

#xor again? round 5 
read_until("encrypts to '")
enc = read_until("'")[:-1]
s.send("0\n")
read_until("\n")
read_until("\n")
key = read_until("\n")

dec = ''.join(["%x"%( (int(c, 16) ^ int(key, 16))&0xf ) for c in enc])
s.send(dec +"\n")

#long addition, round 6
read_until("encrypts to '")
enc = read_until("'")[:-1]
s.send("0"*32+"\n")
read_until("\n")
read_until("\n")
key = read_until("\n")

dec = ''.join(["%x"%( (int(c, 16) - int(key[i&0x1f], 16))&0xf ) for i,c in enumerate(enc)])
s.send(dec +"\n")


#lolcbc, round 7
read_until("encrypts to '")
enc = read_until("'")[:-1]

s.send("0"+"\n")
read_until("\n")
read_until("\n")
iv = int(read_until("\n")[:-1], 16)

dec = ''
for i in xrange(32):
  dec += "%x"%( (iv ^ int(enc[i], 16))&0xf )
  iv = int(enc[i], 16)^iv

s.send(dec +"\n")

#lolcbc, round 8
read_until("encrypts to '")
enc = read_until("'")[:-1]

s.send("0"+"\n")
read_until("\n")
read_until("\n")
iv = int(read_until("\n")[:-1], 16)

dec = ''
for i in xrange(32):
  dec += "%x"%( (int(enc[i], 16) - iv)&0xf )
  iv = int(enc[i], 16)

s.send(dec +"\n")

#lolcbc, round 9
read_until("encrypts to '")
enc = read_until("'")[:-1]

s.send("0"+"\n")
read_until("\n")
read_until("\n")
iv = int(read_until("\n")[:-1], 16)

dec = ''
for i in xrange(32):
  dec += "%x"%( (iv ^ int(enc[i], 16))&0xf )
  iv = int(enc[i], 16)^iv

s.send(dec +"\n")

#xor + endiannes flip, round 10
read_until("encrypts to '")
enc = read_until("'")[:-1]

def ee(x):
  return chr((x>>4) | ((x&0xf) << 4))


s.send("00"+"\n")

read_until("\n")
read_until("\n")
key = read_until("\n")[:-1]

dec = ''.join([ee(ord(c)^ord(key.decode("hex"))) for c in enc.decode("hex")])
s.send(dec.encode("hex") +"\n")

t = telnetlib.Telnet()
t.sock = s
t.interact()
