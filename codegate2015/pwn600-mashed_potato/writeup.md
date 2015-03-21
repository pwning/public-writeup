# Mashed Potato (400pts)

"Mashed potato" is a remote pwnable challenge.

Mashed potato has several obvious buffer overflows, effectively `fgets(stack_buf[500], atoi(fgets(...)), stdin)`, but stack canaries keep them from being immediately exploitable.

In one such case, the overflowable buffer is passed through deflate(), and the size of the compressed data is displayed back to the user. By specifying that this buffer be oversized (and therefore include the stack canary), and then taking advantage of the fact that fgets() will stop reading on a newline to NOT overflow the buffer, we can get deflate() to operate on user-supplied data with the canary appended to the end (while not actually corrupting the stack canary). Because the program allows us to do this repeatedly, we can use a CRIME-like technique to leak out the stack canary.

After leaking the stack canary, there are non-deflate()ing overflows that allow easy exploitation via ROP.

An attack script is attached. The most relevant detail to note is that zlib deflate() only really starts using LZ77 backreferences for 3-bytes matches, so bootstrapping the attack is a little tricky. To achieve this, we take advantage of the fact that the first byte of x86-64 stack canaries is always a null byte (which normally _prevents_ leakage of the canary, heh).