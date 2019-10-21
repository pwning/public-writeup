## dadadb

The binary tries to simulate a simple key-data kind of database utility. We can basically add new key-value pair, read the value for key and free the key. For updating currently existing key, it basically free the value pointer first and updates the value pointer with new buffer.

### Vulnerability

The vulnerability is in the `add` function where if you try to add new data for the key which already exists, it will free the previous data buffer and allocate new buffer for the new size, however the size which is read for input is not updated in the main structure (which stores the `key` and pointer to the `data` buffer) and hence it ends up writing the number of bytes that the first allocated buffer had for that key, leading to heap overflow and out of bounds read.

### Exploit

After logging in, we allocate our first key-data pair such that chunk allocated for value is also the same size or similar to the size of chunk we use for key structure. Allocate another key-data pair of huge size (atleast `0x70 * 3 + 0x40`, we choose 0x300). Free the first allocation and allocate/update value buffer for second key with something of size whose chunk will be allocated at the place where first key was allocated (now since the size is small, we would have an overflow here). Allocate a new key-data pair to have the following layout in the heap:

```

---+-----------+-----------+-----------+-----
   |data 2     |key3 struc |key2 struc |
---+-----------+-----------+-----------+-----
    ^________________________|

```

Doing the read on key2 will now leak the heap pointer (memory pointed by `key3->data`). Now we keep updating the value for `key2` by giving the same size as used earlier so we end up on the same place, but since our initial size was large enough, we will be able to overflow onto `key3` struct, thus overwriting `value` and `size` for it, leading to arbitrary memory leak. Using this arbitrary memory read, we leak all the information in following order:

 - leak heap encoding value and `ntdll` from the heap segment structure (usually the start of heap memory)
 - From `ntdll`, we get the `PebLdr` which helps in leaking `imagebase`
 - Once we have `imagebase`, we leak out the `kernel32`, `fopen`, `puts` and `fread`
 - Using `ntdll`, we also leak the `PEB` and `TEB` struture address (`TEB` is in the next page after `PEB`) and stack base from `TEB`
 - Once we have stack base, we find the actual address of the main stack frame and stack cookie value

Now we have all the information/memory leak we need but no write to any interesting location. To get the write, we first fix the pointer of `key3->value` and call free on the `key3` key-value pair. Now since all the chunks are in the free-list, we try to update `key2->value` again, but this time we overflow it in a way that we corrupt the free list and insert the address to fake chunk that we will be putting onto the stack. We also ensure that `flink` and `blink` are sane enough and correctly pointing to each other to avoid crash - this is the reason we choosed to have more than `0x300` size so that we can properly insert our chunk in between the free list (and not either the first or last in free list - that triggered failure for some reason).

Once the chunk address is inserted into the free list, we do add (update `key2` value) of the size equal to the one fake chunk is of, and while passing `key2`, we also pass along the data to make fake chunk on the stack. This will result in allocation on the stack. However, since `key2` size is 0x300, we end up overflowing on the stack (we know the stack cookie from leak and also the stack address so making a correct canary is possible).

Using ROP, we make our stack executable and jump to our shellcode which creates new process heap (previous one has corrupted free list) and use `fopen`, `fread` and `puts` to print the `C:\dadadb\flag.txt` file.

Output looks like the following:
```
➜  /tmp python x.py
[+] Opening connection to 13.230.51.176 on port 4869: Done
[*] heapbase: 0x261d4850000
[*] encoding: 0xaf8640b34338
[*] ntdll: 0x7ff94e161000
[*] image: 0x7ff7de140000
[*] kernel32: 0x7ff94e011000
[*] fopen: 0x7ff94b2f1770
[*] puts: 0x7ff94b300760
[*] fread: 0x7ff94b2981c0
[*] peb: 0xaf3372d000
[*] teb: 0xaf3372e000
[*] stack base: 0xaf335fd000
[*] useful info: 0xaf335ff910
[*] cookie: 0x90f720f5a869
[!] Could not find system include headers for amd64-windows
[*] Switching to interactive mode
Done!
hitcon{Oh_U_got_the_Exc4libur_in_ddaa-s_HEAP}
Try to learn breath of shadow to kill demon !
[*] Got EOF while reading in interactive
$
[*] Closed connection to 13.230.51.176 port 4869
[*] Got EOF while sending in interactive
➜  /tmp
```
