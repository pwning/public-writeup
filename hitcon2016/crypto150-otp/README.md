# Crypto 150 &mdash; OTP

In this problem, we are given a remote web service that allows us to send arbitrary data, and have it be "encrypted" with a random string. However, before the encryption occurs, the flag for this problem will be appended to our input string. Then, the program will generate some number of bytes (up to 10000) of random data, and then XOR your string with it. Once the encryption has been completed, it sends the resulting string back to the sender. In addition to this, the program allows you to choose where the random data is being generated from. Among the available options are:

 - /dev/urandom
 - openssl
 - gcrypt
 - gnutls

Given a problem like this, our first instinct might be to send a really large request to drain the systems entropy, followed by a shorter guess. The idea behind this approach is that if we drain entropy from /dev/urandom, another algorithm being seeded by it might be much easier to brute force the random state from. However, this approach will not work because each connection is only allowed to encrypt once. After the string has been returned to the client, the connection terminates. After poking around on the internet for a bit, we came up with [this article](http://formal.iti.kit.edu/~klebanov/pubs/libgcrypt-cve-2016-6313.pdf) from two researchers from the Karlsruhe Institute of Technology. It describes CVE-2016-6313, a bug in gcrypt that allows an attacker to "trivially" predict 20 bytes of the random state, given the preceeding 580 bytes. While this paper does an excellent job describing the bug in high level terms, it does not actually provide any code samples or specific details on how to predict these 20 bytes.

To understand what the bug is, we have to dive into the libgcrypt source code for a bit. When libgcrypt is generating random numbers, it creates what it calls an entropy pool. On most systems, this pool is 600 bytes long (20 byte blocks, 30 blocks). This entropy is pulled from a number of sources on the target system, and just gets thrown into this big pool. Then, to prevent against side channel attacks on the random state, the pool is mixed. This is akin to taking a large spoon and stirring it around the pool until the individual sources of entropy are indistinguishable. The above article describes in overview how this process occurs, but does not give specifics as to how this mixing occurs. To understand this, and why its important, we need to dive into the libgcrypt source. 

The interesting funtion for this problem is in `random/random-csprng.c`. If we look at `mix_block`, we see that it performs this loop over the entropy pool

```c
for (n=1; n < POOLBLOCKS; n++) 
  {    
    memcpy (hashbuf, p, DIGESTLEN);

    p += DIGESTLEN;
    if (p+DIGESTLEN+BLOCKLEN < pend)
      memcpy (hashbuf+DIGESTLEN, p+DIGESTLEN, BLOCKLEN-DIGESTLEN);
    else 
      {    
        unsigned char *pp = p + DIGESTLEN;

        for (i=DIGESTLEN; i < BLOCKLEN; i++ )
          {    
            if ( pp >= pend )
              pp = pool;
            hashbuf[i] = *pp++;
          }    
      }    

    toBurn = _gcry_sha1_mixblock (&md, hashbuf);
    memcpy(p, hashbuf, 20 );
  }
```

For every set of 20 bytes, they are calculated by performing `_gcry_sha1_mixblock` on the concatenation of the following 44 bytes, and the preceeding 20. However, there is an issue in the way they do this. As the article mentions, when it computes the first 20-byte block, it does so from the first 20 bytes of the pool, and from the last 44 bytes, which is a slight variation on the technique used in the remaining blocks. Thus, the second block of 20 bytes is the pool will never be used as the second parameter of the mixing function. As the Researchers demonstrate, this means there is a loss of entropy during the mixing process. In this case, this loss of entropy manifests itself in the last 20 byte block of the pool.

For this block, when mixing occurs, it will take the previous 20 bytes in union with the following 44 bytes. However, since its at the end of the pool, those 44 bytes wrap around to the beginnning of the pool. Thus, when it computes the `_gcry_sha1_mixblock` "hash" of it, its drawing completely from the mixed entropy pool. Given that the results of mixing are what gets returned by the call to `gcry_randomize`, those bytes will be known to us. Thus, if we have this function `_gcry_sha1_mixblock` we may compute outright the last 20 bytes of the pool.

If we look into `cipher/sha1.c`, we see that all this function does is call a subroutine of the standard SHA1 hashing function called `transform`. This function takes a set of initialization variables (`0x67452301`, `0xEFCDAB89`, `0x98BADCFE`, `0x10325476`, and `0xC3D2E1F0` for the standard SHA1 function), and transforms them according to a SHA-specific algorithm. While it would certainly be possible to extract this functionality and reimplement it into our main exploit script, it turned out to be easier to simply take the `sha1.c` file and strip out all of the code that we didn't need. From there, we could add a main method that would allow for passing in the byte data and have it return the result of the mixing function. 

Unfortunately, this system was missing one crucial element. Its not apparent from the function call, but `md`, the message digest object that references the SHA state, is upbdated on successive transform calls. Furthermore, at the end of the transform call, the 20 byte result is stored in the initial parameters field. Thus, in order to get this to work, we need to pass the 20 bytes preceeding the 20 in question as the initialization variables for this digest algorithm. Once we have all of these components, we can put it together, and predict 20 bytes at a time of the random state. By sending the server 20 bytes that we know, we can calculate the final one. Performing this twice gives us the whole flag. 

To test the exploit, first install `libgcrypt` (`apt-get install libgcrypt` or `brew install libgcrypt`) and pwntools, then run `make && python ./drain.py`. This should fetch and print the flag from the local binary.
