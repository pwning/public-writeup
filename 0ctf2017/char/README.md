## char - Pwnable Challenge

We are given a 32-bit binary that maps the provided `libc.so` at
0x5555e000, then calls a function with a trivial buffer overflow. The
one catch is that the input is first validated - the program exits
immediately if the input contains any bytes outside of [0x20, 0x7f).

As a result, we have straightforward ROP, but are limited to gadgets
with valid addresses. Using a quick function to search for valid
gadgets, we found `pop edi; ret`, `pop esi; ret`, `pop ebp; ret`, and
`int 0x80` gadgets. This isn't enough to setup the arguments to a
syscall, so we noticed that `pusha; ret` and `popa; ret` gadgets were
present, and could be used to move values between registers by doing a
`popa` misaligned with a `pusha`.

The next challenge is that the string "/bin/sh" does not get mapped to a
good address. To get this, we try to build this address by adding valid
values together. we used the following gadgets:

```assembly
mask_and_ror:
  mov eax, [esp+4]
  and eax, 0xffff
  ror ax, 0x8
  ret

add_edx_eax:
  add eax, edx
  ret
```

The `mask_and_ror` gadget lets us us mask off the top 16 bits of a value
to get a small addend. We then use the `add_edx_eax` gadget to build a
pointer to "/bin/sh".

Using these, combined with the `pusha`/`popa` trick and an `inc eax; ret`
gadgets to set `eax` to 0xb, we manage to construct valid syscall arguments to
call `execve("/bin/sh", ptr_to_null, ptr_to_null)`;

```
flag{Asc11_ea3y_d0_1t???}
```
