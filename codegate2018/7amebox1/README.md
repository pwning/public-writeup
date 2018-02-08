## 7amebox1 - Pwnable Challenge

The 7amebox challenge is built on a custom VM written in Python (with
meaningless function names). The VM uses 7 bit bytes and three byte words with
"middle endian" byte order, presumably a reference to cLEMENCy from DEFCON 24.

To start, we annotated the VM implementation to use decent names and to
add basic disassembly and debugging functionality. See the files in this
directory for our modifications.

Disassembling the program, we see a trivial stack buffer overflow with a
hardcoded canary of 0x12345:

```asm
main:
   9:  push bp
   b:  mov bp, sp
   d:  sub.t sp, #3c
  12:  mov r5, bp
  14:  sub.t r5, #3
  19:  mov r6, #12345
  1e:  st.t r6, [r5]
  20:  mov r0, #cd # "name>"
  25:  call writestr
  2a:  mov r1, #42
  2f:  mov r5, bp
  31:  sub.t r5, #3c
  36:  mov r0, r5
  38:  call read
  3d:  mov r0, #d3 "bye\n"
  42:  call writestr
  47:  mov r5, bp
  49:  sub.t r5, #3
  4e:  ld.t r6, [r5]
  50:  cmp.t r6, #12345
  55:  jne #5
  5a:  mov sp, bp
  5c:  pop bp
  5e:  ret
```

The VM has no memory protections. Even though it appears to have a
configuration option to NX (which was disabled on this challenge), the
permission check is wrong:

```python
def check_permission(self, addr, perm):
    if self.get_perm(addr) & (PERM_MAPPED | perm):
        return True
    else:
        return False
```

The exploit overwrites the return address to point into the stack buffer. Our
flag reading shellcode didn't quite fit, so we used a stager to read larger
shellcode to the bottom of the stack.

Unfortunately, the time we spent adding debugging functionality was a waste as
we did not have enough time to exploit the rather convoluted bug in the second
challenge using this VM.
