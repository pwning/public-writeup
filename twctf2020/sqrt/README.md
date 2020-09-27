# sqrt

Crypto, Score: 216, solved by 45 teams

Writeup by @f0xtr0t; solved by @f0xtr0t, @DilhanSalgado

## Problem

[sqrt.7z](./sqrt-20758716979865e7d93c1617585d9f1fb7fc0284ae16044d967462edc6366eb7.7z)

## Solution

The provided file contains [`chall.py`](./chall.py) and
[`output.txt`](./output.txt) generated from it.

The challenge simply takes the `2^64`th power of the flag, modulo a
large prime `p`, and provides us this result (along with `p`).

The solution thus must "simply" perform 64 modular square-roots to
find the flag. This is easier said than done, because there exist
multiple values that have the property of `m^(1<<64) == ct`. Thus, we
need to find the right one, such that it is an ASCII encoding of a 42
character string starting with `TWCTF{` (constraints provided in
`chall.py`).

First we use the [Tonell-Shanks
Algorithm](https://en.wikipedia.org/wiki/Tonelli%E2%80%93Shanks_algorithm)
to find one such `m`. This gives us a point to start off from. If we
can multiply this with a non-unit value whose `2^64`th power is a
unit, we can find the other values of `m` that satisfy the same
property. Since `p-1` is `2^30 * q` where `q` is prime, we can find
the `2^30`th root of unity (which is then no longer a quadratic
residue, and thus cannot be square-rooted further). We do this by
performing repeated square-roots of `p-1` (since `(p-1)^2 == 1 (mod
p)`). This gives us a value `k`.

Now, we can find all the 2^30 values `m * k^r (mod p)` (where `r`
ranges from 0 to 2^30) to find a value that satisfies the required
`TWCTF{` prefix, since all of them satisfy the ciphertext.

Solve script for finding `m` and `k`:
[`solve_initial.py`](./solve_initial.py). Solve script to find the
right `r` to satisfy constraints (parallelized via Rust for _speed_):
[`solve_constr.rs`](./solve_constr.rs).

Alternate annotated solve script: [`solve.py`](./solve.py)
