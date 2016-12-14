from AESCipher import *

from hashlib import sha256
from itertools import product
from string import printable

ciphertext = open('flag.encrypted', 'rb').read()
printable = printable[:-5]

password = ""
for i in range(4):
	print("round {}".format(i + 1))
	possibilities = []
	for i,j in product(range(256), repeat=2):
		c1, c2 = chr(i), chr(j)
		if c1 not in printable or c2 not in printable:
			continue
		key = sha256(chr(i) + chr(j)).digest()
		cipher = AESCipher(key)
		dec = cipher.decrypt(ciphertext)
		n = ord(dec[-1])
		if n < 32 and all(i == dec[-1] for i in dec[-n:]):
			print('padding length: {}'.format(n))
			possibilities.append((n, chr(i) + chr(j), dec))
	_, key, ciphertext = sorted(possibilities, reverse=True)[0]
	ciphertext = AESCipher._unpad(ciphertext)
	password = key + password
	print('found bytes: {}'.format(key))

with open('flag.dec', 'wb') as f:
	f.write(ciphertext)
print(password)
