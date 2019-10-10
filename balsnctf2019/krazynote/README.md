### Vulnerability

The global variables which stores the data relateed to the note is susceptible to race condition.

### Exploit

We use the race-condition by using userfault fd to handle the fault in `copy_from_user` while allocating a new chunk. In the fault handler, we reset the notes and allocate two chunks of small sizes such that the end of first allocation (whose fault we are handling) overlaps only the size (to make it 0xf0) and xor key for the second note. We also tried to do userfault on the second allocation write so that we can overwrite the key before it is used to to encrypt data for second allocation (however I failed at this, but somehow since that allocation happens in another thread, it works out as race most of the time :P). We also make the third allocation which is small enough that the chunk 2 overlaps with chunk 3 and further to have following layout

```
+--------+---------+---------+----
|chunk 1 | chunk 2 | chunk 3 |
+--------+---------+---------+----
         ^......................^
              chunk 2 after overwriting its size
```

Now we can do read on `chunk 2` to leak xor key and use that to get the `page_offset_base` difference with `chunk 3->buf` address. Since that is at constant offset from the array where all pointers to this chunks are stored, we overwrite the `buf` pointer of `chunk 3` to point it to the start of array (while doing this, we also overwrite xor key to `0x0` for easier memory read/write). Now we have memory leak and using that, we can calculate `page_offset_base` (this helps us in doing arbitrary kernel memory read/write). Use the leaked address of this chunks to get offset of `this_module` and leak the `modules` address which is part of kernel image. We then iterate through `init_task->tasks` linked list to get our current `task_struct` and then overwrite the uid/gid in our cred structure with 0 to get root.

**Flag:** `Balsn{Rac3_Rac3_Rac3_A_FLAG}`
