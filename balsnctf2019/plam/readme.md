# pLam

This was a tough challenge. We spent a long time trying to understand what the various Lambdas represented - since a lambda can represent both data and code, it can be very hard to untangle these two.

Eventually, we figured out that the functions `c/d/h/i` constructed tree objects which looked like this:

    Value: Bool | (\c.c Bool Value Value)

They employed a temporary stack which looked like this:

    Stack: (\c.c Value Stack)

to construct the objects. We reimplemented the logic in Python. Each `e` and `g` function passed to `j` was being used basically as a tree walk. The logic effectively XORs together various bits of the flag and checks the parity through a large number of conditions. One complicating factor was the fact that some of the parity bits selected different conditions to check.

We tried to solve it with z3 and boolector, but both took too long. Instead, I used my `solve_gf2` library to brute-force 65536 possible combinations of boolean equations, and eventually got a winning combination of bits:

`[0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0]`

Converting that to hex gave us the flag:

`Balsn{1e54d4b3ca953d4bcd4ab27e}`

See [`solve.py`](solve.py) for details.

