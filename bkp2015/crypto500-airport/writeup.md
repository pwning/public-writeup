## Airport - Crypto 500 Problem - Writeup by Robert Xiao (@nneonneo)

The hint for the problem says

> The timing in this challenge is clearly not very realistic---but the methods you'll use here can be extended to real-world implementations of modular exponentiation.

Opening up the package, we see that they have implemented a simple modular exponentiation algorithm which takes your input `b` and computes `b^e % m` for a randomly-generated, secret exponent `e` and a large safe prime `m`. The obvious change here is that the square-and-multiply exponentiation algorithm, aptly named `slowpower`, pauses for one full second any time an intermediate result is equal to 4.

Clearly, the expected solution is to use the one-second delay to extract the exponent. A partial result at step `k` is given as `b^e[:k] % m`, where `e[:k]` denotes the number formed by taking the first `k` bits of `e`. Note that if we know `e[:k-1]`, there are only two possibilities for `e[:k]`: `e[:k-1] * 2` (if the `k`th bit is 0) or `e[:k-1] * 2 + 1` (if the `k`th bit is 1). So, if we know `e[:k-1]`, we can input some `b` such that `b^(e[:k-1]*2+1) % m == 4`. If we see a 1 second delay, we know that the kth bit is a 1; otherwise, the kth bit must be 0.

Thus, we can extract the secret one bit at a time. All that's left to do is compute a suitable `b` at each stage. Luckily, their use of a safe prime makes this very easy: the modulus `m` is prime, and equal to `2q+1` where `q` is also a prime.

The goal here is to find a `b` such that `b^r == 4` for a given exponent `r`, i.e. to take the `r`th root mod `m = 2*q+1`. Let `s` be such that `r*s = 1 mod 2q` (we're assuming such an `s` exists). Then, by Fermat's Little Theorem, `b == b^(rs) == 4^s` mod `m`. For `s` to exist, we note that `r` must be odd because it must invert `s` mod `2q` -- hence why we chose to check the `e[:k-1]*2+1` case up above. To compute `s`, we can simply apply Euler's Theorem: `s = r^(q-2)` mod `2q`.

Finally, we did a few things to make the attack more reliable - very important because the attack takes anywhere from 20 to 40 minutes to run. You can see the full details in the `attack.py` script.
