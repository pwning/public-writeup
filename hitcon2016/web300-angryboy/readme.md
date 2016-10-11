## Hackpad - Crypto/Forensics 150 Problem

### Description

Why my teammate, Angelboy, is so angry?
http://52.196.144.8:8080/

### Hint

```
$ java -version
java version "1.7.0_111"
OpenJDK Runtime Environment (IcedTea 2.6.7) (7u111-2.6.7-0ubuntu0.14.04.3)
OpenJDK 64-Bit Server VM (build 24.111-b01, mixed mode)
```

### Writeup

The page gives us its source, a Java class file. Decompiling it, we find that
the page lets us guess a byte of a secret key, but only after we solve a md5
captcha, increasing in difficulty as we recover more and more bytes. When we
guess the last byte correctly, the page also gives us a flag encrypted with
the md5 hash of `our ip + secret key`. 

After we recovered the secret key, we found that decryption didn't work.
Apparently, Java's conversion from byte arrays to strings is weird. Running
decryption routines under the version of Java given in the hint correctly
decrypted the flag.

Captcha solving script: [captcha.py](captcha.py)
