# Children Tcache - Pwn

**Vuln:** Read input of exactly the size allocated and use `strcpy` to copy the buffer from stack to its destination which lead to null byte overflow.

**Exploit:**

1. Allocate a chunk `A` of size `0x1070` (large bin chunk that does not go into `tcache` upon free)
2. Allocate a chunks `B` and `C`  each of size `0x20` (any size that falls into `tcache` size range)
3. Allocate a chunk `D` of size `0x1000` (any size that does not fall into `tcache` size range). We choose `0xff0` because the chunk allocated will be of size `0x1000` so that it does not shrink on null byte overwrite
4. Allocate a dummy chunk so that freeing `D` , top chunk does not coalesce with top chunk
5. Free chunk `A` and `C`
6. Allocate a chunk of size `0x20` (returns the chunk `C`) such that it sets the `PREV_INUSE` bit of next chunk `D` to `0`
7. Repeating allocation and free with size reduced by 1 each time can help in overwriting the `prev_size` field of next chunk `D` to `0x10b0`
8. Freeing chunk `D` coalesces with freed chunk `A` leading to overlapping chunks
9. Free recently allocated chunk `C`
10.  Allocate chunk of size `0x1070`
11. Use `show heap` on chunk `B` to leak the `fd` pointer of the chunk in unsorted bin
12. Allocate chunk of size `0x30` and overwrite the `fd` to the address of `__free_hook`
13. Allocate chunk of size `0x20` twice. Second allocation gives chunk over `__free_hook` and overwrite it with one_gadget
14. Free any chunk

**~** Jenish Rakholiya