## RedOs (pwn 160)

### Description

Here are some files to help you along.

Find the flag from /ctf/level2.server
There is a sample client in /ctf/level2.client (you may need to write
your own)

It is running on os-uedhyevi.9447.plumbing port 9447

### Reversing

Now, we are given the full setup for running the challenge, which
reveals that this is a custom kernel running under qemu. Reversing the
kernel, we see that there is a `ctf_drm` syscall (number 0x15) that
allows a flag to be read from the kernel (and then clears the flag from
kernel memory so that it can only be used once). The kernel runs an init
program which starts `ctf/level3 --silent` `ctf/level2.server --silent`
then finally `ctf/level1` the calculator program that gave us in calcpop
reloaded.

Reversing the level2 server, we see that after calling `ctf_drm` to load
the flag into memory, it calls the `shmap` syscall, which maps a page of
shared memory into the caller. This page is then available to be mapped
into any other userspace program. The server uses this shared memory to
implement some sort of IPC server.  Specifically, it checks a status
flag in the shared memory in a yield loop in order to determine when to
process a command. The format of the shared memory looks like this:

```
struct command {
  uint32_t cmd;
  uint32_t ready;  // when this is 1, the server handles the command.
  char key[8];
  char value[8];
};
```

The server implements a simple key/value store. It supports the
following commands:
 * Set a key/value
 * Delete an entry by key
 * Get the nth largest value
 * Get the value for a key.

The keys/values are stored in a 200-element array in the data section
(0x200000). The buffer where the flag is stored is immediately after
this array. 

Looking at the `get_nth_largest_value` functionality, we we see that it
sorts the array in place, then returns the nth element of the list
(where n is read from the shared memory). At the beginning of the
function, n is validated to be less than 200, but after sorting the
array, n is once again read from the shared memory, and data at that
index is returned back to the caller. If we can change n to be >200 in
between the two reads, we can leak the flag out.

### Exploit

To exploit this, I modified the calcpop reloaded exploit to run
arbitrary shellcode, then wrote some code to flip the value of n between
0 and 200 in a loop. This was sufficient to to leak most of the flag.
For reasons that I did not figure out, the 4 bytes of each 16 bytes I
attempted to leak were always zeroed. Luckily, those bytes were easy
enough to guess.

See
[double_fetch.py](https://github.com/pwning/public-writeup/blob/master/9447ctf2015/pwn160-redos/double_fetch.py)
and
[double_fetch.S](https://github.com/pwning/public-writeup/blob/master/9447ctf2015/pwn160-redos/double_fetch.S)
for the full exploit.

### Flag

`9447{i_hope_no_one_writes_code_like_this}`
