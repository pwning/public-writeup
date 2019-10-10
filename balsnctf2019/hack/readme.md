# Hack

The compiler is pretty dumb and only makes simple optimizations. Therefore, we were able to use a bunch of regular expressions to transform the given code and simplify it, aided by the fact that we had access to the compiler source code.

This produced the file [`main.annotated.asm`](main.annotated.asm), from which we were able to determine that the algorithm was simply adding up various characters in the flag and checking them against constants. This can be trivially solved by z3, see [`solve.py`](solve.py). When run, this gives the flag:

`Balsn{U_r_C0Mp1LeR_h4cKer}`
