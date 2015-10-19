## rsabin - Crypto 314 Problem - Writeup by Robert Xiao (@nneonneo)

### Description

> Classical things?
> 
> rsabin-a51076632142e074947b08396bf35ab2.tgz

### Solution

We are given the flag encrypted with naïve RSA, with a 314-bit modulus and the unusual exponent 31415926535897932384. Furthermore, looking carefully we can see that the flag is 50 bytes (400 bits), which is *greater* than the modulus size. Therefore, some information has been lost in the encryption process.

The first step is to factor the modulus. cado-nfs works well for this, factoring the number in less than half an hour on my laptop. The primes are

    p = 123722643358410276082662590855480232574295213977
    q = 164184701914508585475304431352949988726937945291

Now, `gcd(e, (p-1)*(q-1)) == 16` and so `e` is *not* invertible. We can use the *pseudoinverse* `d` of `e` mod `(p-1)*(q-1)`, a number such that `c**d == m**(d*e) === m**16` mod n. To get the value of `m` mod n, we will have to compute the 16th root of `c**d`, and there are 16 such roots.

If we know `m` mod n, we still have to recover the flag by finding the 86 missing bits. We assume that the flag is formatted normally, i.e. as `hitcon{...}`, which gives us 64 bits, and then bruteforce for the remaining 22 bits, which is completely feasible. The valid flag presumably contains only printable characters.

The attached `solve.py` script implements this attack. It uses [Eli Bendersky's `modular_sqrt` function](http://eli.thegreenplace.net/2009/03/07/computing-modular-square-roots-in-python) to compute 16th roots of `c**d`, and tries the bruteforce for each root. After about 5 minutes, spits out the flag:

    hitcon{Congratz~~! Let's eat an apple pi <3.14159}
