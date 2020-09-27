from Crypto.Util.number import getStrongPrime, getRandomRange

N = 1024


def generateKey():
    p = getStrongPrime(N)
    q = (p - 1) // 2
    x = getRandomRange(2, q)
    g = 2
    h = pow(g, x, p)
    pk = (p, q, g, h)
    sk = x
    return (pk, sk)


def encrypt(m, pk):
    (p, q, g, h) = pk
    r = getRandomRange(2, q)
    c1 = pow(g, r, p)
    c2 = m * pow(h, r, p) % p
    return (c1, c2)


def main():
    with open("flag.txt") as f:
        flag = f.read().strip()

    pk, sk = generateKey()
    with open("publickey.txt", "w") as f:
        f.write(f"p = {pk[0]}\n")
        f.write(f"q = {pk[1]}\n")
        f.write(f"g = {pk[2]}\n")
        f.write(f"h = {pk[3]}\n")

    with open("ciphertext.txt", "w") as f:
        for m in flag:
            c = encrypt(ord(m), pk)
            f.write(f"{c}\n")


if __name__ == "__main__":
    main()
