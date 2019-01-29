# Maris\_shop

**Vulnerability:**
There were multiple vulnerabilties in the binary, but the 2 which were used in our exploit are:
  - Integer overflow in signed comparison and updating the money/crystals when you buy a single item
  - If we add 16 items to the list and do buy all while clearing the list (freeing the list), the last element (index 15) is not NULL'd out. This leads to a UAF and double-free vulnerability.

**Exploit:**
  - Add item with negative amount and buy it to get more money
  - Allocate 16 times
  - Buy all, clearing the list (this leaves a pointer in the list but we don't have libc value yet due to coalescing)
  - Allocate for 3 times
  - Buy all, don't clear (free) the list
  - Allocate enough so that we get the same chunk that is pointed by the dangling pointer, and one more (to prevent coalescing with top-chunk)
  - Buy the item (index 12) which was pointed by dangling pointer (still at index 15)
  - Show cart to leak libc value
  - Overwrite bk pointer with `&(stdin->_IO_buf_end) - 0x10` by adding more amount of specific item in add to cart option
  - Allocate chunk to trigger unsorted bin attack
  - In the next call to fgets, overwrite vtable of stdin to point to user-controlled data (we use the memory region just after stdin file struct, and overwrite it with *one_gadget* address)
  - Shell!

**Flag:** `CODEGATE{55f74e7a6fa3a979f71ccfaf27aa112a}`
