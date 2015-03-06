## Wonderland - Crypto 600 Problem - Writeup by Robert Xiao (@nneonneo)

Wonderland was quite a tough problem. Opening up the package, we see that the server implements some kind of elliptic curve scheme. We found that the curve was given in Montgomery curve form, and checked that the arithmetic was all correct (also verified by checking with SAGE).

The server lets us pick an arbitrary base point, which is "exponentiated" to the power of the unknown flag. Thus our goal is to find this flag. With a base point on the curve, this is quite difficult - it is equivalent to the ECC discrete log problem, and there's no obvious weaknesses with the curve. The order of the points is

    k1 = 1461501637330902918203684014253252914573215409208

which factorizes as `2*2*2*182687704666362864775460501781656614321651926151`: the presence of the really big prime makes the curve quite secure.

The weakness of the scheme lies in the fact that it accepts arbitrary base points, without checking to see if they lie on the curve. This makes it possible to supply points that actually don't lie on the curve at all - they lie instead on the "quadratic twist" of the curve, an object with different mathematical properties. In particular, the multiplicative order of points on the quadratic twist is not equal to the multiplicative order of points not on the quadratic twist. For example, the order of the point `[8; 1]` (a point with `x=8`) is

    k2 = 1461501637330902918203685651179313124738649676760

and, unlike the order of the points on the curve, this order factors as

    2*2*2*5*7*31*5857*3280967*68590573243*308648791439*413879086189

which consists of a bunch of small factors.

Now the attack is clear. We can a non-curve point `P_f` of order `f` by computing `[8; 1]^(k2/f)` whenever `f` is a factor of `k2`. Then, we can ask the server to exponentiate `P_f`: the result is a point `P_f^e` for some `e` congruent to the key. Finding all the `e`s will let us apply the Chinese Remainder Theorem to recover the key.

The actual attack, then, uses a variation of Pollard's Rho algorithm to compute the discrete logarithms `e` for each `P_f^e`. The full details can be seen in `attack.py`.
