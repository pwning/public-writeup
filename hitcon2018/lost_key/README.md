# Lost Key

## Description

> Crypto

I lost my public key. Can you find it for me?

```
nc 18.179.251.168 21700

```

[rsa-b667a9ca0d5c6735e5609565d1fd6ab9.py](./rsa-b667a9ca0d5c6735e5609565d1fd6ab9.py)

## Writeup

The server script implements RSA,
and exposes the ability to perform some queries.

It first does key generation by choosing two random 512-bit primes and then picking a random public exponent.

Once that is done, it encrypts the flag and sends it to us, and then
exposes the ability to perform a maximum of 150 queries. These
queries can be one of two kinds `A` or `B`:

+ `A`: Encrypt arbitrary input
+ `B`: Decrypt arbitrary input, but only receive the least significant
		_byte_.

At this point things seemed fairly similar to the [Lost Modulus](../lost_modulus/README.md) challenge. 

Since we have the encrypted flag (which we'll call `flag_enc`), and we
have a lsB (least significant _byte_) decryption oracle (query `B`),
we can easily obtain the least significant byte of the flag. If we
know `enc(modinv(256, N))` (where `N` is the public key), we can multiply
the encrypted flag by successive powers of this number, subtracting previous 
results, and so obtain the flag one byte at a time.

However, we are not provided `N` by the server! At first we briefly thought
using the same technique we applied to Lost Modulus. But the number of
attempts we're allowed here is quite small, and certainly not enough
to do binary search to find the public key. But RSA ciphertexts, unlike
Paillier ciphertexts, carry around quite a few relations.

In particular, suppose we choose two numbers `x` and `y` (ideally relatively 
prime). Then we can compute the ciphertexts `u = enc(x)` and `v = enc(y)`.
And then we can compute the ciphertexts `u' = enc(x * x)` and `v' = enc(y * y)`.
But then, since RSA is multiplicatively homomorphic, we know that 
`u * u = u' (mod N)` and `v * v = v' (mod N)`. Then we know that
`u * u - u'` and `v * v - v'` must both be multiples of `N`.

So we can compute `N' = gcd(u * u - u', v * v - v')`. However, odds are that
there are other common factors beyond `N`, likely powers of small primes. So 
we also divide `N'` by a handful of small primes until it's relatively prime
to all of them, at which point we can be fairly confident we've found `N`.

This allows us to compute `N` using 4 total queries, and then we can use the 
remainder of our queries to fetch the flag.

Here's our [script](./solution.py) implementing this attack. It outputs a
hex string which, once-decoded, contains the flag. 

## Flag

```
hitcon{1east_4ign1f1cant_BYTE_0racle_is_m0re_pow3rfu1!}
```
