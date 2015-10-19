# Thank you based CADO-NFS - 1600 seconds to factor this.
p = 123722643358410276082662590855480232574295213977
q = 164184701914508585475304431352949988726937945291

n = 20313365319875646582924758840260496108941009482470626789052986536609343163264552626895564532307
e = 31415926535897932384
c = 19103602508342401901122269279664114182748999577286972038123073823905007006697188423804611222902

from Crypto.Util.number import inverse, isPrime, bytes_to_long, long_to_bytes

assert p*q == n

assert isPrime(p)
assert isPrime(q)

from sqrt import modular_sqrt

def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a*b, n)
 
    for n_i, a_i in zip(n, a):
        p = prod / n_i
        sum += a_i * inverse(p, n_i) * p
    return sum % prod

def power2roots(a, k):
    if k == 0:
        yield a
        return
    for i in power2roots(a, k-1):
        s1 = modular_sqrt(i, p)
        s2 = modular_sqrt(i, q)
        if s1 and s2:
            yield chinese_remainder([p, q], [s1, s2])
            yield chinese_remainder([p, q], [p-s1, s2])
            yield chinese_remainder([p, q], [s1, q-s2])
            yield chinese_remainder([p, q], [p-s1, q-s2])

# This is a *pseudoinverse* since gcd(e, (p-1)*(q-1)) == 16.
d = inverse(e, (p-1) * (q-1))

for m in reversed(list(power2roots(pow(c, d, n), 4))):
    assert pow(m, e, n) == c

    # OH NO! They left out a bunch of bits :(
    flagfmt = 'hitcon{' + ' '*42 + '}'
    assert len(flagfmt) == 50
    curm = bytes_to_long(flagfmt) // n * n + m
    while curm % 256 != ord('}'):
        curm += n

    assert curm % n == m
    assert pow(curm, e, n) == c

    import re
    valid_flag_re = re.compile(r'^[\x20-\x7e]+$')

    increment = n * 256 # leave the last byte (}) unchanged
    for i in xrange(1000000000):
        s = long_to_bytes(curm, 50)
        if s > 'hitcon{\x7f':
            break
        if valid_flag_re.match(s):
            print i, repr(s)
        if i % 10000 == 0:
            print i, repr(s[:10])

        curm += increment

# hitcon{Congratz~~! Let's eat an apple pi <3.14159}
