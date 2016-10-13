## Hackpad - Crypto/Forensics 150 Problem

### Description

My site was hacked. The secret was leaked.

(link to pcap)

### Writeup

Browsing the given pcap, we see encrypted ciphertext, and a bunch of calls to a
web service that decrypts data, which gives errors most of the time.
This sounds like a padding oracle attack!

We look for decryption calls of the form
`[data (full 16 bytes)][ciphertext block (16 bytes)]` that succeed.

If it succeeds, then the decryption must be correctly padded, and at this stage
of the padding oracle attack, the last block must be all 16s, meaning that
`data ^ decrypt(ciphertext block) = [16]*16`.

We compute `data ^ previous ciphertext block ^ [16]*16` to extract the
decryption of `ciphertext block` in the real message.

Script to view data: [solve.py](solve.py)
