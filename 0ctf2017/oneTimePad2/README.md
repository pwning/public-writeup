## oneTimePad2 - Crypto Challenge

We're given ciphertext and the script that generated it.

`process1(m,k)` in the script returns `(m*k)**2`, where `m` and `k` are
(integer representations of) elements in `GF(2**128)` defined by the polynomial
`P`.

`process2(a,b)` in the script returns `a*b` where `a` and `b` are 2x2 matrices
defined over the field.

`nextrand(rand)` in the script returns `newrand`, where
`[[newrand],[1]] = [[A,B],[0,1]]**N * [[rand],[1]]`, and `A`, `B` are known
values, and sets `N` to `N**2` treating `N` as an element of the field.

We can also calculate `r1` and `r2 = nextrand(r1)` from the ciphertext and
partial plaintext (where `[[r2],[1]] = [[A,B],[0,1]]**N * [[r1],[1]]`),
and the goal is to recover `N`, so we can decrypt the
remaining ciphertext.

Note that the matrix `[[A,B],[0,1]]` is diagonalizable, so we can decompose it
as `P * D * P**-1`, where `D` is a diagonal matrix and `P` is invertible.
Note also that `(P * D * P**-1)**N = P * D**N * P**-1`, and `D**N` can be
calculate by taking each of the diagonal entries to the `N`th power.

Then, we have:
```
[[r2],[1]] = (P * D * P**-1)**N * [[r1],[1]] = P * D**N * P**-1 * [[r1],[1]]
P**-1 * [[r2],[1]] = D**N * (P**-1 * [[r1],[1]])
```

This means that we can reduce the problem to a discrete-log problem involving
only one of the diagonal entries of `D`.

Final code in [solve.sage](solve.sage).

```
flag{LCG1sN3ver5aFe!!}
```
