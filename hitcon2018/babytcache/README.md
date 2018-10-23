# Baby Tcache - Pwn
**Vuln:** Null byte overwrite at the end of offset `size` from the start of input buffer while creating new heap.

**Exploit:**

1. Allocate a chunk `A` of size `0x1070` (large bin chunk that does not go into `tcache` upon free)
2. Allocate a chunk `B` of size `0x20` (any size that falls into `tcache` size range)
3. Allocate a chunk `C` of size `0x1000` (any size that does not fall into `tcache` size range). We choose `0xff0` because the chunk allocated will be of size `0x1000` so that it does not shrink on null byte overwrite
4. Allocate a dummy chunk so that freeing `C` , top chunk does not coalesce with top chunk
5. Free chunk `A` and `B`
6. Allocate a chunk of size `0x20` (returns the chunk `B`) such that it sets the `PREV_INUSE` bit of next chunk `C` to `0` and overwrite the `prev_size` to `0x1090`
7. Free chunk `C`. It coalesces with freed chunk `A` leading to overlapping chunks
8. Free recently allocated chunk `B`
9.  Allocate chunk of size `0x1070`
10. Allocate chunk of size `0x1090` and only overwrite the lower two bytes of `B`'s `fd` with the lower two bytes of the address of `_IO_2_1_stdout_->_IO_write_ptr` (involves 4 bit of brute-forcing)
11. Allocate chunk of size `0x20`. Allocating another chunk of size `0x20` will give the chunk on top of `_IO_2_1_stdout_->_IO_write_ptr`. We overwrite the least byte of `_IO_write_ptr` with the value `0xf0` to leak the address of `_lock`
12. Repeat the above step again to get allocation over `_free_hook` and overwrite it with one_gadget address
13. Free any chunk

**~** Jenish Rakholiya