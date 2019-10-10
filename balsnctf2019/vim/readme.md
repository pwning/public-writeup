# vim

For reversing, a hint told us that there were "registers" and "calling
convention". When we looked at the code, we quickly realized that the marks were
being used as registers, with lowercase marks (a-z) used as general purpose
registers and the uppercase marks (A-Z) being used as a kind of stack to store
arguments and saved registers.

Realizing this allowed us to break up the big pile of Vim code into functional
blocks based on recognizing the function prologue (which "pushed" a bunch of
registers onto the stack) and epilogue (which "popped" the registers off the
stack and stored a result in register `a`). The reversing strategy was to
find-and-replace the inlined function chunks with calls to Vim functions which
contained the common code, enabling us to rewrite the Vim code into a more
standard style. Then, it was simply a matter of figuring out what each function
did. We kept our nicely disassembled code, in
[task.annotated.vim](task.annotated.vim), functionally equivalent to the
original, allowing us to debug the program by inserting "breakpoints" (crashing
instructions).

With the disassembled code, we were able to derive the following pseudo-code:

```
flag = "Balsn{"+flagpart+"r}"
# len(flagpart) == 16
flagpart = map(lambda x: ord(x) % 32, rot13(flagpart))

B = matrix("Welcome_to_th1s_") # 4x4 matrix, mod 32
C = matrix(flagpart) # 4x4 matrix, mod 32

BB = B*B
CC = B*B*C
​
prev = 0
for i in range(16):
    b = BB[i] <<< 3
    c = CC[i] <<< 3
    c += prev
    result = b + c
    print(result)
    prev = result
```

We can recover `BB[i]+CC[i]` by taking differences, then we can subtract off
`BB[i]` to recover `CC[i]`, then calculate `B^(-2)*CC` and rot13 to get the flag.
