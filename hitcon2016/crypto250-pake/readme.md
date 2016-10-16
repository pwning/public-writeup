## PAKE - Crypto 250 Problem

### Description

nc 52.198.13.246 20431
pake1.rb

### Writeup

The server will XOR the flag with 11 keys that are generated using SPEKE. The same prime is used for every round, but the secret password for each round is a number between 1 and 16. Naive brute force against the server is impossible because it would require 17 trillion connections.

Instead, we will use the fact that if we open two connections to the server, we can make the server establish a key with itself. The result is that we will get two encrypted flags (K1 and K2) which are the same because the generated keys were the same:
```
K1 = K2
flag ^ (K1,1) ^ (K1,2) ^ ... ^ K(1,11) = flag ^ (K2,1) ^ K(2,2) ^ ... ^ K(2,11)
```

Now, for a single round, instead of just forwarding the public values between the connections, we can instead guess a password (number between 1 and 16) and use it to generate the private values, public values, and round keys for both connections. Now, the encrypted flags will not be equal because each connection generated a different round key, but if we guessed the correct password then we know the round keys and we get:
```
K1 ^ K(1,n) = K2 ^ K(2,n)
K1 ^ K2 ^ K(1,n) ^ K(2,n) = 0
```

Because we can now brute force each password individually, instead of needing 17 trillion connections, we can instead brute force every password with only 176 connections.

Once we know all of the secret passwords, we can trivially get the flag.

Solution: [exploit.py](exploit.py)
