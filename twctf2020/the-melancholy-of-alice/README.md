# The Melancholy of Alice

Crypto, Score: 242, Solved by 36 teams

Writeup by @f0xtr0t; solved by @clam, @DilhanSalgado, @f0xtr0t

## Problem

Carol "That's classified information."
[melancholy.7z](./melancholy-4a8a124513bc5c57755d523167606710fe0f68d66f46cc93ccc8966713da3f01.7z)

## Solution

In this challenge, we are given 3 files:
[`encrypt.py`](./melancholy/encrypt.py),
[`ciphertext.txt`](./melancholy/ciphertext.txt) and
[`publickey.txt`](./melancholy/publickey.txt), where the two `.txt`
files have been produced from `encrypt.py`, which is an implementation
of the [ElGamal
encryption](https://en.wikipedia.org/wiki/ElGamal_encryption)
scheme. However, it decides to encrypt each character of the plaintext
(flag) separately, rather than encrypting the plaintext as a whole. We
abuse this in our solution. Additionally, we abuse the fact that `q`
(explained below) has a few small factors.

In short, the public key consists of the numbers `p`, `q`, `g`, and
`h`, and the private key consists of the number `x` where
  * `p` is a (strong) prime
  * `q == (p-1)/2`
  * `x` is a random value between 2 and `q`
  * `h == g^x (mod p)`

The encryption consists of picking a random number `r` between 2 and
`q` and computing `c1` and `c2` from the message `m` where
  * `c1 == g^r (mod p)`
  * `c2 == m * h^r (mod p)`

Looking at the values that we have for the public key, we notice that
`q` has a few small factors, namely 3, 5, and 19. We'll use these,
along with 2 as our list of primes that we'll identify the message
results with.

In particular, we find the `n`th-power residue (see [Quadratic
residue](https://en.wikipedia.org/wiki/Quadratic_residue)) as an
"identifier" to figure out which character has been used in the
message. Here, `n` is in the list [2, 3, 5, 19]. For this, we compute
the `n`th-power generalization of the [Legendre
Symbol](https://en.wikipedia.org/wiki/Legendre_symbol). That is, we
compute `x^((p-1)/n) (mod p)` for each of these `n` and use it as an
identifier.

We know that the flag _must_ start with `TWCTF{` and this gives us the
relationship between `g` and `h` for the modification of the symbol
for each such `n`. We can thus use this to compute back the symbols
for each `m`. By performing an inverse lookup of this identifier, to
the list of all printable characters, we can identify equivalence
classes that can then be manually analyzed to give the flag.

More details in our solve script: [solve script](./solve.py) or
[alternate solve script](./solve_alternate.py)
