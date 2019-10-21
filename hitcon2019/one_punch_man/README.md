## One Punch Man

A service which allocates, reads, writes and frees a non-fastbin sized chunks.

### Vulnerability

The characters pointers are not made `NULL` after freeing, thus giving us read/write on freed memory

### Exploit

Exploit is very much similar to the idea used in lazyhouse challenge

 - Fill tcache and read the freed tcache memory to get heap leak (we choose the size of chunk as 0x410)
 - Fill 5 tcache entries for 0x220 size chunks
 - Allocate 2 chunks (first one of size 0x410 and second one of any size to prevent coalescing with top) and free the first chunk
 - Read memory to get libc leak
 - Allocate huge chunk (again of size 0x410) and another chunk of size 0x210 (this we will use while faking the small bin free list)
 - Now basically try to allocate chunks such that we send a 0x220 chunk into the small bin and then corrupt the free list such that last chunk is the one which was already inserted, however its bk points to another fake free chunk. For the fake free chunk, we would have its fd pointing back to original chunk in small bin, and bk pointing to top address location on the main arena (we choose top address so that we can change it and it also satisfies the requirement of `address+0x10` and `address+0x18` pointing to valid memory region for proper fd/bk list update
 - Allocate chunk of size 0x220, so the tcache now gets filled and the first entry for size 0x220 is filled with the address we want to get allocation on
 - Allocate using `malloc` to get overwrite on top (overwrite top address this with the start of heap address - to overwrite tcache structure)
 - On next allocation update the number of entries in tcache as 0x8 for size 0x220 and make the entry to point to `__malloc_hook`. Now doing another malloc allocation will give write over `__malloc_hook`.
 - Since we have a huge buffer on the stack while calling calloc in debut function, we overwrite the `__malloc_hook` with gadgets to do ROP using our stack buffer
 - We use ROP to make the heap executable and then jump to the address in heap where we have stored shellcode to open/read/write arbitrary file
