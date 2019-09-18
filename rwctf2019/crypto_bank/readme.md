## bank - crypto problem - 94 points (56 solves)

### Description

We're given the Python implementation for a server which implements a "bank" with cryptographic signatures, and a host/port for the server.

The server uses Schnorr signatures over an elliptic curve to verify messages. You can provide your own public key, then either provide a signed message for a DEPOSIT command (to deposit one "coin") or a multi-signed message for a WITHDRAW command which gives you a flag.

The multi-signed message must be signed with a combination of your key and the "bank manager"'s key; you get their public key.

### Exploit

The bug is that the server lets you set a new public key for each command. The consequence of this is that you can sign the DEPOSIT message with one public key P1, then change your public key for the WITHDRAW command. The server verifies your WITHDRAW command using the public key (your pub key + manager's pub key) (using elliptic curve point addition), so you simply set your "public key" for WITHDRAW to (P1 - manager's pub key), and sign with your original private key. The server ends up verifying using P1 alone.

This is very simple to implement with the schnorr.py library they provide. Code is in [`exploit.py`](exploit.py).
