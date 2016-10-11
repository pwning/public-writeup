## Secret Holder - Pwn 100 Problem

### Description

Break the Secret Holder and find the secret.
nc 52.68.31.117 5566

(link to binary)

### Overview

Secret Holder is an x86-64 ELF (NX, partial RELRO, no PIE) implementing
a somewhat contrived secret keeping service. The service supports
storing three types of secrets, small (40 bytes), big (4000 bytes), and
huge (400000 bytes).

The user can modify and free secrets after adding them.

### Reversing

Since the code was pretty simple, I'll just give an approximate
decompilation with some details omitted here:

```c
char *g_big_secret;
char *g_huge_secret;
char *g_small_secret;
int g_have_big_secret;
int g_have_huge_secret;
int g_have_small_secret;

void keep_secret() {
  int type = read_choice();
  switch (type) {
    case SMALL:
      if (!g_have_small_secret) {
        g_have_small_secret = calloc(1, 40);
        g_have_small_secret = 1;
        read(0, g_have_small_secret, 40);
      }
     case HUGE:
        // same as above with size 400000
     case BIG:
        // same as above with size 4000
  }
}

void renew_secret() {
  int type = read_choice();
  switch (type) {
    case SMALL:
      if (g_have_small_secret) {
        read(0, g_have_small_secret, 40);
      }
     case HUGE:
        // same as above with size 400000
     case BIG:
        // same as above with size 4000
  }
}

void wipe_secret() {
  int type = read_choice();
  switch (type) {
    case SMALL:
      free(g_small_secret);
      g_have_small_secret = 0;
      break;
     case HUGE:
        // same as above
     case BIG:
        // same as above
  }
}
```

### Bug

`wipe_secret` does not check `g_have_*_secret`, so the same pointer can
be freed twice.

### Exploit

The `g_*_secret` pointers are laid out so that if `g_big_secret` and
`g_huge_secret` point to the same place, is possible to unlink a chunk whose
`fd` and `bk` pointers point to `&g_big_secret - 0x10` without failing forward
and backward link checks (note: it is not strictly necessary for `g_big_secret`
and `g_huge_secret` to be the same, since `fd` and `bk` can be adjusted so that
`&fd->bk == &bk->fd`).

```c
#define unlink(AV, P, BK, FD) {                                            \
    FD = P->fd;                                                               \
    BK = P->bk;                                                               \
    if (__builtin_expect (FD->bk != P || BK->fd != P, 0))                     \
      malloc_printerr (check_action, "corrupted double-linked list", P, AV);  \
    else {                                                                    \
        FD->bk = BK;                                                          \
        BK->fd = FD;                                                          \
        if (!in_smallbin_range (P->size)                                      \
            && __builtin_expect (P->fd_nextsize != NULL, 0)) {                \
            ...                                                               \
          }                                                                   \
      }                                                                       \
}
```

to get into this situation, we want to get into the state where `g_huge_secret`
points in front of an allocated `g_small_secret`:

```
+---------+------+
| big     |small |
+---------+------+-------+
| huge                   |
+--------------------+---+
```

 We then write write a fake malloc chunk with next and prev pointing to
`&g_big_secret - 0x10`, and overwrite `g_small_secret`'s malloc chunk, setting
`prev_inuse` to 0 so that when the chunk is freed via `g_small`, it will
consolidate backwards, unlinking the fake chunk. After `g_small_secret`'s
chunk, we place an additional chunk with `prev_inuse` set to prevent forward
consolidation.

```
+---------+------+
| big     |small |
+---------+------+--------------------+
| fake     fake_small fake_prev_inuse |
+--------------------+----------------+
```

At that point, we free `g_small_secret` and pass the unlink checks, resulting in:

```c
fake_chunk->fd->bk = fake_chunk->bk;
fake_chunk->bk->fd = fake_chunk->fd;
```

This has the effect of setting

```c
g_huge_secret = &g_big_secret - 0x10;
g_big_secret = &g_big_secret - 0x10;
```

Which we can turn into arbitrary write by editing `g_big_secret` to overwrite
`g_huge_secret` and `g_have_huge_secret` and editing `g_huge_secret`.

All that remains is to lay out `g_*_secret` in the required way.

We start by allocating and freeing `g_huge_secret`. This raises the dynamic
mmap threshold so that later huge allocations will be placed on the brk heap.

Next, we allocate and free `g_small_secret`, then allocate `g_huge_secret` to
consolidate fastbins. This places the `g_small` chunk back on the unsorted
list, then since `g_small_secret` is at the top of the heap, `g_huge_secret` is
placed at the same location as `g_small_secret`.

We free `g_small_secret` one more time, then allocate `g_big_secret` and
`g_small_secret`, which now occupy the same location as `g_huge`.  This results
in exactly the layout that we wanted above.

We get arbitrary write as described above, then overwrite `free`'s GOT
with `puts` to get a memory leak. By writing to `g_huge_ptr`, we can
call `puts` with an arbitrary argument by resetting `g_huge_ptr`. We use
this to leak `__libc_start_main`'s address, then use the same technique
to call `system("/bin/sh")`.

Unfortunately, we were too sleepy and busy to solve Sleepy Holder.
Sleepy Holder was identical to this problem, except that `g_huge_secret`
cannot be renewed or freed.

See
[exploit.py](https://github.com/pwning/public-writeup/blob/master/hitcon2016/pwn100-secret-holder/exploit.py)
for the full exploit.

As with other pwnables, this exploit was unreliable against the remote server
(in Japan) when sent from a machine in the US. To land this, we had to run the
exploit from a machine in Japan.
