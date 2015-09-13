## i - Programming 150 Problem - Writeup by Robert Xiao (@nneonneo)

For this challenge, you are given the implementation of a simple stack-based language called "i"
(itself written in a slightly obscure language called Icon), and asked to write a *quine*: a program
which, when run, perfectly reproduces its own source code (without resorting to hacks like reading
its own source code).

The classic way to do this is two-fold. First, you define a way to encode arbitrary code bytes
as a constant (e.g. a string, array or number), then you write two functions to operate on that
constant. One outputs the constant verbatim, and the other outputs the decoded version of the constant.
Then you just encode the decoder functions into the desired constant, append the decoders, and you're done.

This is the approach we take with `i`. Thankfully, `i` supports bigints (because Icon does), and `i`
also supports printing ints. So, we'll use an integer as the constant.

To decode the integer we'll just encode all the bytes of the code mod 256. This is a tiny bit wasteful,
but it's the simplest approach. This means we have to write a decoder that loops and outputs characters.

Here's the program broken down:

Encoded program code goes here:

    #12345

This outputs the hash in front of the constant:

    #35.

This outputs the encoded program as a number:

    :,

This duplicates the number, takes it mod 256, and outputs it:

    :#256%.

This divides by 256:

    #256/

We then jump back 19 bytes to the start of the loop:

    :#19~^$

(Breaking that down: we duplicate the divided value, then push -19 onto the stack.
`^` swaps the two elements because `$` expects the tested value on top and the jump
distance in second place)

All together with the right constant:

    #228292625567813707610492315745411014366174217147707905356579#35.:,:#256%.#256/:#19~^$

It's an `i` quine!
