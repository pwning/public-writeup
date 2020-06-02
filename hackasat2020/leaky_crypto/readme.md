## Payload Modules - Leaky Crypto - 223 points (11 solves)

_Writeup by: Jay Bosamiya (@jay\_f0xtr0t)_

### Background

> My crypto algorithm runs in constant time, so I'm safe from
> sidechannel leaks, right?
>
> Note: To clarify, the sample data is plaintext inputs, NOT
> ciphertext
>
> You'll need these files to solve the challenge.
>   https://generated.2020.hackasat.com/leaky/leaky-papa45187foxtrot.tar.bz2

We are given two files inside the .tar.bz2:

+ [Readme.txt](./provided/Readme.txt)
+ [test.txt](./provided/test.txt)

The first contains some information about an AES key (the first 6
bytes are given, rest is unknown), and an ECB encrypted
ciphertext. The second contains a plaintext to timing mapping, for
10000 plaintexts.

### Solution

Given that the challenge implied a timing attack on AES, the obvious
choice would be [Cache-timing attacks on
AES](https://cr.yp.to/antiforgery/cachetiming-20050414.pdf) by djb
in 2005. However, a quick test shows that this does not apply, and the
provided data doesn't allow us to obtain information via this.

However, something related to this must work, so we find a paper that
references the above paper. [Cache-Collision Timing Attacks Against
AES](https://www.microsoft.com/en-us/research/wp-content/uploads/2006/10/aes-timing.pdf)
by Bonneau and Mironov in 2006. This one appears more promising.

Let's call any arbitrary plaintext `P` and the key as `K`. For this
attack, you group plaintexts (for each index `i` and `j`) by
`P[i]^P[j]`, and look for the cache sidechannel. If `i` & `j` were
accessing the same table, then `K[i]^K[j]` is `P[i]^P[j]`.

When we do the above, we get only the higher 6 bits (i.e., the lower 2
bits are indistinguishable). Also using this, we only are able to
identify the top bits of 7 of the 10 unknown bytes. The other 3 do not
show any correlation. This means we have a brute force of `7*2 + 3*8
== 38` bits. This is infeasible.

When we plot the data to see patterns in the values, we notice that
the data is quantized, and thus it points strongly towards the data
being synthetic. This means that some assumption that we made might've
been broken during the synthesis process by the problem authors. The
most obvious such broken assumption would be the "same table"
assumption (which for actual implementations, would definitely apply,
but is easy to miss when reading the paper). The same table assumption
simply means that the only "useful" indices should be ones which
access the same AES table (which happens when `i === j (mod 4)`).

When we relax this assumption (i.e., we are moving away from what
might happen in practice) we notice that we are able to get the more
top bits out. In particular, we now can identify the top bits of 9 of
the 10 unknown bytes. This places a brute force of `9*2 + 1*8 == 26`
which while large (~70 million cases), is within feasible range.

Thus, we implement a bruteforce for these values, testing for the
presence of `flag{` in the result of the ECB decryption, and sure
enough, we obtain the flag!

The full solve script can be found [here](./solve.py).
