## 32world

As the name implies, the service is a x86-64 Linux binary that runs your shellcode after switching to the 32-bit capability segment. The challenge is non-trivial because the service uses a seccomp filter to prevent any system call that originates from code  within the first 4GB of memory (e.g. ```if ($ip >> 32) == 0, block syscall```).

Using david942j's seccomp-tools, we can disassemble the bpf filter:

```
 line  CODE  JT   JF      K
=================================
 0000: 0x20 0x00 0x00 0x0000000c  A = instruction_pointer >> 32
 0001: 0x15 0x00 0x01 0x00000000  if (A != 0x0) goto 0003
 0002: 0x06 0x00 0x00 0x00000000  return KILL
 0003: 0x06 0x00 0x00 0x7fff0000  return ALLOW
```

And with objdump we disassemble the stub that is prepended to your shellcode:

```
   0:   eb 42                   jmp    0x44
   2:   5e                      pop    rsi
   3:   48 31 c0                xor    rax,rax
   6:   48 31 db                xor    rbx,rbx
   9:   48 31 c9                xor    rcx,rcx
   c:   48 31 d2                xor    rdx,rdx
   f:   48 31 ed                xor    rbp,rbp
  12:   4d 31 c0                xor    r8,r8
  15:   4d 31 c9                xor    r9,r9
  18:   4d 31 d2                xor    r10,r10
  1b:   4d 31 db                xor    r11,r11
  1e:   4d 31 e4                xor    r12,r12
  21:   4d 31 ed                xor    r13,r13
  24:   4d 31 f6                xor    r14,r14
  27:   4d 31 ff                xor    r15,r15
  2a:   48 31 e4                xor    rsp,rsp
  2d:   48 89 fc                mov    rsp,rdi
  30:   48 31 ff                xor    rdi,rdi
  33:   67 c7 44 24 04 23 00    mov    DWORD PTR [esp+0x4],0x23
  3a:   00 00
  3c:   67 89 34 24             mov    DWORD PTR [esp],esi
  40:   48 31 f6                xor    rsi,rsi
  43:   cb                      retf
  44:   e8 b9 ff ff ff          call   0x2
```

The code zeroes all of the registers and switches to a new stack that is also zeroed. Then it pushes the x86 compatibility segment and 32-bit eip on to the stack, followed by a retf. After this point, we will be executing our 32-bit code.

The first step for our shellcode to bypass the seccomp filter is to switch back to 64-bit land.

```
  push 0x33
  call do_retf
  ... # 64-bit code here
do_retf:
  retf
```

Then, we need to find a pointer to some 64-bit code, which is difficult because the location of our stack and 32-bit code is randomized, and the original binary and its libraries are randomized due to ASLR. However, the fs segment register was not zeroed.

We start by reading the first pointer in the fs segment. This is always a pointer to the fs segment data. Then we used gdb to find a libc address that was at some offset from the fs segment data, e.g. ```*(fs:[0] - 0x58)```. Once we have a pointer to within libc, we can calculate the address of a one-shot gadget that gives us a shell.

At this point, it is as simple as jumping to the one-shot gadget. Since it is in libc, it will pass the checks in the seccomp filter.