# LACUCARA_VM - Rev, 805 points (5 solves)

_Writeup by [@nneonneo](https://github.com/nneonneo)_

Description:

> Did you know that a month ago was BASIC's 60th birthday? (Note: In Korea, a 60th birthday is called “Hwangap” and has a special meaning). To celebrate, I've created a challenge using the BASIC language. Have fun!
> 
> for_user.zip

We're provided with a Windows binary called `encryptor.exe`, a redacted 64-byte flag, and `output.txt` - presumably, output from running the program with the real flag.

## Reversing the Windows Binary

The program relies heavily on OLE Automation ([oleauto.h](https://learn.microsoft.com/en-us/windows/win32/api/oleauto/) and oleaut32.dll) functionality, particularly Variants and Safe Arrays.

It implements an interpreter for a virtual machine (not surprising, given the name). The key functions are 0x442e36 (`vm_load`), which loads the virtual machine program (as a series of nine functions) and sets the initial state, and 0x44e2a2 (`vm_run`), which executes the VM. `vm_run` runs the VM one instruction at a time by calling 0x44af2b (`vm_step`), which is the function that actually implements all of the instructions.

The program allocates four `SAFEARRAY`s for the VM: a program array, memory array, stack array and register array. The program array is formatted as an array of `int[4]`s (i.e. each instruction is 4 32-bit ints); every other array is just an array of `int`s. There are 25 supported instructions, each with up to four different address modes. The format of each instruction is `[address_mode, opcode, operand1, operand2]`, where `operand1` usually refers to the destination register, and `operand2` is interpreted according to the address mode.

The operations map very closely to x86 instructions, so I extracted the program by using a debugger ([`prog.py`](prog.py)), and wrote a little disassembler that uses mostly Intel syntax ([`disas.py`](disas.py)). This produces the disassembly in [`disas.txt`](disas.txt).

## Reversing the VM

I used a regular expression to transform the idiom `push rX; op rX, Y; mov rZ, rX; pop rX` into a three-operand `op rZ, rX, Y`, which substantially simplifies the code, cutting it down by about 40%. The filename suggests that this is an encryption algorithm, and indeed several of the functions appear to perform bit permutation or substitution operations (S-Box substitutions); I named them in [`disas.annotated.txt`](disas.annotated.txt). The entry point for the VM program is the `main` function.

The algorithm starts with values in registers r0 through r5. r0 and r1 are random values which are printed to `output.txt`; r2 and r3 contain 64 consecutive bits of the flag; and r4 and r5 are constants (`LACU` and `CARA` in ASCII). All of the top-level permute/substitute functions (f3, f6, f7, f8) operate on 64-bit quantities expressed as register pairs, and are invertible. The logic of the main function looks like this:

```python
r0 ^= r4 ^ r2
r1 ^= r5 ^ r3
r0, r1 = f6(r0, r1, 0)
r0, r1 = f3(r0, r1)
r0, r1 = f7(r0, r1)

r0 ^= r4 ^ 0x3707344
r1 ^= r5 ^ 0x13198a2e
r0, r1 = f6(r0, r1, 0)
r0, r1 = f3(r0, r1)
r0, r1 = f7(r0, r1)

[...]

r0 ^= r4 ^ 0xe0e3610d
r1 ^= r5 ^ 0x64a51195
r0, r1 = f8(r0, r1)
r0, r1 = f3(r0, r1)
r0, r1 = f6(r0, r1, 16)

r0 ^= r4 ^ 0xca0c2399
r1 ^= r5 ^ 0xd3b5a399
r0, r1 = f8(r0, r1)
r0, r1 = f3(r0, r1)
r0, r1 = f6(r0, r1, 16)

r16 = ((r3 << 31) & 0xffffffff) | (r2 >> 1)
r18 = ((r2 << 31) & 0xffffffff) | (r3 >> 1)
r0 ^= r16 ^ r4 ^ (r3 >> 31) ^ 0xc97c50dd
r1 ^= r18 ^ r5 ^ 0xc0ac29b7
return (r1 << 32) | r0
```

It consists of several rounds of invertible permutations and substitutions, followed by a step which combines the final `r0, r1` with the initial `r2, r3`. Normally, the non-linearity of S-boxes would make the final `r0, r1` a non-linear function of `r0, r1, r2, r3, r4, r5`, making recovering the inputs hard without knowing `r2, r3` (the flag).

However, in our case, the S-boxes are `[4, 7, 2, 1, 8, 0xb, 0xe, 0xd, 0xf, 0xc, 9, 10, 3, 0, 5, 6]` and `[0xd, 3, 2, 0xc, 0, 0xe, 0xf, 1, 4, 10, 0xb, 5, 9, 7, 6, 8]`, which happen to be perfectly linear functions of their input bits. Linear here means that `S(x) = S(0) ^ S(x & 1) ^ S(x & 2) ^ S(x & 4) ^ S(x ^ 8)` for all `x`.

Since bit permutations (any combination of only `shl`/`shr`, `xor`, `and`, `or`) are always linear, the linearity of the S-boxes means that the entire encryption operation collapses to a linear computation. That is, we can express the operation mathematically as a matrix multiply: `(r0', r1') = M1 * (r0, r1) ^ M2 * (r2, r3) ^ C` when working with the bits in GF(2).

That in turn makes it trivial to invert, since we can just calculate `(r2, r3) = M2^{-1} * ( (r0', r1') ^ C ^ M1 * (r0, r1)`. This is implemented in [`solve.py`](solve.py), using my [`gf2.py`](https://github.com/nneonneo/pwn-stuff/blob/master/math/gf2.py) library for solving the linear equations. With this script, we get our flag: `codegate2024{B45IC_i5_n07_d34d_4nd_n3v3r_wi11_b3_2024_MQCJAb4Wr}`
