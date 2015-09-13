## Alicegame - Crypto 250 Problem - Writeup by Robert Xiao (@nneonneo)

In this challenge, you connect to a server which generates a random set of parameters for
ElGamal encryption, then lets you encrypt up to 10 messages with chosen `r`. It then encrypts
the flag with a random `r` and asks you to decrypt it.

In brief, the setup works as follows:

- Generate a random prime `p`
- Generate a random generator element `g` between 2 and p-1
- Generate a random secret exponent `x` between 1 and p-1
- Publish `p`, `g`, and `h = g^x mod p`

Then to encrypt, it does the following:

- Compute `c1 = g^r mod p`
- Compute `c2 = m * h^r mod p`
- Send `c1` and `c2`

Since we control both `m` and `r`, we can trivially work out what `p`, `g`, and `h` are:

- `m=1 r=1` => `c1=g c2=h`
- `m=-1 r=1` => `c1=g c2=p-h`

Once we know `p`, `g`, and `h` we can encrypt our own messages and don't need the oracle anymore.

Our goal is to decrypt the flag, which is encrypted with a random and unknown `r`. How can we do that?

The security of ElGamal relies on the difficulty of taking a _discrete log_ mod p, that is, calculating
`x` such that `g^x = h`. It turns out that this is only hard if `p-1` has a big prime factor - otherwise,
if `p-1` has all small prime factors, you can solve the discrete log under each factor and combine the
results using the Chinese Remainder Theorem. In this challenge, since `p` is chosen randomly, sometimes
`p-1` will have no large factors (in mathematical terms, `p-1` is "smooth").

Thus, the solution boils down to trying again and again until we get a smooth `p-1`, at which point
we quit and compute the discrete log. In my case, I tried about 100 times until I got the following
parameters:

    p = 2488665134832285853092948293008213155978176626596688076035471
    g = 2059715652525439319626604918085000816657307363269561921215002
    h = 2446745500193945956354541994529416399024970775365943146442167
    p-1 = 2 * 3^4 * 5 * 13 * 397 * 34703 * 142231 * 663997 * 1335134757001 * 1681985613731 * 80885896977317

We can calculate discrete logs mod a prime `q` in time proportional to `sqrt(q)` using the baby step-giant step
algorithm. Using the Pohlig-Hellman algorithm for discrete logs in groups of smooth order, we find that

    x = 398107572758509184512000160060709442427941395118355047140976

in less than a minute with an unoptimized Python implementation. With this, we can decrypt the message

    c1 = 2452567037320397751961393328390658371418392744217174769456381
    c2 = 2275782475603610705409626635179996988083154458407066163845692

using the relation

    m = (c2 * inverse(pow(c1, x, p), p)) % p

and obtain the flag

    MMA{wrOng_wr0ng_ElGamal}
