## knote - Pwnable Challenge

We are given a 64-bit qemu image running a recent version of Linux with SMEP
and kASLR enabled. The machine is setup with a kernel module that supports
various actions on "notes" via ioctls on /dev/knote. Reversing the kernel
module, we see that it supports the following actions:

1) Add note
2) Delete note
3) Read note
4) Edit note buffer
5) Edit note time

Where a note is represented by the following structure:

```c
struct note_time {
  unsigned long year;
  unsigned long month;
  unsigned long day;
  unsigned long hour;
  unsigned long minute;
  unsigned long second;
};

struct note {
  struct note_time time;
  uint64_t epoch;
  uint64_t id;
  char *buf;
  struct hlist_node hlist_node;
};
```

Notes are stored in a hash table keyed by the epoch (in addition, each bucket
is sorted by epoch). In addition, the buffers for notes, which are always
exactly 1024 bytes large, are also stored in a separate red black tree. The
note reading/editing function only operate on buffers that are in this red
black tree. In addition, they calls `check_object_size` on a buffer before
using it. These two checks mean that overwriting the `buf` field in a `struct
note` does not immediately give arbitrary read/write.

We used two bugs:
1) The note buffer is never initialized. This allows leaking memory to defeat ASLR.
2) The The "edit note time" function operates on the hash table without taking
   any locks. For the most part, the other functions only perform operations under
   a global mutex.

To defeat ASLR, we allocate/delete a `struct tty_struct` (which falls into the
same size class as a 1024 note buffer) by opening and closing `/dev/ptmx`. We
then allocate a note buffer, which gets placed at the same address. Since the
buffer is never initialized, we can then read a kernel text pointer via `ops`
field of `struct tty_struct`.

To take advantage of the missing locking, we need to win a race condition.
First, we need to understand what editing a note time does. The high level flow
is:

```c
old_epoch = get_epoch(old_time);  // old_time provided by caller
new_epoch = get_epoch(new_time);  // new_time provided by caller
new_node = kmalloc(sizeof(struct note));
new_note->epoch = new_epoch;

old_node = find_node(g_hlist, old_epoch)
insert_node(g_hlist, new_node)
new_note->id = old_note->id;
new_note->time = new_time;
new_note->buf = old_note->buf;
old_note->buf = NULL;
// removes node from hash table, removes note->buf from rb tree if not null
put_note(old_node);
```

Deleting a note looks like:
```c
mutex_lock(&g_note_mutex);
old_node = find_node(g_hlist, old_epoch)
put_note(old_node);
mutex_unlock(&g_note_mutex);
```

While it was likely more straightforward and reliable to attempt to double-free
the 1024-byte `buf` member, we did this to the `struct note` itself instead.
Specifically, we attempt to trigger the following race, where E and D are
threads attempting to edit time and delete the same node:

```
E: insert_node(g_hlist, new_node);
D: put_note(old_node);
E: ...
E: put_note(old_node);
```

To improve reliability, we scheduled E and D on different CPUs, and tried to
make the first `insert_node` take a long time by inserting a lot of notes to
make the `g_hlist` bucket large.

The exploit starts an edit thread, which repeatedly attempts to edit the
time on a particular note. It then sleeps for 100ms, then starts a
delete thread that tries to delete that note. If neither the remove or
any of the edits fail, then we know that we have freed a note twice.
With this combination, we were able to win this race with OK
reliability.

At this point, we have freed a single `struct note` (size 0x58) twice.
Out of laziness, we exploited this in an extremely unreliable way, which
permanently corrupts the kmalloc free list for this size class.

First, we reallocate the note once, with an year value equal to an
address a little before the `modprobe_path` variable in the kernel. This
links the address into the SLAB allocator's free list, causing it to be
returned later by a call of `kmalloc` with the right size class.

Next, we use IPC message queue calls to allocate a `struct msg_msg` at
the address we just linked in.  This is a nice structure because its
length and a fair amount of the data are user-controlled (the
user-provided message payload is stored immediately after the
structure). We set the message data such that `modprobe_path` will be
overwritten by a shell script we placed in a writable directory.

Finally, we trigger a modprobe call by `execve`ing a binary whose first
4 bytes are nonprintable. When the kernel sees this, it attempts to load
a module for handling this unknown binary format. It does this by
running modprobe (based on the `modprobe_path` variable) as root.  This
conveniently gives us root privileges without needing to worry about
SMEP (or SMAP, had it been enabled). We setup our shell script to make
/root world-readable so that we can read the flag.

This exploit is incredibly unreliable because it leaves a kmalloc free
list in a very unhappy state. Since this was a CTF, we just ran this
(probably over 30 times) on the server until it worked without crashing
:-P
