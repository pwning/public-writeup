## RSAbaby - Crypto Challenge

The goal of this challenge is to decrypt an RSA message, given the following hints:
```
h = (d+p)^(d-p)
g = d*(p-0xdeadbeef)
```
where `d` and `p` are the usual RSA parameters, i.e. the private exponent and one prime factor of `n`.

Our solution (math due to @ThinerDAS) only makes use of `g`. Let `k = 0xdeadbeef`, and perform
the following computation to derive `p`:
```
m_pmc = pow(c, g, n)
m_epmc = pow(m_pmc, e, n)
m_ce = pow(c, k, n)
m_ep = m_ce * m_epmc
p = gcd(m_ep - c, n)
```

Using `p`, we simply compute `d` and decrypt the message. Full solution is in [solve.sage](solve.sage).
