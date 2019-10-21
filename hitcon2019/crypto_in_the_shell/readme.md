## Crypto in the Shell - pwning challenge - 20 solves (284 points)

We're provided a binary and an IP:Port to attack. The binary has a buffer in its .bss segment. It lets you input an offset and a size parameter, encrypts `size` bytes starting from `offset` bytes into the buffer using an unknown AES key, then outputs the result. Neither `offset` nor `size` are checked in any way, giving you the ability to perform an "encrypt-what-where" with a relative offset. You get to do this a total of 32 times.

We first "encrypted" the AES key, which was also stored in .bss. Since the encryption result is returned, this allowed us to see what the new key was. We then encrypted the `dso_handle` at the start of the read/write .data segment, which points to the exe itself, allowing us to leak the exe base address (as we now knew the AES key). Then we "encrypted" the `stderr` pointer in the exe's .bss to leak libc too. Finally, with both the exe and libc bases, we could "encrypt" the environ pointer in `libc` in order to leak a stack address.

With a stack address in hand, we were able to "encrypt" the loop counter in `main`'s stack to make it a large negative value, allowing us to have infinite encryption attempts. Because we could choose the offset with byte granularity, we figured we could actually write data one byte at a time by "encrypting" a target until the first byte was what we wanted, then sliding one byte over and doing it again. To avoid round-trip reads from the server (which kept giving us timeouts), we fully emulated this process so we knew exactly what to send. We used our infinite reads and byte-by-byte write to write a simple `execve` ropchain, and thus got our flag:

`hitcon{is_tH15_A_crypTO_cha11eng3_too00oo0oo???}`

See [`exploit.py`](exploit.py) for the exploit script.
