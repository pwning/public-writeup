F = GF(2^128, 'z', modulus=x^128 + x^7 + x^2 + x + 1)
P = 0x100000000000000000000000000000087
A = 0xc6a5777f4dc639d7d1a50d6521e79bfd
B = 0x2e18716441db24baf79ff92393735345

def num2poly(n):
    return F.fetch_int(n)

def poly2num(p):
    return p.integer_representation()

def str2num(s):
    return int(s.encode('hex'), 16)

def process1(m, k): # m * k
    res = 0
    for i in bin(k)[2:]:
        res = res << 1;
        if (int(i)):
            res = res ^ m
        if (res >> 128):
            res = res ^ P
    return res

def process2(a, b): # matrix mult
    res = []
    res.append(process1(a[0], b[0]) ^ process1(a[1], b[2]))
    res.append(process1(a[0], b[1]) ^ process1(a[1], b[3]))
    res.append(process1(a[2], b[0]) ^ process1(a[3], b[2]))
    res.append(process1(a[2], b[1]) ^ process1(a[3], b[3]))
    return res

def nextrand(c):
    # [[newrand],[1]] = [[A,B],[0,1]]^N * [[rand],[1]]; N = N^2
    # P^-1 * [[newrand],[1]] = [[1,0],[0,d^N]] * P^-1 * [[rand],[1]]
    global N, A, B
    tmp1 = [1, 0, 0, 1] # id matrix
    tmp2 = [A, B, 0, 1] # [[A,B],[0,1]]
    s = N
    N = process1(N, N) # N = N^2
    while s:
        if s % 2:
            tmp1 = process2(tmp2, tmp1)
        tmp2 = process2(tmp2, tmp2)
        s = s / 2
    return process1(rand, tmp1[0]) ^ tmp1[1]

c = [i.decode('hex') for i in ['0da8e9e84a99d24d0f788c716ef9e99c',
'c447c3cf12c716206dee92b9ce591dc0',
'722d42462918621120ece68ac64e493a',
'41ea3a70dd7fe2b1d116ac48f08dbf2b',
'26bd63834fa5b4cb75e3c60d49676092',
'1b91df5e5e631e8e9e50c9d80350249c']]

p = ["One-Time Pad is ",
"used here. You w",
"on't know that t",
"he flag is flag{"]

r1 = num2poly(str2num(c[0]) ^^ str2num(p[0]))
r2 = num2poly(str2num(c[1]) ^^ str2num(p[1]))

M = matrix([[num2poly(A), num2poly(B)],[0,1]])
D,P = M.eigenmatrix_right()
assert P * D * P.inverse() == M
d = D[1][1]

a2 = (P.inverse() * vector([r2, 1]))[1]
a1 = (P.inverse() * vector([r1, 1]))[1]
# N = (a2/a1).log(d)

N = 76716889654539547639031458229653027958
N = poly2num(num2poly(N)*num2poly(N))
N = poly2num(num2poly(N)*num2poly(N))
N = poly2num(num2poly(N)*num2poly(N))
r4 = ((M^N) * vector([num2poly(str2num(c[3]) ^^ str2num(p[3])),1]))[0]
print(hex(str2num(c[4]) ^^ poly2num(r4))[2:-1].decode('hex'))
N = poly2num(num2poly(N)*num2poly(N))
r5 = ((M^N) * vector([r4,1]))[0]
print(hex(str2num(c[5]) ^^ poly2num(r5))[2:-1].decode('hex'))
