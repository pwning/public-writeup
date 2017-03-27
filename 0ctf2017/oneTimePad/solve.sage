fake_secret1 = "I_am_not_a_secret_so_you_know_me"
fake_secret2 = "feeddeadbeefcafefeeddeadbeefcafe"

F = GF(2^256, 'z', modulus=x^256 + x^10 + x^5 + x^2 + 1)

def num2poly(n):
    return F.fetch_int(n)

def poly2num(p):
    return p.integer_representation()

def str2num(s):
    return int(s.encode('hex'), 16)

nc1,nc2,nc3 = [int(i,16) for i in open('ciphertext').read().strip().split()]

c2 = num2poly(str2num(fake_secret1)^^nc2)
c3 = num2poly(str2num(fake_secret2)^^nc3)

seed = c3.sqrt()-c2

print("flag{"+hex(Integer(poly2num(c2.sqrt()-seed)^^nc1)).decode('hex')+"}")
