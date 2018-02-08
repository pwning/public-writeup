## CPU - Reversing Challenge

We are given a 64-bit ELF [binary](47bce5c74f589f4867dbd57e9ca9f808.zip) and an IP:port. From the 
strings in main, it is apparent that this challenge involves providing VM code to execute. We
also googled for some of the strings in the binary, and came across a 
[GitHub project](https://github.com/Hersh500/cpu/blob/master/cpu.c) whose code is similar to
our binary.

After aggressively labeling the various functions and global data in IDA, we started to audit
each instruction handler. The **syscall** handler stood out because it provides a way to
read and write to file descriptors and open files, perhaps a flag file. Unfortunately it is
guarded by a permission check: ```(r6, r7) == (*0x35000, *0x35004)```.

This leads us to the **load** memory handlers. We try to read from 0x35000, but it fails
because that area of memory is inaccessible to non-kernel code (e.g. us).

We try to ignore the exeception by using instruction 23, which allows us to configure the
system to ignore exceptions. While this prevents our program from dying, it does not
allow us to read the memory because the result is cleared to zero if an exception occurs.

Next, we look for other ways of reading memory. The cache instruction stands out because
it reads memory without any permission checks.

The first thing we considered was an uninitialized
memory vulnerability in the **cache\_add\_data** function. It uses malloc to allocate
cache lines without zeroing the contents, so if we can load the kernel data into a cache
line then evict it, the next cache line that is allocated will still contain our kernel
data. Unfortunately, this attack was impossible to pull off because the cache is too
big to be able to ever cause an eviction.

Finally, we realized that we can use the one byte read in the cache instruction that gets
the page index to leak one byte of kernel memory. We can load an address into the cache,
with the page index pointer targetting the memory we want to read. Then load each possible
memory address, and test whether there was a cache hit. This only works because the
**load** function will set register 14 to 0 for a cache miss and 1 for a cache hit, even
if there was a permission fault!

The remaining pieces of the exploit were straightforward. We use the clear cache
instruction between each memory leak to reset the cache to a pristine state. We concatenate
the leaked bytes into the r6 and r7 registers, then use the syscall instruction to read
the flag file and write it to fd 1.

The complete exploit is included as [exploit.py](exploit.py).
