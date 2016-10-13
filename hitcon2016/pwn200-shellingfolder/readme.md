## ShellingFolder – Pwn 200

This challenge is a standard remote x86-64 pwnable, with all protections on (NX, PIE, canaries, and full relro). A libc.so was provided (as with most other chals this CTF, the platform is just Ubuntu 16.04).

Despite the service being themed after folder & file creation, it does not do any filesystem i/o; it just manipulates structs on the heap.

### Reversing

The program allows you to manipulate a tree of allocated structs that represent a directory hierarchy. The struct is:

```
struct obj {
  struct obj *children[10]; // these are just left null for files
  struct obj *parent;
  char name[32]; // size limit is 31 on entry; cannot be edited.
  int64_t size; // User chooses size of files on creation
                 // Folders get sum of child sizes upon request.
  int32_t is_folder; // Set to 1 if obj represents a folder, 0 for file.
  char padding[4]; // unused
};
```

The only relevant function is in `sub_1334`, the "6.Caculate the size of folder" function, that we can call on a directory we've set up.

```
void sub_1334(obj *folder) {
  // I've left out printf()s and other things.
  char stackbuf[24] = {0}; // This buffer is too small!
  int64_t *ptr = 0; // Comes right after stackbuf

  for(int i = 0; i <= 9; i++) {
    if(!folder->children[i]) continue;
    ptr = &folder->total_size;
    register char *name = dir->children[i]->name; // We control 31 bytes of name.
    memcpy(stackbuf, name, strlen(name)); // This call can clobber ptr.
    if(!folder->children[i]->is_folder)
      *ptr += folder->children[i]->size; // We control the size (as an int32_t).
  }
}
```

### Exploiting

In `sub_1334`, because we can control `name` to be a string of up to 31 bytes, we can get the `memcpy` to overwrite `ptr`. Then, a value we control is added to `*ptr`. If this were just an arbitrary write primitive, we'd be stuck because 64-bit ASLR with PIE prevents us from knowing any writeable locations before getting a leak; however, we can choose to to a partial overwrite of `ptr`, to get a (not-quite-deterministic) heap-relative "arbitrary add" primitive.

By using a 25-character `name` to overwrite just the least significant byte of `ptr`, we can make it point into the `children` array of `folder`. This causes a child pointer to get incremented by `size` (which we control), and with a size like 200 we cause the child pointer to point to under-defined heap memory. The program has a "1.List the current folder" feature (to print out the `->name` of all child pointers), which will allow us to leak heap. By playing around in a debugger, we can find a suitable `size` value that will cause our leak to show a libc pointer.

(For those who were unaware: glibc malloc just tosses libc pointers on the heap. You'll need to play around with allocating and freeing things a bit first though, which fortunately shellingfolder lets us do as part of it's normal functionality.)

With this leak, we now know libc's base address and can target its data section with the `sub_1334` bug. There are a variety of convenient glibc function pointers to target. The attached exploit sets glibc's [`__free_hook`](https://www.gnu.org/software/libc/manual/html_node/Hooks-for-Malloc.html#index-_005f_005ffree_005fhook) to the address of `system()`, and then triggers a `free("/bin/bash")` to pop a shell.

Triggering a `free("/bin/bash")` is not totally trivial: shellingfolder only lets us free its folder/file objects, which unfortunately starts with the `->children` pointers rather than the `->name` we control. We already have the tool to hack around this: we apply the `sub_1334` bug yet again to increment a child pointer (like we did the first time). By incrementing a child pointer by 88 bytes, it now points directly at a `->name` field that we control; if we used the name `/bin/bash`, subsequent deletion of that file (with the "5.Remove a folder or a file" feature) will result in the `free("/bin/bash")` we need.

Due to heap non-determinism the attached `exploit.py` isn't fully reliable, but hey, a flag one out of every ten throws is still enough flag.
