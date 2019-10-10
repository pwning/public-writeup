# simple sol aeg

We used [this decompiler](https://ethervm.io/decompile) for the contracts.

We have 3 kinds of contracts:
* We need to call a single function to win.
* We have multiple functions, and we need to call one of them.
* We have to call a function with an argument that's within a specific range.

We can distinguish between them by checking the length.

Solution script in [solve.py](solve.py).
