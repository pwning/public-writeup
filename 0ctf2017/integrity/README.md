## integrity - Crypto Challenge - Writeup by Tim Becker (@tjbecker)

This service attempts allows you to create "login secrets" for any
name of your choice, except for `admin`. The goal is to construct a
secret for `admin` and login.

The scheme works by encrypting `md5(pad(username)) || pad(username)`
with AES CBC mode, with a random IV. The secret contains the concatenation
of the IV and the ciphertext produced.

Since our usernames are allowed to be 2 blocks long, we can request a secret
for `md5(pad("admin")) || "admin"`. The padded version of this message will be
`p = md5(pad("admin")) || pad("admin")`, and so the secret will be
`IV || AES-CBC(IV, md5(p) || p)`.

Because of how CBC works, any suffix of the message will decrypt successfully.
So if we drop the IV and use `AES-CBC(IV, md5(p) || p)` as our secret, then
this will decrypt to `p = md5(pad("admin")) || pad("admin")`, which will
validate correctly for the username `admin`.

Solution script [here](./solve.py).
