# Boxes of Ballots Writeup
### Hack the Vote 2016 – crypto200

Adam Van Prooyen [website](http://van.prooyen.com/cryptography/2016/11/06/Boxes-of-Ballots-Writeup.html)

> Privjet Komrade!

> While doing observing of Amerikanski's voting infrascture we find interesting box. We send operative to investigate. He return with partial input like showing below. He say box very buggy but return encrypted data sometimes. Figure out what box is do; maybe we finding embarass material to include in next week bitcoin auction, yes?

## Overview

In addition to this description, the Russian spy was also able to exfil a transmission snippet which when reconstructed looks like this:

``` javascript
{"debug": true, "data": "BBBBBBBBBBBBBBBB", "op": "enc"}
```

If we send this to the server, we get back a response that remote debugging enabled along with an error:

``` python
{"debug": true, "data": "BBBBBBBBBBBBBBBB", "op": "enc"}
[+] Remote Debugging Enabled
Traceback (most recent call last):
  File "./blocks.py", line 115, in dataReceived
    self.key = encData['key']
KeyError: 'key'
```

Now we know that the remote debugging mode allows to leak information about the program itself. If we add a field for the key of the appropriate length (16 bytes), the server responds with:

``` python
{"debug": true, "data": "BBBBBBBBBBBBBBBB", "op": "enc", "key": "AAAAAAAAAAAAAAAA"}
[+] Remote Debugging Enabled
{"Status": "ok", "data": "0134c8a2c19a4c9af41d8dd5f34916e0"}
```

## Gathering Information

Now that we have a basic idea of what the server expects from us, we can manipulate the program to crash at different points in the execution. Since the program gives us the error traceback, we can use this to reconstruct the program source.

For instance, if we give the data as a list with the same length as the key instead of a string, we learn that the data is being encrypted with CBC:

``` python
{"debug": true, "data":[1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6],"op": "enc", "key": "AAAAAAAAAAAAAAAA"}
[+] Remote Debugging Enabled
Traceback (most recent call last):
  File "./blocks.py", line 97, in encrypt_data
    enc = encrypt_cbc(self.key, self.iv, encData['data'])
  File "./blocks.py", line 61, in encrypt_cbc
    ctxt = xor_block(blocks[i],IV)
  File "./blocks.py", line 45, in xor_block
    first[i] = chr(ord(first[i]) ^ ord(second[i]))
TypeError: ord() expected string of length 1, but int found
```

And if we make the list shorter, we get another error which leaks information about how the plaintext is padded.

``` python
{"debug": true, "data":[1,2,3,4,5,6,7,8,9,0,1,2,3,4,5],"op": "enc", "key": "AAAAAAAAAAAAAAAA"}
[+] Remote Debugging Enabled
Traceback (most recent call last):
  File "./blocks.py", line 97, in encrypt_data
    enc = encrypt_cbc(self.key, self.iv, encData['data'])
  File "./blocks.py", line 57, in encrypt_cbc
    plaintext = pad(plaintext,len(key))
  File "./blocks.py", line 25, in pad
    return instr + ' ' * (length - (len(instr) % length ))
TypeError: can only concatenate list (not "str") to list
```

After several more of these leaks, most of the source code is recovered:

``` python
def pad(instr, length):
    return instr + ' ' * (length - (len(instr) % length ))

def encrypt_block(key, plaintext):
    encobj = AES.new(key, AES.MODE_ECB)
    return encobj.encrypt(plaintext).encode('hex')

def xor_blocks(first,second):
    # ...
    for i in range:
        first[i] = chr(ord(first[i]) ^ ord(second[i]))
    # ...

def encrypt_cbc(key, IV, plaintext):
    if(len(plaintext) % len(key) != 0):
        plaintext = pad(plaintext, len(key))
    blocks = [plaintext[x:x+len(key)] for x in range(0,len(plaintext),len(key))]
    for i in range(len(blocks)):
        if i == 0:
            ctxt = xor_block(blocks[i], IV)
            ctxt = encrypt_block(key,ctxt)
        else:
            tmp = xor_block(blocks[i],ctxt[-1 * (len(key) * 2):].decode('hex')) #len(key) * 2 because ctxt is an ASCII string that we convert to "raw" binary.
            ctxt += tmp
    # ...
    return ctxt

def encrypt_data(encData):
    enc = encrypt_cbc(self.key, self.iv, encData['data'])

def dataReceived():
    # ...
    self.key = encData['key']
    # ...
    op = encData['op']
    self.ops[op](encData) # just enc 4 now
```

After reconstructing the source, it was still unclear what we were actually trying to discover. After toying with some requests for a litter longer, I realized that the if the debug field is removed, the encryption key is ignored *and* that the ciphertext is longer than it should be.

``` python
{"data": "BBBBBBBBBBBBBBBB", "op": "enc", "key": "AAAAAAAAAAAAAAAA"}
{"Status": "ok", "data": "adf983dcb5f1d388ba06074330c0b9194376b61c668693277c00a5f3649fdea4b7f7e2e12ce6610fd54de6768483bcb5"}

{"data": "BBBBBBBBBBBBBBBB", "op": "enc", "key": "BBBBBBBBBBBBBBBB"}
{"Status": "ok", "data": "adf983dcb5f1d388ba06074330c0b9194376b61c668693277c00a5f3649fdea4b7f7e2e12ce6610fd54de6768483bcb5"}
```

Because of this, we know that the server is likely appending extra information -- probably the flag!

## Breaking the Cipher

From the source code, we know that the server is using a custom implementation of AES CBC. Additionally, because the same data encrypted multiple times yields identical ciphertexts, we know that a fixed IV is being used. Unlike [ECB](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Electronic_Codebook_.28ECB.29), [CBC](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#CBC) mode is usually not vulnerable to byte by byte decryption. However, the constant IV allows for this kind of attack. 

The idea of a byte by byte decryption is to give the server the blocksize - 1 known bytes to encrypt so that the full plaintext is:

``` python
'A' * (blocksize - 1) + flag
```

Now the first block of encrypted message is made up of A's and the first byte of the flag. Using this fact, we can brute force the first byte of the flag by sending the same number of A's and all possible values for the byte and checking if the first block of the ciphertexts match.

We can continue this process until we recover all the bytes of the flag.

> flag{Source_iz_4_noobs}

``` python
sol = ''
for i in range(32):
    base = 'A' * (15 - (i % 16))
    desired = get_enc(base)
    examining = (i // 16 + 1) * 32
    for c in string.printable:
        if get_enc(base + sol + c)[:examining] == desired[:examining]:
            sol += c
            print(sol)
            break
```

# Downloads
[ballots.py](ballots.py)  
[blocks.py](blocks.py)