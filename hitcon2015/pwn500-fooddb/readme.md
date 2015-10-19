## Fooddb - Pwn 500 Problem - Writeup by Robert Xiao (@nneonneo)

### Description

> Do you want some delicious food ?<br>
> nc 52.68.53.28 0xdada
> 
> fooddb-e303c9bc733ca06044a7bd2b6ea12129<br>
> libc-3f6aaa980b58f7c7590dee12d731e099.so.6

### Reversing

The program implements a pretty simple "food database" written in C++ which allows you to insert, show, edit and delete foods, and insert and delete food types (categories). The strange thing is that the food's name is stored as a `char *` (when all other strings are stored as `std::string`). The `Food` structure looks like

    struct Food {
        char valid; // if unset, food will not be erased during "delete food" operation
        char renamed; // if set, further name changes are forbidden
        /* 6 bytes padding */
        char *name;
        std::string type;
    };

When editing a food, the function `Food::rename` (`sub_346A`) will directly writes up to 8 bytes to the name if the input is <= 8 bytes. Otherwise, it `realloc`ates the name.

### Bug

When renaming a food, you can specify the new name as `\x00AAAAAAAAA` (at least nine bytes starting with a null byte), which causes the rename function to call `realloc(food->name, 0)`. Under glibc (and as specified by POSIX), this frees the name and marks the food as invalid. However, the name pointer is not reset, leaving the modified `Food` with a freed pointer. Later, a vector resize can be triggered to cause the `Food` to be destructed, resulting in a double-free (this double-free cannot be triggered with a simple "remove food" due to the validity check).

### Exploit

The double-free bug allows us to construct a Food that points at freed memory, and then use the 8-byte overwrite from the first branch of `Food::rename` to overwrite either the free heap metadata (in glibc, the "forwards" pointer) or the first 8 bytes of some heap structure. I didn't find any particularly useful allocated structures to overwrite (as `Food`'s first 8 bytes are just flags), so I chose to overwrite a free chunk. This allows me to allocate a fake object that overlaps with some real object, enabling a larger overwrite.

We start by deleting all existing foods, since a later step requires that we create a food close to the start of the food vector.

We setup the necessary fake memory chunk by abusing Food's `operator=` to memory-leak a name, arranging things so that it will be adjacent to the object we overwrite later. We then create a pair of objects, one "shadow" (index 0) and one "victim" (index 1) having equal-length names (which must both be shorter than the "fastbin" limit in glibc). We apply the bug to the victim, causing it to have a freed pointer. We can no longer rename or delete the victim directly.

By adding a bunch of objects, the vector will resize. When this happens, it will allocate a second vector containing new shadow and new victim Foods. The new shadow Food will get a pointer to the previously freed name (because of the LIFO nature of glibc's fastbins). When the old vector is destroyed, the old victim is deallocated and the pointer is freed again - now the shadow Food points at the freed chunk, but it is still renamable.

We rename the shadow Food to point the freed chunk's "forward pointer" at our fake chunk in memory. Creating a new Food with the right name length will result in two allocations. The first allocates our freed chunk, and the second allocates our fake chunk. The fake chunk is set up so that the end of it overlaps the new Food vector, and so the name written to the new Food will overflow into the Food vector.

We use this overflow to write the address of glibc's `realloc_hook` to one of the Food names. There are two complications, however: first, we can't have any null bytes so the overflow must end at the name overwrite, and second, the overwrite will clobber the `renamed` flag of the target Food, causing it to be unrenamable.

We get around the second problem by overwriting the Food that is being created (in our case, Food #4), so that upon return from the overwriting `memcpy`, the constructor will reset the renamed flag to zero. We get around the first problem by arranging our heap sizes carefully so that the overwrite will have the correct name length.

Finally, if we are successful, we can simply edit the new Food and write a pointer to `system`, since the new Food's name points at the `realloc_hook`. We trigger our modified hook by creating a final object and editing it to trigger `realloc`, getting a shell and the flag.

See the full exploit in `pwn.py`.

### Flag

    hitcon{sH3lL_1s_4_d3L1c10Us_f0oD_1S_N7_17}

