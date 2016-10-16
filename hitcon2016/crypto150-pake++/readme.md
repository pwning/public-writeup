## PAKE++ - Crypto 150 Problem

### Description

nc 52.198.13.246 20432
pake2.rb

### Writeup

The server will XOR the flag with two keys that are generated using SPEKE. The two keys are generated using two primes selected at random from a list of primes.

We are able to decrypt the flag without breaking SPEKE by using the properties of XOR. By opening 3 connections to the server, we can exploit the situation when:

  - Connection 1 (first prime) and connection 2 (first prime) are the same
  - Connection 1 (second prime) and connection 3 (first prime) are the same
  - Connection 2 (second prime) and connection 3 (second prime) are the same

If we XOR the outputs of those situations, we get the unencrypted flag (where K(n,m) is the generated key for connection n and m):
```
 = (flag ^ K(1,2) ^ K(1,3)) ^ (flag ^ K(1,2) ^ K(2,3)) ^ (flag ^ K(1,3) ^ K(2,3))
 = flag
```

Since the primes are chosen uniformly randomly from a list of 8 primes, the expected number of times we need to run our naive solution is 512 times.

Solution: [exploit.py](exploit.py)
