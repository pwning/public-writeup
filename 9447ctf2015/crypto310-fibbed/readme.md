## fibbed - Cryptography 310 Problem

### Description

`fibbed` implements a special encrypting server. A secret key is established
through Diffie-Hellman key exchange, and messages are encrypted with AES.

We get a PCAP of the initial handshake and encrypted message.

### Solution

Based on the name and a quick glance at the `fibCrypt.py` file, we quickly
establish this scheme uses the Fibonacci numbers mod a prime for the DH exchange.

To do this, Alice sends a prime, and `F_{n}, F_{n+1}`, Bob then sends
`F_{m}, F_{m+1}`. With their respective knowledge of `n` and `m`, Alice
and Bob are able to calculate `F_{n+m}` and use that as a shared secret.

After only spending a bit of time looking at this, we noticed that the
prime number used, `981725946171163877` was only 60 bits long. This meant
it was wide open to using any fairly standard discrete logarithm algorithm.

Since this isn't a simple system, `p` wasn't the order of the group (testing
by taking the `p`th Fibonacci number gave us `[1, -1]`, which wasn't quite what
we wanted. With some quick playing around we found that `2p+3` worked. This is
a bit larger, but still puts the total work involved at around 30 bits, which
is quite easy on modern machines.

We chose to use the Baby Step, Giant Step algorithm, and implemented it in C
(with a dash of C++).

We then attempt to compute the discrete log for the pair of numbers sent by
Alice (as taken from the PCAP): `[58449491987662952, 704965025359609904]`

Our code can be found in this folder as `baby.c`. Note that this was CTF code
written in C, so bugs are guaranteed. However, after about 80GB of RAM and
a bit less than 30 minutes, we get our answer: `155959985731300133`.

With this, we are able to easily use the code provided to finish the key
establishment, which allows us to re-derive the AES key in use, and decrypt
the message:

`9447{Pisan0_mU5t_nEv3r_hAve_THougHt_0f_bruTe_f0rce5}`
