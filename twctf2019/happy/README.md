# Happy!

This is a variant on `R u SAd?` from PlaidCTF 2019 :)
We have some modulus of the form `pq^k` for some natural `k` and primes `p`,`q`.
We also have the value of `cf = p^(q^(k-1) * (q-1) - 1) mod q^k` leaked since
the public key generation removes `ce` (which doesn't exist), not `cf`.

Note that `cf` should be the same order of magnitude as `q^k`. Since `cf`
is about `n^(2/3)`, we know that `k = 2`, as `n = pq^k`. Then
`cf = p^(q*(q-1) - 1) mod q^2`.

Note that `cf*p = p^(q*(q-1)) = p^(phi(q^2)) = 1 mod q^2` so
`cf = p^(-1) mod q^2`. We then have `cf * p^2 = p mod pq^2 = p mod n` so
`cf*x^2 - x mod n` should have a root at `x = p`.

We can do that with Sage's `small_roots()` (See [solve.sage](solve.sage).)
After recovering `p`, we can recover `q` and compute `d`. We then modified
the original Ruby script so we could generate a private key easily
(See [happy](happy), where we used fixed values for `p` and `q`).
