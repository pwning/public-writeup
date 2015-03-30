Freak is a Windows reversing challenge.

I started this challenge by reversing some of the binary in IDA. IDA's FLIRT is able to rule out most of the binary as library code. Note that even though FLIRT only identifies ~70% of the functions here, it's usually safe to assume that all user-written functions are adjacent, and all library code is adjacent. This assumption serves well on freak, and you really only need to look at the first 7 functions. Among these 7 functions:

1. Two appear to be setting up Windows exception handling with `sub_B510F0`, `sub_B514C0`, and `sub_B516D0` as the callbacks.

2. Three are the functions I just listed above.

3. The remaining two are just subroutines of `sub_B516D0`.

I didn't really bother to understand how all the Windows exception handling stuff worked, because you can pretty much figure everything out just by reversing those three main callbacks.

Reversing is somewhat hindered by the fact that the HexRays decompiler kinda chokes, but luckily the functions are fairly straightforward.

##### `sub_B510F0`

`sub_B510F0` tries to read in a file named "Critical:Secret" and decrypts it using the RSA public key

    -----BEGIN PUBLIC KEY-----
    MEwwDQYJKoZIhvcNAQEBBQADOwAwOAIxALq4LnUOW1zMkgDMMvltyslOk4OkRITW
    R5IW33srQ2kTfkLzH5gNjTvZiuSopApJSwIDAQAB
    -----END PUBLIC KEY-----

The resulting plaintext (that we don't have the ciphertext to) is stored in a global buffer.

##### `sub_B514C0`

`sub_B514C0` looks at the first 10 characters of this global buffer, and checks that each pair of characters xored together is "BCTF2015!" (i.e. `s[0] ^ s[1] == 'B'`, `s[1] ^ s[2] == 'C'`, `...`, `s[8] ^ s[9] == '!'`).

##### `sub_B516D0`

Finally, `sub_B516D0` and its subroutines appear to use this global buffer as the key to some kind of home-rolled decryption routine that operates on a blob of encoded data. This theory is supported by the fact that, at the end, some library function is called on the decoded data, which looks kinda like it might be a `puts()`. Spoiler: it is.

##### Game time!

So, lets try to trigger this `puts()`. Judging from the second function, `sub_B514C0`, it looks like there are only 256 possible options for the global buffer (assuming it has length 10, that is; my initial guess that it was a fully-constrained length 9 string didn't pan out). The binary is kinda difficult to run in a debugger because of the exception handling funkiness, but I just manually edited the first function, `sub_B510F0`, to fill the global buffer with data of my choice, instead of actually RSA decrypting the "Critical:Secret" file.

I generated 256 modified copies of the freak binary, one for each possible length 10 string that meets the `sub_B514C0` constraint, and ran them all. Most produced garbage output, but for `\x8A\xC8\x8B\xDF\x99\xAB\x9B\xAA\x9F\xBE`:

    Your system is verified!
    The Flag is BCTF{MD5(Critical:Secret).upper()}.
    Ok.. So how to get the content of Critical:Secret?
    I've already told you somewhere, all you need is time and patience!

Hmm. "Critical:Secret" decrypted with the public key above results in `\x8A\xC8\x8B\xDF\x99\xAB\x9B\xAA\x9F\xBE`, so if we factor the public key and encrypt `\x8A\xC8\x8B\xDF\x99\xAB\x9B\xAA\x9F\xBE`, we should have the original contents. The public key is 384-bit RSA, so I just left the modulus factoring in [CADO-NFS](http://cado-nfs.gforge.inria.fr) overnight, got the primes, and reconstructed the private key.

    -----BEGIN RSA PRIVATE KEY-----
    MIHyAgEAAjEAurgudQ5bXMySAMwy+W3KyU6Tg6REhNZHkhbfeytDaRN+QvMfmA2N
    O9mK5KikCklLAgMBAAECMDmpjXdK0r4q0t/6L7fFxz05zeZ2gU6AmZyjJEBFJEVZ
    6EIPBpaKs1CuQaEhi7zEUQIZANuNctCtYTnMiJFEObYI/AXLN6b5JHh4WQIZANm3
    ZEzFfpTYXPjq/AYZ8hI6KYHsgV/aQwIYX5+74iehsQrkcGDGwgInwl5AXvkkaVQB
    AhkAq/EoJ3F57LeLhZKfg3oOMdL5YQCVlEvdAhgXnjOReOPTr5IXhWz5SAuvi8CE
    YlLgEMo=
    -----END RSA PRIVATE KEY-----

After a bit of time trying and failing to write basic Windows Crypto32 code, the Freak binary was pulled and updated with one that asked you to just submit `BCTF{hex(P^Q).upper()}`, where P and Q are the RSA primes. I dunno what was wrong with the original task (perhaps Crypto32 salts its encryption?), but whatever.

As an additional note: While reversing the binary, I was able to test my theories about what was happening by running the program in the IDA debugger, and manually setting EIP to the entry points of the above functions. Those functions themselves were pretty normal; it was just the method by which they would naturally get invoked that was all Windows-y. (Actually, now that I think about it, `sub_B514C0` was doing some weird exception things as well; while debugging, I would just jump directly the middle of the function).