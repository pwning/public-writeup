from Crypto.PublicKey import RSA
r = RSA.importKey(open("publickey.pem").read())
print(r)
print(r.n)

n = r.n
e = 65537

R.<x> = PolynomialRing(ZZ, 'x')

for k in range(2,e):
    poly = k*x*x + x - n*e
    if poly.roots() != []:
        p = poly.roots()[0][0]
        q = ZZ(n/p)
        assert p*q == n
        print(p)
        print(q)
        print(k, poly.roots())
