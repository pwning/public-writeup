## poe (part 1, luna)

We are given a statically linked x86-64 Linux ELF implementing an
menu-based "editor" with text buffer and cliboard operations.

The editor supports multiple text buffers (which it calls Tabs), with
the following structure:


```c
struct Tab {
  unsigned long length;
  int cord_handle;
  bool cache_empty;
  char* cache;
};
```

The clipboard is also represented as a Tab.

the contents of a Tab are stored either in the process's memory
("cache") or in the kernel, via a custom cord kernel module.

### Vulnerability

The cut operation does not handle the case where the contents of the
clipboard prior to the cut are "cached". In that case, the cut operation
updates the length of the clipboard to length of the cut string without
updating the clipboard's cache pointer. If the clipboard is then pasted
into a new tab, that buffer can be written out of bounds.

This gives arbitrary read/write.

### Exploit

The most difficult part of this challenge was interacting with the
qemu instance, which appeared to pipe qemu (and it's tty handling)
directly over a socket.

We initially developed and exploit which used the arbitrary read/write
to find the stack and overwrite a return address with a ROP chain.
However, this was thwarted by our inability to send an 0x7f byte qemu's
TTY handling, which we wanted to do to determine the offset between
environ and a useful stack frame.

After failing to do this for a long time, we rewrote the
exploit to overwrite `free_hook` with `scanf` in order to overwrite a
saved rbp to pivot the stack.

This gave us an exploit that worked locally against. However, it would
time out when we attempted to run it against the remote server. We
needed to work around this by running the exploit from a cloud machine
in Asia.

`hitcon{achievement: Defeat Luna}`
