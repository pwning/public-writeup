## Useless returnz - Misc Challenge

We are provided with the following hint:

```
I don't know the cipher Key, but I can login as admin using "Useless" challenge!
http://13.125.133.10
```

The previous challenge, Useless, provided us with a python script that used a fixed
key and IV to encrypt a string. If we encrypt the string ```admin127.0.0.1```, we
can send it as our session id and get a flag.

For this challenge, we no longer assume the key is fixed. So we need to find a way
to use the python script and the server to encrypt the admin session string.

A quick read of the python script reveals a block cipher with CBC. While the
block cipher may be broken in some way, we instead focus on CBC and finding
ways to use the server as an encryption oracle.

One thing that we noticed is that the server respects the **X-Forwarded-For**
header. This allows us to inject arbitrary text into the session during login, which
will get encrypted and sent back to us as a cookie. We used this to generate
a valid admin cookie by creating the user **admin127** and setting the
**X-Forwarded-For** header during login:

```
curl -v http://13.125.133.10/login -d username=admin127 -d password=admin127 -H ‘X-Forwarded-For: .0.0.1xxxxxxxxxxxx’
< Set-Cookie: useless_session_id=5e0a4973106c3f776b1877611a222b5e350a22730e18774a2f5567701e262f4c220a7c734a52600a; Path=/
```

Unfortunately, the problem author did not let us get away with an easy solution,
because in order to get the real flag we need to now encrypt an arbitrary string:

```
Encrypt the below plain text in { } with key, and Auth IT!
ENCRYPTME{IT’s_Wh3re_MY_De4M0n5_Hid3_###_}
```

Thankfully, we can still use the server as an oracle, provided we know the IV. We 
assumed it was the same as the previous challenge. Let's start with a simple input:

```
curl -v http://13.125.133.10/login -d username=a723 -d password=fooqqq123 -H ‘X-Forwarded-For: 0xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx’
< Set-Cookie: useless_session_id=080a40731d732f6e764035725169605a210a69731d5a2f47764035725169605a210a69731d5a2f4772532c7f576f66472d0a6e730a487204; Path=/
```

Our input string was split into blocks: ```a7230xxx```, ```xxxxxxxx```, ```xxxxxxxx```, ..., etc.
And we received back the encrypted blocks: 080a40731d732f6e, 764035725169605a, ..., etc.

Since the encryption algorithm uses CBC, we know that the plaintext for the third block
is XOR with the encrypted second block, then encrypted. We can use this to encrypt an
arbitrary string by XOR the first block of the arbitrary string with IV and the encrypted
second block.

```
xor(xor(‘useles5@’, ’IT\‘s_Wh3’), ‘764035725169605a’.decode(‘hex’)) => ‘JgwmkM=)’
```

The rest of the input will be unmodified. We can now take the encrypted output, truncate
the first two blocks, and use the remaining blocks as our flag.

```
curl -v http://13.125.133.10/login -d username=a723 -d password=fooqqq123 -H ‘X-Forwarded-For: 0xxxxxxxxxxxJgwmkM=)re_MY_De4M0n5_Hid3_###_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx’
< Set-Cookie: useless_session_id=080a40731d732f6e764035725169605a160a6373116a7f131d314e6a102821457f0a2373554550303b53573a1a222b22550a327345282c062b43472a0a323b32550a327345282c066e0a027e172f2637550a34731172685d2c4d0b7e1a222b23; Path=/
```

Flag:
```
160a6373116a7f131d314e6a102821457f0a2373554550303b53573a1a222b22
```

