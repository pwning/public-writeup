We are given some Ruby code and an output file that contains some RSA parameters/ciphertext.

Interestingly, we are given 2 different public exponents where the private key used differs only by 2.
```
e1 = OpenSSL::BN.new(d).mod_inverse(OpenSSL::BN.new((p - 1) * (q - 1))).to_i
e2 = OpenSSL::BN.new(d + 2).mod_inverse(OpenSSL::BN.new((p - 1) * (q - 1))).to_i
```

We know from RSA decryption the following relationship holds:
```
d = e1^-1 (mod phiN)
d+2 = e2^-1 (mod phiN)
```

Subtracting the 2 equations yields:
```
e2^-1 - e1^1 = 2 (mod phiN)
```

Multiplying both sides by `e1*e2` yields:
```
e1 - e2 = 2*e1*e2 (mod phiN)
```

Thus, we find that `2*e1*e2 - e1 + e2` must be a multiple of phiN:
```
2*e1*e2 -e1 + e2 = 0 (mod phiN)
```

We can use this to find a possible private key and decrypt the ciphertext to get the flag: `TWCTF{even_if_it_is_f4+e}`