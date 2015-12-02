## calcpop reloaded (pwn 130)

### Description

I heard someone owned my calculator, so I've decided to port it to a more secure OS.

I've also added some proof of work, I'm sure that will stop the hackers!

Find it at os-uedhyevi.9447.plumbing port 9447

The flag is in /ctf

### Reversing

The binary was in a non-standard format. Opening it in IDA and marking
start of the file as code yields reasonable-looking x86 code. Reaching
the first string reference, it becomes clear that the code expects to be
loaded at 0x100000. The program contains various syscall functions
(identifiable thanks to helpful log strings), and appears to be run on
an OS which uses `int 0xff` for syscalls.  Reversing a little more,
program behavior appears identical to the calcpop challenge - it
repeatedly reads 256 command bytes into 136-byte stack buffer, and
supports help, exit, or summing two numbers. If the command does not
match help or exit and does not contain a space, it prints the address
of the stack buffer. If the sum of the two numbers is 0x31337, the
program returns.

### Exploit

This was a straightforward buffer overflow. For unknown reason, I had
issues returning to shellcode in the buffer, so I used ROP instead. The
one piece of complexity was that the read for the buffer overflow
terminates at a null byte or a new line. To address this, we take
advantage of the fact that we can trigger the buffer overflow repeated
and write the ROP backwards, doing a separate read for each null byte
that we need.

We were only told that the flag was in `/ctf` so we list the directoy by
opening/reading `/ctf` and sending the result back. This revealed the
filename to be `/ctf/level1.flag` and we simply replace the filename
with this to obtain the flag.

See
[exploit.py](https://github.com/pwning/public-writeup/blob/master/9447ctf2015/pwn130-calcpop-reloaded/exploit.py)
for the full exploit.
