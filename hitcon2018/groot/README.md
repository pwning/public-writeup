# groot

This program provides a shell-like interface enabling you to do operations on
a file-tree datastructure. The datastructure is stored using parent, next-
sibling, and first-child pointers.

The main bug is that the first-child pointer is not initialized upon creating
a new file node. By allocating, freeing, and allocating an entry again you are
able to use-after-free an old child pointer.

We first use this bug in order to leak a heap address. Because the child has
been freed, its name pointer is also freed. This means that `ls` on the
directory will print out a heap address.

Next, we allocate directly on top of the freed file object, allowing us to
control the data pointer. Unfortunately, this program allocates via `strdup`,
which means that we have to be nul-free up until we reach the correct
allocation size. Fortunately, the `ls` command duplicates the file argument,
giving us easy allocation with arbitrary nul-free data.

For the purposes of controlling the data pointer, we need the `name` field to
be nul-free. Fortunately, the `vsyscall` region contains known data at a nul-
free address. By setting the name to a location in the `vsyscall` page, we are
able to `cat` the clobbered file, giving arbitrary read.

We use this arbitrary read primitive to leak the binary base from the parent
pointer of a file contained within `/`. Because `/` is a global, this leaks a
pointer in `.bss`. Then, we leak libc by leaking `puts` from the GOT.

Finally, we use the bug again to double-free a child file (reallocate and free
the parent directory, freeing the child twice) into the tcache. We land on
this location and overwrite the tcache pointer to `__free_hook`. With two more
allocations, we replace `__free_hook` with a `system`. By freeing a file
named "sh", we call `system("sh")`.

You can read the [full exploit](exploit.py).
