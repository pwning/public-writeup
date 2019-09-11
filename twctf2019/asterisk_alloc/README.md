Asterisk-Alloc
==============

 - Use only realloc to get overlapping unsorted bin and tcache chunks
 - use malloc to get allocation over the `stdout` structure and overwrite the fields to leak libc - there is a 4 bit bruteforce that we need to do to get this allocation
 - do tcache dup again to get allocation over the free hook (in our case, we are allocating 8 bytes before free hook, so that we can have `/bin/sh\x00` followed by `system` address in `__free_hook`). Call free on realloc'd pointer

**Flag:** `TWCTF{malloc_&_realloc_&_calloc_with_tcache}`

