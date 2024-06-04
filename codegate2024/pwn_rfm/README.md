# rfm - Pwn, 805 points (5 solves)

_Writeup by [@nneonneo](https://github.com/nneonneo)_

Description:

> This is really not a my college assignment. 🤪
> 
> nc 3.35.170.102 8811
> 
> rfm.zip

We're provided with a `rfm` Linux binary and a Dockerfile for running it.

## Reversing

`rfm` is a forking socket server, although it calls `exec` to re-execute the binary for each connection.

It implements a file management service (like an FTP server) using a custom binary protocol and an in-memory filesystem. File entries are stored using the following structure:

```c
struct myfs_entry {
    int id;         // incrementing id
    int leaf_id;    // id for the leaf structure, if present
    int _0;         // always set to zero
    int refcount;   // reference count
    int dtype;      // object type: 0 = regular file, 1 = directory, 2 = symlink
    char * fullpath;// full path from root to this file
    char * name_in_parent; // name of this entry in the parent directory
    void * contents;  // type depends on dtype
    struct myfs_entry * parent; // parent directory, or NULL for root
    struct myfs_entry * next;   // sibling objects in the parent directory
    struct myfs_entry * prev;
};
```

The type of `contents` depends on the `dtype`: it is a `myfs_leaf *` for regular files, `myfs_entry *` for directories (forming a linked list of directory contents), and `char *` for symlinks. `myfs_leaf` functions like an `inode`, and looks like this:

```c
struct myfs_leaf {
    int leaf_id;    // random ID for this leaf (like inode id)
    int refcount;   // reference count for this leaf structure
    int field2_0x8; // unused/unknown field
    time_t ctime;   // timestamps for these contents
    time_t mtime;
    time_t atime;
    struct data_buf {
        char * buf; // buffer pointer, points to data.data for an inline buffer
        ulong size; // size of the actual data
        union {
            struct {
                void * buf2; // pointer to out-of-line data
                ulong capacity; // capacity of out-of-line data
            };
            char data[16]; // in-line data, if size <= 0x10
        } data;
    } dbuf;
    struct myfs_leaf * next; // linked list of leaf structures
    struct myfs_leaf * prev;
};
```

The binary protocol is a simple TLV (type-length-value) protocol, which supports several operations:

- 2: allocate a temporary buffer to prepare for a future file write
- 0: write file: must be preceded by a type 2 prepare operation
- 1: read file
- 3: make directory
- 4: make link (hard link or symlink)
- 5: copy file
- 6: remove file/directory (recursively)
- 7: change working directory
- 8: list working directory
- 9: get working directory
- 10: ping

## Exploitation

There are (at least) two bugs in the program:

1. When making a symlink (command 4) on top of an existing file, the dtype is not changed, leading to a type confusion: the symlink target (`char *`) will be interpreted as a `myfs_leaf *`.
2. When removing a regular file, the linked list containing all `myfs_leaf` structures will be iterated, and *any* structure matching the file's `leaf_id` will be deleted.

Bug number 1 leads to a straightforward write-what-where. We can create a fake `myfs_leaf` with `buf` pointing at the target memory; when we write 16 bytes or less to the file, they will be copied straight to `buf` without further checks (`size`, `buf2`, `capacity` etc. are not checked).

Bug number 2 can be exploited to gain UAF. `leaf_id` is generated with only 2 bytes from `getrandom`, so it has only 16 bits of entropy; thus, by the birthday paradox, it suffices to generate ~256 files to have a good chance of having two files with the same `leaf_id`. We can then delete the second file to also free the first file's `leaf`, allowing us to access the freed `leaf` from the first file.

We exploit the UAF to obtain a leak of a heap address. From there, we can use the arbitrary write (bug 1) to overwrite a data pointer for any file, and thereby gain an arbitrary read primitive; with arbitrary read + write, it becomes trivial to win. I chose to obtain the binary base, libc base, and a stack address (via `environ`), and then to write a ropchain to the stack; many other solutions are possible.

The full exploit is in [`exploit.py`](exploit.py); when run, we get a flag (most of the time): `codegate2024{7e412d247dfcc6fa024740fda129afe58b816107893d3ec44e14f2c9efb321624f84b019b5ba1134f61dac6281570363cb208cc65c}`.
