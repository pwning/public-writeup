## WtfOs (pwn 360)

### Description

Use the same files as in RedOs

Find the flag from level3.

It is running on os-uedhyevi.9447.plumbing port 9447

### Reversing

The level3 binary simply calls `ctf_drm` to read the flag into memory,
then exits. Thus, we need to reverse the kernel to figure out how to
somehow leak this back. After spending several hours looking for code
exec bugs in the kernel, a hint was released basically spelling out the
exact solution (which for this problem, did not involve code exec).
Looking at the code for exiting a process, we see that it does not zero
freed pages. The page allocator scans through a bitmap looking for an
unallocated page, starting the iteration where it left off last time. By
repeatedly calling the `shmap` syscall, we can eventually cause the page
containing the flag to be allocated back to our process, and read the
flag out from there.

### Exploit

See
[double_fetch.py](https://github.com/pwning/public-writeup/blob/master/9447ctf2015/pwn160-redos/double_fetch.py)
and
[leak.S](https://github.com/pwning/public-writeup/blob/master/9447ctf2015/pwn360-wtfos/leak.S)
for the full exploit.
