# Lost Modulus Again

We're given an RSA key with `e`, `d`, `x = p^(-1) mod q`, and `y = q^(-1) mod p`,
but no modulus.

Note that we have `ed = 1 + k*phi(n)` for some `1 <= k <= e`, so we can brute
force all possible values of `k` to get `phi(n)`.

We also have the relation `(x-1)*q + (y-1)*p = phi(n)` since `x*q + y*p = n+1`.

Then we have `(y-1)*p = phi(n) mod (x-1)`, and we know `x-1` and `y-1`, so we
can recover `p mod (x-1)`. One small problem is that `x-1` and `y-1` are not
relatively prime, so we will have multiple candidates for `p`, but we can try
all of them out.

Similarly, we can recover `q mod (y-1)`. Since `x` and `y` are around `p/2` and
`q/2`, we don't have to add too many multiples of `x-1` or `y-1` to recover
`p` and `q`.

Once we have `p` and `q`, we can recover `n = pq` and decrypt the flag.

Solve script in [solve.sage](solve.sage).
