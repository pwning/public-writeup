## pngparser - Pwnable Challenge

We are given a URL for a website that accepts either a PNG either via an
upload or a URL and parses it. The result page includes the contents of
the image file in base64. Specifying a file:// URL allows dumping the
source of the web app:

```bash
curl http://110.10.212.132:2223/url -F protocol=file:// -F url=/app/app.py
```

We find that it calls a binary called PNGParser on the input file, and
dumped that file as well. It is a 32 bit binary with no interesting
protections.

Reversing the binary, we see that it calls parses a PNG and then calls
`system` to print a success message for no good reason. This appears to
have been a pattern in this CTF.

The PNG chunk parsing code has a rather contrived bug (there is another
contrived bug with an uninitialized function pointer in PLTE chunk
handling, but we did not use this). The program repeatedly reads up to
0x10000 bytes from the input file and runs the following code to process
what it read:

```c
  // data is a fixed heap buffer that 0x10000 bytes is repeatedly read into
  // len is the number of bytes read.
  size_t offset = 0;
  while ( offset < len )
  {
    if ( len - offset >= state->capacity - state->length )
      amount = state->capacity - state->length;
    else
      amount = 2000;
    ...
    memcpy(&state->buf[state->length], &data[offset], amount);
    state->length += amount;
    offset += amount;
    if ( state->length >= state->capacity )
    {
      ok = process_chunk(state);
      if ( !ok )
        return 0;
    }
  }
```

For no good reason, it copies 2000 bytes into the buffer when there is less
data available than expected. In certain states (for example, when reading a
new PNG chunk type), `state->buf` points a buffer inside of `state` itself.
Since `state` is on the stack, this leads to a stack buffer overflow.

While the program has no stack canaries, there is a `FILE*` above
`state` on the stack, and `feof` and `fclose` are called on this before
the program returns. To get around this, we construct a fake `FILE`
object at a known place in memory. Luckily, the handler for tEXt chunks
unnecessarily reads input into a buffer in .bss. This gives us
everything we need to exploit the buffer overflow.

To exploit this program, we send the required IHDR chunk, then send an
ancillary chunk (with a lowercase first character of the chunk type),
which the program does not process in any complicated way. In this
ancillary chunk, we place the data that will be copied in the buffer
overflow.  Specifically, we aim to set `state->capacity` and
`state->length` so that after the overflow, the program will not attempt
to process a chunk, but go back to the outer loop which calls `feof` and
`fclose`. We also overwrite the FILE pointer to point to what will be
our fake FILE in BSS.

Next, we send a tEXt chunk containing our fake FILE. The FILE is setup to
return 1 for `feof` and call `system(FILE*)` when `fclose` is called on it.

Finally, we send some padding to bring the length of the file to a little more
than 0x10000. Since the `data` buffer is reused (and not cleared between uses),
this ends up pointing it to our overflow data. At this point, we trigger the
bug, providing only one additional byte in the file when the program expects 4.
This triggers the stack overflow, `memcpy`ing our overflow data over
`&state->header` and overwriting `state` and the `FILE` pointer as described
above. This allows us to execute commands, and the output is printed back on
the website after we upload our exploit PNG.

Sending an `ls` shows that the flag is in a file called
`Th1s_1s_S3creT_F14g_F0r_YoU`, and reading that file produces the flag:

```
FLAG{sh3_1s_b3t1fu1_#$%}
```

The last challenge is realizing that the site does not accept `FLAG{}`,
so we must submit:

```
sh3_1s_b3t1fu1_#$%
```
