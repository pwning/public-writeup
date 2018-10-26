# secretnote

This challenge lets you store notes that are only readable in encrypted form.
You can encrypt your notes with RSA or AES. The RSA key is provided and has a
small modulus, and the AES key is loaded remotely. The flag is stored in a
note encrypted with AES, and the AES key is stored in a note encrypted with
RSA.

The notes are stored unencrypted and encrypted on demand. Thus, memory
corruption could exposure some secret data.

The main bug is the AES encryption makes an allocation based on the padded
size of the plaintext, but calculates the size of the padding in two different
ways. If the message is a multiple of the block size then the message is
allocated assuming no padding, and then padding with an entire block. This
gives you out-of-bounds heap write. Unfortunately, the heap write is encrypted
so you have no control over the contents (the IV is fixed and unknown on each
connection).

Using this OOB write, we can corrupt the plaintext of the encrypted AES key.
In this way, we can get the RSA-encrypted key in two ways: corrupted and
uncorrupted. We can also leak the corruption by encrypting two different known
messages after corrupting them. Because the IV is constant, the corruption is
constant as well.

Using the Franklin-Reiter attack on RSA, we are able to first find the value
of the corruption and then find the value of the AES key. This attack works if
we have two polynomials under the integers mod N that are both zeroed by the
unknown message. By taking the greatest common divisor of these two
polynomials, we find a monomial (X - m). Then, the constant coefficient is the
negative of the message we are looking for.

We first do this with our known, corrupted messages with the corruption as the
common root. Then, we use our corruption and the uncorrupted message with the
AES key as the common root. This gives us the AES key.

Finally, we can encrypt a known message using this AES key and back-solve to
find the IV. Then, we can decrypt the encrypted flag.

See the [full exploit](exploit.py). We performed the FR attack using
[sage](dual_fr_attack.sage).
