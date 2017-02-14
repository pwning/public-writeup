## messenger - Pwnable Challenge

This is a simple challenge that allows you to leave messages, remove messages, change messages, and view messages. There is a heap overflow in change message, because it copies the new message into the old buffer without checking the size.

This challenge also uses a custom heap allocator that is very simple. It allows for trivial write-4-byte-anywhere by modifying the heap links that come before a heap block. Also, NX is disabled so we can just point RIP at a buffer containing our shellcode.

We use the heap overflow to change the heap links, so that the exit pointer in the GOT is modified to point to our shellcode. Since this will also change the bytes at (shellcode + 8), we prepend our shellcode with a jump past that point. The shellcode just calls /bin/sh to give us a shell.
