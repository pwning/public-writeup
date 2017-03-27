## oneTimePad - Crypto Challenge

We're given ciphertext and the script that generated it.

`process(m,k)` in the script returns `(m+k)**2`, where `m` and `k` are
(integer representations of) elements in `GF(2**256)` defined by the polynomial
`P`.

We're also given `c1 = flag^key`, `c2 = f1^process(key,seed) = f1^(key+seed)**2`,
and `c3 = f2^process(process(key,seed),seed) = f2^((key+seed)**2 + seed)**2` in
the ciphertext, where `f2` and `f3` are known values.

To recover `seed`, we calculate `(c3^f2).sqrt() - (c2^f1)`.

Then, to get the flag, we calculate `c1 ^ ((c2^f1).sqrt()-seed)`.

Final code in [solve.sage](solve.sage).

```
flag{t0_B3_r4ndoM_en0Ugh_1s_nec3s5arY}
```
