## danklang - Reverse Engineering 100 Problem - Writeup by Robert Xiao (@nneonneo)

### Description

> if you see this task while scroling<br>
> <br>
> you have been visited by the reversing task of the 9447 ctf<br>
> good flags and points will come to you<br>
> <br>
> but only if you submit '9447{`dankcode main.dc`}' to this task.

### Solution

This is a short program written in an unknown meme-based language. Googling for
some of the constant strings in the program `"wewlad" "done implying"` leads us
to https://github.com/jfeng41/greentext, an implementation of a programming
language called "greentext". This is an esoteric programming language which
resembles 4chan's "greentext" quote memes.

The provided program doesn't use loops, only recursion, and under the greentext
interpreter runs *very* slowly. So we have to figure out what the functions are
doing and write more efficient implementations.

Starting from the top:

- `fail(n, 2)` is a primality test
- `dootdoot(n, k)` is the binomial coefficient `(n, k)` (can figure that out by just trying various values for `memes` and `seals` and looking it up on OEIS)
- `brotherman(n)` is the nth Fibonacci number

Each of these is efficiently computable with an alternate implementation:

- `fail(n, 2)` is replaced by `isPrime(n)`
- `dootdoot(n, 5)` is replaced by `n*(n-1)*(n-2)*(n-3)*(n-4) / 120`
- `brotherman(n)` is replaced by a memoized Fibonacci generator.

The rest of the functions, `epicfail`, `such` and `bill` are mutually recursive.
Each selects the next call according to some property of the number, and always
calls the next with `n-1`. We can therefore replace these with a single
iterative function that loops down from `n`, keeping track of which function it
is emulating at each stage.

Once we've done programming all this, we just run the updated, faster
implementation and get the flag:

    9447{2992959519895850201020616334426464120987}

See `solve.py` for the final implementation.
