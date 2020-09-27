exec(open("./publickey.txt").read())
ct = [eval(line) for line in open("./ciphertext.txt")]

known = b"TWCTF{"

facs = [2,3,5,19]

def canon_indexn(n, m):
	assert (p - 1) % n == 0
	lift = pow(m, (p - 1) // n, p)
	root = pow(g, (p - 1) // n, p)
	for i in range(n):
		if lift % p == 1:
			return i
		lift *= root
	assert False

crts = []
for f in facs:
	for x in range(f):
		for (gr, cgrx), c in zip(ct, known):
			grx1 = cgrx * pow(c, -1, p) % p
			grx2 = pow(gr, x, p)
			if canon_indexn(f, grx1) != canon_indexn(f, grx2):
				break
		else:
			print(f"x % {f} == {x}")
			crts += [(f, x)]
			break

x = 0
while True:
	for m, n in crts:
		if x % m != n: break
	else: break
	x += 1

print(f"x = {x}")

import string
from collections import defaultdict

print('precomputing...')
d = defaultdict(list)
for c in string.printable.encode():
	d[tuple(canon_indexn(f, c) for f in facs)] += [c]

print('flag:')
cands = []
for (gr, cgrx) in ct:
	grx = pow(gr, x, p)
	key = tuple((canon_indexn(f, cgrx) - canon_indexn(f, grx)) % f for f in facs)
	cs = d[key]
	cands += [cs]
	print(bytes(cs))
