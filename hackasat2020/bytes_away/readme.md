## Satellite Bus - Bytes Away! - 223 points (11 solves)

### Background

> We have an encrypted telemetry link from one of our satellites but we seem to
have lost the encryption key. Thankfully we can still send unencrypted commands
using our Cosmos interface (included). I've also included the last version of
`kit_to.so` that was updated to the satellite. Can you help us restore
communication with the satellite so we can see what error "flag" is being
transmitted?

We are given `kit_to.so` and a cosmos installation.

### Solution

We see that `kit_to.so` encrypts telemetry packets in `PKTMGR_OutputTelemetry()`
with AES256 (`PKTMGR_encrypt()`) using an unknown key and IV from external
functions `get_key()` and `get_iv()`.

Interestingly enough, `KIT_TO_AppMain()` `mprotects` the page containing
`PKTMGR_OutputTelemetry` as RWX. We also have the ability to modify memory
with the `MM POKE_MEM` command, so perhaps we can modify the telemetry packet
sending to not encrypt the packets?

We can patch the instruction at `0x2615` (offset 350 from `PKTMGR_OutputTelemetry`)
from
```
8d9524aaffff    lea edx, [ebp-0x55dc]
```
to
```
8b9514aaffff    mov edx, DWORD PTR [ebp-0x55ec]
```
by a single 32bit write so `PKTMGR_OutputTelemetry` sends the plaintext
instead of the encrypted packet.

We then enable telemetry with a `KIT_TO ENABLE_TELEMETRY` command, and the
server sends us the unencrypted flag!

Connection script is in [connect.py](connect.py).
