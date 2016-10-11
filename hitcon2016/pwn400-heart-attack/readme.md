## Heart Attack - Pwn 400 Problem

### Description

Let's play Heart Attack together!
nc 52.68.31.117 22222

(link to binary and libc)

### Overview

Heart Attack is a x86-64 ELF (NX, full RELRO, PIE) implementing a multi-player
[Heart Attack](https://en.wikipedia.org/wiki/Slapjack) card game. The game
allows multiple players to connect, send messages to each other, and play heart
attack (optionally with AI players).

### Reversing

For the purpose of the exploit, the main point of interest is the chat
functionality. The program implements multi person chat using a per-connection
unix sockets and a shared memory section for IPC.

The program allows a player send messages to other players that are connected.
Messages are also logged in each process, and the log can be viewed, or
individal logged messages deleted.

Logs are stored in the following structure:

```cpp
struct message {
  struct message *next;
  char *text; // malloced buffer containing message text
  char dest_name[16];
  uint32_t dest_id;
  uint32_t received;
};
```

The code for sending a message looks like:

```cpp
struct message *g_messages;

struct message *new_message(unsigned int len) {
  struct message *msg = calloc(1, *msg);
  ...
  msg->buf = calloc(1, len);
  ...
  msg->next = NULL;
  if (g_messages == NULL) {
    g_messages = msg;
  } else {
		struct message *iter;
		for (iter = g_messages; iter->next; iter = iter->next);
		iter->next = msg;
	}
	return msg;
}

void do_msg(int fd, int id, unsigned int len) {
  ...
  int read_len = 4096;
	if (len <= 0xfff && len) {
		read_len = len;
	}

	struct message *msg = new_message(read_len);
  ...
	read(fd, msg->buf, read_len);
	terminate_newline(msg->buf);
	msg->buf[read_len - 1] = 0;
  ...
}
```

where `terminate_newline` is:

```cpp
void terminate_newline(const char *str) {
 for (size_t i = 0; i < strlen(str); ++i) {
	 if ( str[i] == '\n' ) {
		 str[i] = '\0';
		 return;
	 }
 }
}
```

### Bug

After the `read` call in `do_msg`, `msg->buf` is not guaranteed to be null
terminated. As a result, `terminate_newline` can iterate past the end of the
buffer and replace an 0xa byte with 0x0 out of bounds.

### Exploit

We have quite a lot of flexibility, as we can make allocations of any size up
to 0x1000 with controlled data (only restriction being that a newline cannot
occur before a null byte). We also have the ability to free these allocations
at any time.

To start with, we allocate some messages of size 0x28 (which is the same size
as `struct message`). We can free them at any time to populate the appropriate
fastbins so that allocations of `struct message` come from the fastbin instead
of interfering the allocations we make for the exploit.

Next, we setup the following layout:

```
+--------+-----------+-----------------------+
| guard1 | overwrite | target | top | guard2 |
+--------+-----------+-----------------------+
```

The guard allocations prevent unwanted consolidations when freeing
`overwrite` and `top`.

We make `target` 0xae8 bytes large so that the `size` field in the malloc chunk
header will be 0xaf1. Next, we free `target` and `overwrite`:

```
                    |------- 0xaf0 -------|
+-------------------+---------------------+-----+
| overwrite (freed) | 0xaf0 target(freed) | top |
+-------------------+---------------------+-----+
```

Now, we reallocate `overwrite` and trigger the bug by filling the entire buffer with As:

```
            |------------ 0xaf0 ------------|
+-----------+-------------------+-----------+-----+
| overwrite | 0xf0 target(freed)| untracked | top |
+-----------+-------------------+-----------+-----+
```

This zeros the 0xa in `target`'s `size` field, shrinking `target`'s malloc
chunk to 0xf0 bytes. The remaining 0xa00 bytes that used to be part of the
`target` chunk is now untracked by the allocator.

Next, we fill the shrunken `target` chunk with two smaller blocks, `partial1`
(0x80) and `partial2` (0x50):

```
            |------------- 0xaf0 -------------|
+-----------+----------+----------+-----------+-----+
| overwrite | partial1 | partial2 | untracked | top |
+-----------+----------+----------+-----------+-----+
```

We free `partial1` (which is still a smallbin allocation):

```
            |----------------- 0xaf0 ----------------|
+-----------+-----------------+----------+-----------+-----+
| overwrite | partial1 (freed)| partial2 | untracked | top |
+-----------+-----------------+----------+-----------+-----+
```

Now, we free `top`. `top`'s `prev_size` field is still 0xaf0, which was set the
very first time we freed `target`. As a result, top consolidates backwards and
overlaps `partial2`.

```
            |----------------- 0xaf0 ----------------|
+-----------+-----------------+----------+-----------+-----+
| overwrite |                 | partial2 |           |     |
+-----------+-----------------+----------+-----------+-----+
| overwrite | top (freed)                                  |
+-----------+----------------------------------------------+
```

We have now overlapped a large free block with an allocated block, but
this isn't useful yet, as we don't know any addresses. Now, we turn to
leaking libc.  Log messages are printed via a format string with `%s`,
so we need to place a libc address precisely at the start of an
allocated log buffer (in this case, `partial2`).

First, we reallocate `partial1` (0x80) out of the `top` chunk:

```
            |----------------- 0xaf0 ----------------|
+-----------+-----------------+----------+-----------+-----+
| overwrite |                 | partial2 |           |     |
+-----------+-----------------+----------+-----------+-----+
| overwrite | partial1        | top (freed)                |
+-----------+-----------------+----------------------------+
```

Next, we make an allocation of the same size as `partial2`. This allocation,
called `partial2_2` perfectly overlaps `partial2`.

```
            |------------------ 0xaf0 -----------------|
+-----------+-----------------+------------+-----------+-----+
| overwrite |                 | partial2   |           |     |
+-----------+-----------------+------------+-----------+-----+
| overwrite | partial1        | partial2_2 | top (freed)     |
+-----------+-----------------+------------+-----------------+
```

Now, we free `partial2_2`. Since `partial2_2` is fastbin-sized (0x50), it gets
placed into a fastbin. Fastbins are singly linked, withe next pointer occuring
immediately after the chunk's size field where the user data would normally go.
The next field is always either NULL or a heap address, so this does not give a
libc address. However, by making a large allocation (0x1000), we can trigger
fastbin consolidation, which removes fastbin entries and links them back into
the unsorted list. This places a pointer to libc into the very beginning of
`partial2`'s user data, which we read out by printing the chat log.

Now that we have a libc address, we try to control rip by overwriting
`__malloc_hook` in libc. Luckily for us, there is a misaligned 0x7f qword
before `__malloc_hook` in memory which makes it eligible to be returned from a
fastbin allocation of size 0x68.

At this point, we take advantage of our ability to overlap `partial2`. Once
again, we free `partial1`, returning us to this original state:

```
            |----------------- 0xaf0 ----------------|
+-----------+-----------------+----------+-----------+-----+
| overwrite |                 | partial2 |           |     |
+-----------+-----------------+----------+-----------+-----+
| overwrite | top (freed)                                  |
+-----------+----------------------------------------------+
```

We allocate a 0x300 block, `overlap`, out of top (chosen to be small to avoid
further fastbin consolidation). We fully overwrite `partial2`'s chunk with a
fake fastbin chunk of size class 0x70.

```
            |----------------- 0xaf0 ----------------|
+-----------+-----------------+----------+-----------+----------+
| overwrite |                 | partial2 |           |          |
+-----------+-----------------+----------+---+----+--+----------+
| overwrite | overlap           fake fastbin      | top (freed) |
+-----------+-----------------+--------------+----+--------------+
```

Now, we free `partial2`, which places our chunk, now called `fb1` into the
fastbin.

```
            |------------------ 0xaf0 ------------------|
+-----------+-----------------+--------------+----------+---------+
| overwrite |                 | fb1 (free)   |          |         |
+-----------+-----------------+--------------+------+---+---------+
| overwrite | overlap           fake fastbin        | top (freed) |
+-----------+-----------------+--------------+------+-------------+
```

Once again, we free `overlap` and reallocate it, this time overwriting
the next pointer of `fb1` with the a fake fastbin chunk before
`__malloc_hook`.

Finally, we we make two allocations of size 0x68. The first allocation is
located at `fb1`, and sets the head of the fastbin to `fb1`'s next pointer (the
`__malloc_hook` chunk).

The second allocation, `fb2`, returns an address shortly before
`__malloc_hook`. We control the data written to this allocation, so we can
control rip the next time `malloc` is called.

Since the program is a fork/accept service, a single libc gadget does not
suffice. Looking through the game code, we see that the main menu reads 1024
bytes into a stack buffer. We found one code path (the card printing
functions) that leads to a `malloc` call further down in the call chain
without zeroing this buffer. To reach this code path, we just need to
create a room, start a game, and send a newline (to flip a card).

We set `__malloc_hook` to an `add rsp, large; ret` gadget, then ROP to call
`system("/bin/bash -i <&4 >&4");`.

See
[exploit.py](https://github.com/pwning/public-writeup/blob/master/hitcon2016/pwn400-heart-attack/exploit.py)
for the full exploit.

For some reason (perhaps partial reads), despite having a reliable local
exploit, the exploit did not work against the remote server (in Japan)
when sent from a machine in the US. To land this, we had to run the
exploit from a machine in Japan.
