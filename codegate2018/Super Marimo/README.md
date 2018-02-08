## Super Marimo - Pwnable Challenge

This service implements some sort of marimo management service. Marimos
can be created and edited. They are heap allocated, and their structure
is:

```c
struct marimo {
  int create_time;
  int price;
  char *name;
  char *profile;
};
```

`create_time` is initialized to `time()`, `price` is initialized to 1
and `name` and `profile` are heap allocated. A marimo's name/profile can
be printed, and its profile can be edited. When its profile is edited,
the number of bytes read into `profile` (without reallocating) is
computed as `32 * (time() - create_time + price)`. This is a trivial
heap buffer overflow.

The exploit does the following:

1. Create two marimos
1. Wait 3 seconds
1. Use the heap overflow to set the 2nd marimo's `name` to `puts`'s GOT
   entry and `profile` to `strcmp`'s GOT entry.
1. Show the 2nd marimo, leak `puts`, compute libc base.
1. Edit the 2nd marimo, set `strcmp`'s GOT to point to `system` (there
   is no RELRO).
1. Send /bin/sh, which is passed to `strcmp` (now `system`).
