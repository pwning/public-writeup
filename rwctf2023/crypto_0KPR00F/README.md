# 0KPR00F

_Writeup by [@f0xtr0t](https://github.com/jaybosamiya)_

Crypto, 97 points, solved by 54 teams

[Solve script](./solv.py) if you just want to dive in.

## Challenge Summary

This challenge takes [`py_pairing`](https://github.com/ethereum/py_pairing),
with no changes, and adds the file [`task.py`](./task.py) to it.

`task.py` sets up a server that provides some values to the user, `PKC` and
`PKCa` and the user is expected to find 3 values `PiC`, `PiCa`, and `PiH` that
satisfy certain constraints. These constraints are related to [elliptic curve
pairings](https://medium.com/@VitalikButerin/exploring-elliptic-curve-pairings-c73c1864e627).

The specific values `PKC` and `PKCa` are chosen by picking random numbers `t`
and `a`, and computing the following multiplications (using the notation
`[foo]bar` to mean multiply the elliptic curve point `bar` by the scalar `foo`):

+ `PKC[0] = [t^0]G1`, `PKC[1] = [t^1]G1`, ... `PKC[6] = [t^6]G1`
+ `PKCa[0] = [a t^0]G1`, `PKCa[1] = [a t^1]G1`, ... `PKCa[6] = [a t^6]G1`

Additionally, two other values are computed, but not revealed to the user:

+ `VKa = [a]G2`
+ `VKz = [(t-1)(t-2)(t-3)(t-4)]G2`

The user is expected to find 3 values `PiC`, `PiCa`, and `PiH` such that:

+ `pairing(VKa, PiC) = pairing(G2, PiCa)`
+ `pairing(G2, PiC)  = pairing(VKz, PiH)`

## Solution

Going forward, I will refer to `pairing(x, y)` by the notation `e(x, y)`.

To solve this challenge, we need to first know a little bit about elliptic curve
pairings. Skipping over a lot of details, the following facts are helpful:

+ `e(x + y, z) = e(x, z) * e(y, z)`
+ `e(x, y + z) = e(x, y) * e(x, z)`

This is known as "bilinearity". Note that addition and multiplication of these
variables here is not the regular real number addition/multiplication, but in
the elliptic curve world, since the arguments to `e` are those points.

Notice that this means that:

+ `e([n]x, y) = e(x, y)^n = e(x, [n]y)`

These few facts let us solve the entire problem.

In particular, consider `PiH = G1`.

Since we want `e(G2, PiC) = e(VKz, PiH)`,

```
e(G2, PiC) = e(VKz, PiH)
           = e([(t-1)(t-2)(t-3)(t-4)]G2, PiH)
           = e(G2, PiH) ^ ((t-1)(t-2)(t-3)(t-4))
           = e(G2, [t^4 - 10 t^3 + 35 t^2 - 50 t + 24]PiH)
           = e(G2, [t^4 - 10 t^3 + 35 t^2 - 50 t + 24]G1)
```


Thus `PiC = [t^4 - 10 t^3 + 35 t^2 - 50 t + 24]G1`, which can be computed using
values from the array `PKC`.

Similarly, we can compute PiCa from PKca, because we want `e(VKa, PiC) = e(G2, PiCa)`

```
e(G2, PiCa) = e(VKa, PiC)
            = e([a]G2, PiC)
            = e(G2, PiC)^a
            = e(G2, [a]PiC)
```

So, `PiCa = [a]PiC`.

But due to how we have `PiC = [t^4 - 10 t^3 + ... + 24]G1` (which we _just_
computed above), we now have `PiCa = [a t^4 - 10 a t^3 + 35 a t^2 - 50 a t + 24
a]G1`, which can be computed using values from the array `PKCa`.

We send these values over and get the flag:

```
Congratulations,Here is flag:rwctf{How_do_you_feel_about_zero_knowledge_proof?}
```

Solve script: [./solv.py](./solv.py)
