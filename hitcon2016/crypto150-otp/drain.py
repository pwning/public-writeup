import pwnlib
import struct
import hashlib
import subprocess
from binascii import unhexlify, hexlify
from math import log

#entropyH = 6175-38
#entropyH = 20000
#entropyL = 500
L = 600
method = 3
flaglen = 37


def strxor(a, b):
	return "".join([chr(ord(a[i])^ord(b[i])) for i in range(min(len(a), len(b)))])

def get_entropy(s):
	dct = {}
	nums = float(len(s))
	for i in s:
		if i not in dct:
			dct[i] = 0
		dct[i] += 1
	total = 0
	for k in dct:
		total -= (dct[k]/(nums) * log(dct[k]/(nums))) 
	return total

def hx(value):
	outstr = hex(value)[2:]
	outstr = "0" * (8-len(outstr)) + outstr
	return outstr

def drain(ent, meth, suffix = ""):
	#tube = pwnlib.tubes.remote.remote("52.198.182.219", 50216)
	tube = pwnlib.tubes.process.process("./hint")
	tube.recvuntil(">")
	tube.sendline("2")
	tube.recvuntil(">")
	tube.sendline(str(meth))
	tube.recvuntil(">")
	tube.sendline("1")
	tube.recvuntil("len?")
	tube.sendline(str(ent))
	tube.recvuntil("data?")
	tube.send("a"*(ent))
	print tube.recvuntil("content:")
	data = tube.recv(timeout=2)
	while True:
		try:
			data += tube.recv(timeout=2)
		except:
			break
	dataS = unhexlify(data[1:-1])
	random = strxor(dataS, ("a"*ent+suffix))
	(h0, h1, h2, h3, h4) = struct.unpack("IIIII", random[L-40:L-20])
	randhasher = random[L-40:L-20]+random[:44]
	res = subprocess.check_output(["./sha1", hex(h0)[2:], hex(h1)[2:], hex(h2)[2:], hex(h3)[2:], hex(h4)[2:], hexlify(randhasher)])
	print len(res)
	(v0, v1, v2, v3, v4) = struct.unpack("<IIIII", unhexlify(res[:-1]))
	outstr =  hx(v0) + hx(v1) + hx(v2) + hx(v3) + hx(v4)
	usable_res = unhexlify(outstr)
	output = strxor(usable_res, dataS[L-20:L]) 
	#assert len(dataS) == ent+flaglen+len(suffix)
	#assert len(random) == ent+len(suffix)
	#assert len(randhasher) == 64
	print "Data: "+hexlify(dataS)
	print ""
	print "Init Vals: {:02x} {:02x} {:02x} {:02x} {:02x}".format(h0, h1, h2, h3, h4)
	print "Res: "+hexlify(usable_res)
	print "Hashing: "+hexlify(randhasher)
	print "Extracted: "+output
	print "Ent: {}, Method: {}, Entropy: {}".format(ent, meth, str(get_entropy(random))) 
	return output

piece1 = drain(L-20, method)
piece2 = drain(L-37, method, piece1)

print "got {}{}".format(piece1[:17], piece2)

"""
for i in range(1,5):
	drain(entropyL, i)
	drain(entropyH, i)
"""
