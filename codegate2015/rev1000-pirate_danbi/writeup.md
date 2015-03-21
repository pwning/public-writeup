# pirate_danbi (1000pts)

## Description
Pwnable for Ubuntu 14.04 64-bit 

## Solution
The basic flow of main is it reads in *danbi_key*, then reads in commands which are 3 bytes (1 byte cmd, 2 bytes big endian length of data) followed by data.

Looking at the available commands, we see a command (0x401348) that will execute a script that we provide if we are able to set the *authenticated* flag (0x6030EC). The *authenticated* flag is set by *check_flag* command (0x4012B0) which compares a buffer to the string **YO\_DANBI\_CREW\_IN\_THE\_HOUSE.**.

The *password* buffer is initialized in another command (0x400EDB) which implements a basic decryption function using *danbi_key* as the key and the command data as the ciphertext. The steps of the decryption algorithm are:
 - XOR key with last block of the ciphertext
 - Verify that the key is padded correctly (it uses PKCS#5 padding) and store in *is_valid*
 - For each block except the last block, XOR the bytes with the next block and then subtract the key bytes from it, modulo 256.
 - The last block is the key

This algorithm is susceptile to a padding oracle attack, provided that the *is_valid* result can be determined after running the command. The only place that it is used however, is in the function (0x4011B6) that decompresses the bzip2 file that we provided. And the only place that the result of the decompression is used is in 0x401348 which is guarded by the *authenticated* flag. So, instead of reading *is_valid* directly, we need to use a side channel.

The only easy side channels are going to be using the bzip2 decompression. If we can determine whether the bzip2 decompression occurred, then we know the value of *is_valid*. The two obvious side channels are crashing the program with a bad input to bzip2 or a timing attack. We used a timing attack by providing a bzip2 file that decompresses to 1000 times the size of the output buffer, and then calling the decompression command 1000 times. This magnifies the timing difference and makes it measurable, even from across the world.

We use the oracle by brute forcing each byte of the secret key; until the last byte is a 01, then the second to last byte is a 02, etc. The resulting secret key (*danbi_key*) was:

```
\xeb\x22\x42\x8f\x7f\xff\xf9\x0a
```

Using the secret key we can easily encrypt a payload that will decrypt to the correct password:

```
\xd6\x59\x67\x3f\x80\x9c\xb3\x3f\xb8\x74\x7a\x8a\x42\xd3\xfa\x00\xcc\x55\x6a\x3c\x9a\xb3\xaa\x44\xb8\x67\x6c\x8a\x7a\xfa\xfc\x0f
```

Now we just bzip2 our command, send the server the encrypted password and the bzip2 file, then tell it to run the command!

## Flag
```
barking_danbi_is_waiting_for_you_at_finals
```
