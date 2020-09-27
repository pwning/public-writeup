import random

with open('output.txt') as f:
    ct = int(f.readline())
    p = int(f.readline())

assert(p % (1 << 30) == 1)
q = (p-1)//(1 << 30)
e = 30
assert(q & 1)

#We want to inverse 2^64 mod p-1, but because 2^30|p-1 we can only reduce it to m^2^30
inv = pow(2,-34,q)
m_2_30 = pow(ct, inv, p)
print("m^(2^30):",m_2_30)

#Finds a 2^30th root of unity mod p probabalistically (We also verify that the order does not divide 2^29, so order is actually 2^30).
for i in range(100):
    rou_2_30 = pow(i, q, p)

    if pow(rou_2_30, 1 << 29, p) > 1:
        print("Root Of Unity:",rou_2_30)
        break

#Square Root mod certain primes (1 mod 4 or something) I found on the internet
z = 1
while pow(z, 1 << 29, p) == 1:
    x = random.randint(2, 10000)
    z = pow(x, q, p)
def sqrt(a):
    y = z
    r = e
    x = pow(a, (q-1)//2, p)
    v = (a * x) % p
    w = (v * x) % p

    while w != 1:
        for k in range(1,100):
            if pow(w, 1 << k, p) == 1:
                break
        d = pow(y, 1 << (r-k-1),p)
        y = (d * d) % p
        r = k
        v = (d * v) % p
        w = (w * y) % p

    assert((v * v) % p == a)
    return v

#We can just take an arbitrary square root 30 times, to generate one possible message value that works.
m_1 = m_2_30
for _ in range(30):
    m_1 = sqrt(m_1)
assert(pow(m_1, 1 << 30, p) == m_2_30)
print("M Possibility:",m_1)


assert(pow(m_1, 1 << 64, p) == ct)
lower = 0
upper = 100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
count = 0
#Find all multiple messages by multiplying by square roots of unity, and seeing which ones are small enough to be the flag
#This generates all possible numbers such that m'^(2^30) = m^(2^30), so the flag must be one of these numbers
while True:
    if lower <= m_1 <= upper:
        print(m_1) #Decode the output for flag!
    m_1 *= rou_2_30
    m_1 %= p
    count += 1
    if count % 1000000 == 0:
        print(count, pow(m_1, 1 << 64, p) - ct)
