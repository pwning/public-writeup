Examining the source code, we can see it implements some custom hash function:
```
def easy_hash(x):
    m = 0
    for i in range(len(x) - 3):
        m += struct.unpack('<I', x[i:i + 4])[0]
        m = m & 0xffffffff
    return m
```

The goal of the challenge seems to be to find a message that hashes to the same hash as `MSG`'s hash (second-preimage).

Note that in the `easy_hash` function, it adds one character at a time: `struct.unpack('<I', x[i:i + 4])[0]`. We can just add a null byte in the middle of `MSG`, so when hashed, 0 will be added and won't affect the final result.

Sending request with this new message, we get the flag: `TWCTF{colorfully_decorated_dream}`