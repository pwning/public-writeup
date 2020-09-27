from Crypto.Util.number import bytes_to_long, isPrime
from secret import flag, p


def encrypt(m, k, p):
    return pow(m, 1 << k, p)


assert flag.startswith("TWCTF{")
assert len(flag) == 42
assert isPrime(p)

k = 64
pt = bytes_to_long(flag.encode())
ct = encrypt(pt, k, p)

with open("output.txt", "w") as f:
    f.write(str(ct) + "\n")
    f.write(str(p) + "\n")
