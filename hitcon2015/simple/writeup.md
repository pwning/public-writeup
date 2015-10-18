# Simple - Crypto 100 problem

In this challenge, we have the ability to log into a website with a username
and password. These are stored in a json blob, along with the dictionary
element `"db":"hitcon-ctf"`. This json blob is then encrypted with AES in CFB
mode and saved as a cookie. Our goal is to get the json blob to also encode
`"admin":true`.

To do this, we feed in a message of length 81, just over 5 blocks. This has a
final 17 bytes of plaintext as `db":hitcon-ctf"}`, but we want it to be
`":1,"admin":true}`. We simply use xor to convert the last full block of text,
leaving just the last byte corrupted due to propogation in CFB. To solve this
we simply guess random characters for the last byte of ciphertext until we
get our flag: `hitcon{WoW_CFB_m0dE_5o_eAsY}`
