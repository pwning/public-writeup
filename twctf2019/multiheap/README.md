# Multiheap

We are given a typical-looking heap menu challenge, where we are able to more or less freely create, edit and free different heap chunks. We can easily get a libc leak by reading a chunk before writing to it. The chunks are stored in a vector, and when a chunk is freed it is erased from the chunk vector. There is also no overflow, so there is no immediate memory corruption.

However, there is also a 'copy chunk' function which copies data from one chunk to another, which may be run in a separate thread. Therefore, we can race the 'copy chunk` and 'free chunk' functions to write over the tcache next pointer of the freed chunk. The rest is standard stuff.

The race is unfortunately not always the most stable because pthread_create call passes a pointer to a stack object to the thread runner instead of allocating memory for the struct, so it just randomly crashes because the struct gets overwritten. (We did not see a convenient way to control this value directly).

However we can just send this race a bunch of times and hope it doesn't crash, and that the race succeeds, and after a few (~1-5) runs it gives shell.

`TWCTF{mulmulmulmultititi}`
