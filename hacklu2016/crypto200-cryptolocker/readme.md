# cryptolocker Writeup
### hack.lu 2016 – crypto200

Adam Van Prooyen [website](http://van.prooyen.com/cryptography/2016/10/20/cryptolocker-Writeup.html)

For this challenge, we were given a simple file encrypting command line utility and an encrypted file. The utility takes a file and an eight character password and outputs an encrypted file.

> Usage: ./cryptolock.py file-you-want-to-encrypt password-to-use

Using this password, it constructs 4 keys by sha256-ing 2 bytes of the password at a time:

``` python
keys = [ # Four times 256 is 1024 Bit strength!! Unbreakable!!
    hashlib.sha256(user_input[0:2]).digest(),
    hashlib.sha256(user_input[2:4]).digest(),
    hashlib.sha256(user_input[4:6]).digest(),
    hashlib.sha256(user_input[6:8]).digest(),
]
```

To encrypt data, it repeatedly encrypts the data and writes the final output:

``` python
one        = self.ciphers[0].encrypt(plaintext)
two        = self.ciphers[1].encrypt(one)
three      = self.ciphers[2].encrypt(two)
ciphertext = self.ciphers[3].encrypt(three)
```

Since the "1024 bit" key is derived from eight bytes, the key is actually only 64 bits. Although a brute force attack on a 64 bit key is [possible](https://www.iacr.org/archive/ches2006/09/09.pdf), it is not feasible for the time or resources of a 24 hour CTF.

The vulnerability here is that the encrypt function pads the input before it runs the cipher using [PKCS#7](https://en.wikipedia.org/wiki/Padding_%28cryptography%29#PKCS7). With this specification, the last byte of each decrypted step should specify how much padding was added and all padding bytes should have the same value. 

This way, we can brute force two bytes of the password at a time by attempting to decrypt the ciphertext once and checking if the padding is valid. By chance, some padding is going to be valid even it is not the correct decryption. However, we know that the last three encryptions are on already padded data. Therefore, it will be padded to the block size (16 in this case). Since it is almost impossible for a correct padding of length 16 to happen by chance, the password bytes for a decryption with this padding are correct.

Using this method, we find that password is "Sg52WH4D". The decrypted file is saved as "file.dec".

``` bash
$ file file.dec
.../cryptolocker/flag.dec: OpenDocument Text
```

Opening the document shows the flag: "flag{v3ry_b4d_crypt0_l0ck3r}"

[cryptolocker.zip](cryptolocker.zip)  
[crack.py](crack.py)