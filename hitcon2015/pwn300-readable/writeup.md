# readable (pwn 300)

## Description

```
Can you read everything ?
nc 52.68.53.28 56746

readable-9e377f8e1e38c27672768310188a8b99
```
(Intentionally no libc given)

## The bugs

The program is *really* simple.

```C
ssize_t __fastcall main(__int64 a1, char **a2, char **a3)
{
  char buf[16]; // [sp+0h] [bp-10h]@1

  return read(0, buf, 32uLL);
}
```

It reads 32 bytes into a 16-byte stack buffer. This gives us full control of the buffer, saved rbp, and return address. 

## Exploit

The first challenge is to get data that we control into the bss section, so that we can stack pivot to the bss section. This will give us an arbitrarily long rop chain. Our strategy was to use our control of rbp and set it to the memory location we want to write to plus 0x10 bytes. Then return to `0x400505` so that our memory location is used as the destination buffer. We can repeat these steps to read in as many blocks of 16 bytes as we require.

Next, we need to generate a rop chain that will give us a shell. With NX and ASLR enabled, and no knowledge of the libc binary, this is non-trivial. We realized that by brute forcing the last byte of the `read` pointer in the GOT we could stumble upon a `syscall` instruction. In order to know when we hit the `syscall` instruction, we needed to have `eax` set to 1 so that it would be a `write` to `STDOUT`. We can control `eax` by doing a read with `eax` number of bytes (`read` returns the number of bytes read in `eax`). Note that we do not need to brute force again once we find the last byte.

Now a shell is trivial. We setup the registers for a `execve` syscall and call the `read` pointer that has been changed to point to a `syscall` instruction.

See
[exploit.py](https://github.com/pwning/public-writeup/blob/master/hitcon2015/pwn300-readable/exploit.py)
for the full exploit.

## Flag

Flag: `hitcon{R3aD1NG_dYn4mIC_s3C710n_Is_s0_FuN}`
