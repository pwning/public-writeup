## Ropsynth—Binary 400

### Description

The ropsynth challenge prompted competitors to rapidly solve 5 randomized instances of the same ROP exploitation exercise. (It was not a single binary; it was a Python harness around a C tool that enforced that you play the challenge as intended).

This exercise was to write an open/read/write ropchain, from a specific provided pool of gadgets. These gadgets were exactly the `pop rdi/rsi/rdx` & `syscall` & `push rax` you'd want, except that each gadget also popped additional values off the stack and asserted that they matched randomized constants (lightly obfuscated with random `sub`/`add`/`xor`s).

Here's an example of the `pop rdx` gadget from a particular instance:

```
32d: pop    %rdx              # <- The gadget. Addr gets randomized
32e: pop    %r13              # ⎫
330: sub    $0x1891cd04,%r13  # ⎪
337: sub    $0x6f00ddf3,%r13  # ⎪
33e: add    $0x42619004,%r13  # ⎪
345: add    $0x49db471a,%r13  # ⎬ <- A check you have to pass
34c: xor    $0x3ba35b5a,%r13  # ⎪
353: sub    $0xbe4fa50,%r13   # ⎪
35a: cmp    $0x5080daf5,%r13  # ⎪
361: je     0x366             # ⎭
363: hlt                      #
364: hlt                      #
365: hlt                      #
366: pop    %r11              # ⎫
368: xor    $0xacd07b7,%r11   # ⎪
36f: xor    $0x7c768982,%r11  # ⎪
376: xor    $0x629e3aee,%r11  # ⎪
37d: add    $0x667ef815,%r11  # ⎪
384: sub    $0x3733733f,%r11  # ⎬<- Another check
38b: add    $0xa17c5cf,%r11   # ⎪
392: add    $0x52f35cbd,%r11  # ⎪
399: xor    $0x1eae6ffb,%r11  # ⎪
3a0: cmp    $0x21bc6ae0,%r11  # ⎪
3a7: je     0x3ab             # ⎭
3a9: hlt                      #
3aa: hlt                      #
3ab: pop    %rcx              # ⎫
3ac: add    $0x4bbb4e0,%rcx   # ⎪
3b3: add    $0x5c3fad54,%rcx  # ⎪
3ba: add    $0x7649fb35,%rcx  # ⎪
3c1: add    $0xa6df2ff,%rcx   # ⎬ <- Yet another check
3c8: xor    $0x5bc9474,%rcx   # ⎪ (IIRC the number of checks per
3cf: sub    $0x1ffa6009,%rcx  # ⎪  gadget is not consistent
3d6: xor    $0x5bb89590,%rcx  # ⎪  between problem instances)
3dd: cmp    $0x6bbfa733,%rcx  # ⎪
3e4: je     0x3e8             # ⎭
3e6: hlt                      #
3e7: hlt                      #
3e8: retq                     # <- The subsequent return
```

Because of the time-limits in the challenge harness, the only viable solution was to automate the generation of a suitable rop payload from the provided gadget buffers. (That is, assuming the challenge harness itself could not be exploited. It did a bunch of chroot/seccomp/setuid/munmap stuff that looked safe to me, though).

(Note that all the `hlt`s and the fact that you need to solve 5 instances in a row means that looking for unintended gadgets within the random values probably isn't going to work.)

### Solution

Although the ROP buffer is randomized, it always has the gadgets you need to do:

```
fd = open(buf, O_RDONLY)
nbytes = read(fd, buf, 100)
write(STDOUT_FILENO, buf, nbytes)
exit(0)
```

(Helpfully, the challenge provides an R/W buffer `buf == 0x00a00000`, which initially contains the filename you're supposed to read.)

The checks that come after each gadget always take some randomized form of `pop`–`add`/`sub`/`xor`–`cmp`–`je` (and the `pops` only use registers that don't interfere with your syscalls), so parsing the asm to generate a value that passes the check is straightforward to do directly.

That's about it. Our challenge solution is attached in solve.py, which if nothing else serves as a basic CTF example of using capstone and z3py :)
