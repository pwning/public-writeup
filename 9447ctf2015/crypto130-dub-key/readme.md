## dub-key - Crypto 130 Problem - Writeup by Robert Xiao (@nneonneo)

### Description

> My friend set up a small signing scheme, however she won't let me sign stuff. Can you get it signed?

> Find it at dub-key-t8xd5pn6.9447.plumbing port 9447 

### Solution

The signing algorithm is a bit of a curious one. It signs 128-byte messages as follows:

- prepend a 128-byte secret to get a 256-byte buffer
- treat the 256-byte buffer as a directed graph, with each edge being `i→buf[i]`
- for each `i` from 0 to 255, calculate the "chain length" starting at node `i`
  (the number of nodes you can visit before you reach a previously-visited node)
- the result is the product of the chain lengths.

In this challenge, you need to generate the signature for a specific 128-byte message, and you can ask for the signatures of up to 256 other messages.

Terminology: "secret nodes" are nodes 0-127, and "message nodes" are nodes 128-255. The "target" is the message to be signed.

The "identity" message is the message `128, 129, 130, 131, ..., 255`. When signing this message, all the message chains are of length 1. Let `x` be the result of signing the identity.

If we now sign the message `128, 128, 130, 131, ..., 255` (where we set `129→128` instead of `129→129`), then the result is `2x` only if `129` does not appear in the secret - if it did appear, then some chain in the secret would become longer, which would increase the resulting signature past `2x`.

Using this technique we can figure out which message nodes do *not* appear in the secret. We can also trivially filter out message nodes that appear in the target (since we know the target). These nodes therefore have no incoming edges, and so editing one of these "root" nodes in the target will affect only the chain starting at that node.

Let `r1` and `r2` be two distinct root nodes - the likelihood of finding two such nodes is very high. Then we sign three modified target messages:

- `r1→r1, r2→r2`: the "baseline" `a` - `r1→r1`: this signature `b` will be equal to `a * chainlength(r2)` - `r2→r2`: this signature `c` will be equal to `a * chainlength(r1)`

Then we can calculate the signature of the target as `a * chainlength(r1) * chainlength(r2)`, or simply `a*(b/a)*(c/a)`.

See `solve.py` for the full implementation. When run, we get a flag:

    9447{Th1s_ta5k_WAs_a_B1T_0F_A_DaG}
