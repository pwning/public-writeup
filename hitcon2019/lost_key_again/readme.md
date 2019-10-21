# Lost Key Again

We have an RSA encryption oracle with unknown `n` and `e`, but it always
prepends `"X: "` to our input: `oracle(x) = ("X: "+x)^e mod n`

Note that
```
  oracle(x+"\x00")
= ("X: "+x+"\x00")^e mod n
= (("X: "+x)*256)^e mod n
= ("X: "+x)^e(256^e) mod n
= oracle(x)(256^e) mod n
```
and similarly `oracle(x+"\x00\x00") = oracle(x)(256^(2e)) mod n`.

Then we have
```
oracle(x+"\x00\x00")oracle(x) - oracle(x+"\x00")^2 = 0 mod n
```
so we can generate many multiples of `n`, and take the gcd to recover `n`.

Script in [recover.py](recover.py).

We then tried factoring `n`. It turns out that Williams's `p+1` algorithm
factored `n`:
```
python -m primefac -m=p+1 28152737628466294873353447700677616804377761540447615032304834412268931104665382061141878570495440888771518997616518312198719994551237036466480942443879131169765243306374805214525362072592889691405243268672638788064054189918713974963485194898322382615752287071631796323864338560758158133372985410715951157
```
so we can now compute some discrete logs mod `p` and mod `q` to
recover `e`, then compute `d` and decrypt the flag.

Solve script in [solve.sage](solve.sage).
