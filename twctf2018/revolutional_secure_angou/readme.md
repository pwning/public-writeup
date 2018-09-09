## Revolutional Secure Angou - Crypto Challenge - Writeup by Samuel Kim (@ubuntor)

### Description

We get an RSA public key, an encrypted flag, and the generator ruby script:

```ruby
require 'openssl'

e = 65537
while true
  p = OpenSSL::BN.generate_prime(1024, false)
  q = OpenSSL::BN.new(e).mod_inverse(p)
  next unless q.prime?
  key = OpenSSL::PKey::RSA.new
  key.set_key(p.to_i * q.to_i, e, nil)
  File.write('publickey.pem', key.to_pem)
  File.binwrite('flag.encrypted', key.public_encrypt(File.binread('flag')))
  break
end
```

### Solution

Note that `q = e^(-1) (mod p)`. Then `eq = 1 + kp` where `k` is in the range `[0, e]`.

Then `ne = pqe = p + kp^2`, so we have the following quadratic: `kp^2 + p - ne = 0`.

Note that `n` and `e` are known from the public key, and we can brute force `k`.

We can check each resulting quadratic and check for roots to see if one of them is `p`.

Solution script in [solve.sage](solve.sage).
