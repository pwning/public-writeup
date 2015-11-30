#!/usr/bin/python3
from Crypto.Util.number import isPrime

import sys

def dootdoot_5(n):
    return (n * (n-1) * (n-2) * (n-3) * (n-4)) // 120

fibs = [1, 1]
def brotherman(n):
    # fibonacci numbers
    while n > len(fibs):
        fibs.append((fibs[-1] + fibs[-2]) % 987654321)
    return fibs[n-1]

def epicfail(n):
    x = 0
    mode = 'epicfail'
    while n:
        if n % 10000 == 0:
            print("progress: ", n)
        if mode == 'epicfail':
            if isPrime(n):
                x += 1
                mode = 'bill'
            else:
                mode = 'such'
        elif mode == 'bill':
            y = brotherman(n)
            if y % 3 == 0:
                x += 1
                mode = 'such'
            else:
                mode = 'epicfail'
            x += y
        elif mode == 'such':
            y = dootdoot_5(n)
            if y % 7 == 0:
                x += 1
                mode = 'bill'
            else:
                mode = 'epicfail'
            x += y
        n -= 1
    return x

print(epicfail(9))
assert epicfail(9) == 73

print(epicfail(23001))
assert epicfail(23001) == 75395552257179342059104

n = 13379447
print(epicfail(n))

# 9447{2992959519895850201020616334426464120987}
