# M-Poly Cipher

## Reversing

The code operated on matrices stored on the stack, and reversed (roughly) to the following sage code:

```python

def genkey():
    A,B,P = [random_matrix(GF(2^32-5), 8, 8) for _ in range(3)]
    # The next two lines are incorrect, but for our purposes are same as the actual executable
    # since both result in rank 4 matrices with the first 4 rows linearly independent.
    A[4:8] = A[0:4] * randrange(2^32-5)
    B[4:8] = B[0:4] * randrange(2^32-5)
    pub = (A, B, -A*P*P-B*P)
    priv = P
    return (pub, priv)

def enc(pub, msg):
    A,B,C = pub
    M = msg # the matrix of a message (up to 64 bytes) is just every entry is 1 byte of the message
    H = random_matrix(GF(2^32-5), 8, 8)
    return (H*A, H*B, H*C+M)

def dec(priv, cip):
    P = priv
    D,E,F = cip
    return D*P*P + E*P + F

```

## Cracking the Cipher

From the files provided, we have the pub=(A,B,C) and cip=(D,E,F) matrices.  We need to find the M matrix.

We see that F = HC + M, so if we can figure out H then we have C and F and then can figure out M.  To find H,
we know that D = HA and E = HB, but all of A, B, D, E are all singular (rank 4) we cannot solve them individually,
however we are able to solve them together by creating block matrices of rank 8 from each one.  Specifically, the
following solve code yields the M matrix.

```python

def crack(pub, cip):
        A,B,C = pub
        D,E,F = cip
        preH = block_matrix(GF(2^32-5), [[A,B]])
        postH = block_matrix(GF(2^32-5), [[D,E]])
        H = preH.solve_left(postH)
        M = F - H*C
        return M

```

### Getting the Flag

`public.key` is just the A,B,C matrices stored consecutively as unsigned C integers. `flag.enc` is the same but for matrices D,E,F.

With `flagenc` being the contents of `flag.enc` and `publickey` being the contents of `public.key`:


```python

from struct import unpack

keydata = unpack("I"*8*8*3, publickey)
flagdata = unpack("I"*8*8*3, flagenc)


A = matrix(GF(2^32-5), 8, keydata[0:64])
B = matrix(GF(2^32-5), 8, keydata[64:128])
C = matrix(GF(2^32-5), 8, keydata[128:192])

D = matrix(GF(2^32-5), 8, flagdata[0:64])
E = matrix(GF(2^32-5), 8, flagdata[64:128])
F = matrix(GF(2^32-5), 8, flagdata[128:192])

pub = (A,B,C)
cip = (D,E,F)

M = crack(pub, cip)

flag = "".join(chr(elem) for row in M for elem in row if elem != 0)
print(flag)
```

Which yields the flag `TWCTF{pa+h_t0_tomorr0w}`.