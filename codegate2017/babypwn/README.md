## babypwn - Pwnable Challenge

This service implements a simple echo server. There is a trivial stack buffer overflow when it receives the message. Exploitation requires bypassing the stack canary first.

When it receives the message, it does not NUL terminate it. So we can fill the memory up to the canary with bytes, and then when it prints, we will know the canary. Now we construct our message so that it overflows the buffer, sets the canary correctly, and overwrites the return pointer.

They gives us the system import, so we can simply return to system with a buffer containing a command as an argument. We can leak out a stack address, so we know where the buffer we control is in memory. Since this service is not inetd-like, we need to redirect stdin/stdout of sh to our file descriptor.
