## scs7 - Crypto Challenge - Writeup by Samuel Kim (@ubuntor)

### Description

We get a network service that sends us an encrypted flag and allows us to make
100 encryption queries.

### Solution

The service seemed to use a base64-like encoding, run through a random
substitution (different per each connection).

Playing around with encryption revealed that it used base59, as encrypting
`v = chr(2 * 59)`
changed the first character compared to the encryption of
`u = chr(2 * 59 - 1)`.

We grabbed an implementation of base58 from 
[https://github.com/keis/base58/blob/master/base58.py](https://github.com/keis/base58/blob/master/base58.py)
and modified it to use base59 instead.

We then gathered multiple encryption samples to derive the substitution and
decode the flag.

Solution script in [scs7.py](scs7.py).
