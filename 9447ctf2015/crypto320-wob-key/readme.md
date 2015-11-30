## wob-key - Crypto 190+130 Problem - Writeup by Robert Xiao (@nneonneo)

### Description (wob-key: Crypto 190)

> My friend won't believe that I signed it, and is now challenging me to sign anything she throws at me! Can you beat it?

> Find it at wob-key-e1g2l93c.9447.plumbing port 9447 

### Description (wob-key-hard: Crypto 130)
> Do it without raising any suspicion!

> Find it at wob-key-e1g2l93c.9447.plumbing port 9447 

### Solution

`wob-key` and `wob-key-hard` are very similar challenges. In both challenges, you are asked to sign 17 random 128-byte messages using the signing algorithm from `crypto130-dub-key`. Unlike in `dub-key`, however, you do not know what to sign in advance.

The only difference is that `wob-key` lets you sign 65536 messages before trying to solve the challenge, while `wob-key-hard` only lets you have 350 messages. Since we want to get both, we'll just focus on doing it in less than 350 messages.

Because you need to be able to sign arbitrary messages, you need to reconstruct enough of the secret to forge signatures.

The signing algorithm is, again:

- prepend a 128-byte secret to get a 256-byte buffer
- treat the 256-byte buffer as a directed graph, with each edge being `i→buf[i]`
- for each `i` from 0 to 255, calculate the "chain length" starting at node `i`
  (the number of nodes you can visit before you reach a previously-visited node)
- the result is the product of the chain lengths.

Terminology: "secret nodes" are nodes 0-127, and "message nodes" are nodes 128-255.

There are two kinds of secret nodes, based on their chain behaviour. "Internal" nodes
have a chain that ends in a cycle entirely within the secret; at no point does the chain involve a message node. "External" nodes have a chain that eventually "exits" into a message node. For example, "6→29→65→47→29" would mean that 6, 29, 65 and 47 are all internal nodes (with chain lengths 4, 3, 3, 3 respectively), while "9→93→160" makes 9 and 93 external nodes (with chain lengths 2 and 1 respectively).

Internal nodes are fully characterized by their chain lengths `c[i]` - we can't know exactly what nodes are involved in the chain (since e.g. `1→2→3→1`, `4→5→6→4` behaves exactly the same as `1→3→5→1`, `2→4→6→2`). External nodes are characterized by their successor node `s[i]` and final exit node `e[i]`.

#### Finding chain lengths

The "identity" message is the message `128, 129, 130, 131, ..., 255`. When signing this message, all the message chains are of length 1. Let `x` be the result of signing the identity.

If we now sign the message `128, 128, 130, 131, ..., 255` (where we set `129→128` instead of `129→129`), then the result is `2x` only if `129` does not appear in the secret - if it did appear, then some chain in the secret would become longer, which would increase the resulting signature past `2x`.

Using this technique we can figure out which message nodes do *not* appear in the secret. For this challenge, we need only a single root node, which we call `r`.

For each secret node `i`, sign a modified identity message, with `r→i`. The result will be `x*(c[i]+1)`.

#### Distinguishing internal from external

Now, note that the "shift" message `128, 128, 129, 130, ..., 254` consists of 128 chains, of length 1, 2, 3, 4, ... We'll skip over the root node `r` when constructing the shift message to leave it free. Let `d[i]` be the chain length of node `i` in the shift message. Let the signature of the shift message be `y`.

For each secret node `i`, signing a modified shift message with `r→i` will yield `x*(c[i]+1)` if the node is internal, or `x*(c[i]+d[e[i]]+1)` if the node is external. This lets us easily distinguish the two types of nodes, and also tells us where the external nodes exit to.

#### Finding external node paths

For an external secret node `i`, the possible successor nodes are those with the same exit `e[i]` and a chain length exactly one less (`c[i]-1`) (of course, if `c[i] = 1` then the successor node is simply `e[i]`).

If there is more than one possible successor node, then we have to disambiguate them. For each possible successor node `j`, we sign the modified identity message with `e[i]→i, r→j`.
If `j` is `i`'s successor, then this message will result in the chain

    r→j→...→e[i]→i→j

If `j` is not `i`'s successor, then this message results in the longer chain

    r→j→...→e[i]→i→k→...

with `k≠j`. Thus, the successor case will have the shortest chain out of all possibilities, and so we can choose the successor as the `j` which yields the smallest signature.

Thus, we can uniquely find the correct successor for each external node, and therefore fully characterize the secret.

The total number of signatures needed is 128 for the first step, 128 for the second step, and a smaller number of disambiguating signatures for the third step (usually around 60-80). Since this is less than 350, we get both flags:

    wob-key: 9447{S1gning_15_HaRD_0Bvi0Usly}
    wob-key-hard: 9447{Alth0ugh_be1Ng_sm4rt_iS_eVen_b3tter}
