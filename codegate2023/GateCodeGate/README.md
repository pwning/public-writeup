# GateCodeGate (rev, 901 points)

Solved by @f0xtr0t, @5w1Min, @ubuntor.
Writeup by @f0xtr0t.

## Challenge Overview

We're given a [stripped x86-64 ELF executable](./main.xz). It accepts a string
at stdin, and then prints "wrong". Presumably, our job is to pass a valid string
that will be accepted.

## Solution

@5w1Min recognized that the whole binary is just a massive `main` function which
calls out to a collection of operations (and/or/not/shl/...), but that there is
no real control flow at play; it is purely a huge computation. 

All the operations were happening on 32-bit values, and likely this could be
solved by some form of symbolic execution.

After annotating a little bit, she handed me (@f0xtr0t) [an assembly
dump](./gatecodegate.asm.xz), while working trying to see if angr might work
on this challenge.

I wrote up a short little [Python script](./solv.py) that parsed the lines,
worked on a symbolic set of registers (and stack variables, which I also marked
as just being registers with weirder names), and applied the symbolic
operations. Then it passed off the entirety of it to z3 to be solved.

Picking only the most interesting bits here (see the [whole file](./solv.py) for
the full ~90 LoC solver):

``` python
registers = {
    x: BitVec(x, 32)
    for x in [
        "eax",
        "ebx",
        ...
        "[rsp+1C8h+var_64]",
        "[rsp+1C8h+var_68]",
    ]
}

gates = {
    "gate_and": lambda x, y: x & y,
    "gate_or": lambda x, y: x | y,
    ...
}

for line_num, line in enumerate(code):
    opcode = line[0]
    if opcode == "mov":
        dst = line[1]
        src = line[2]
        registers[dst] = getval(src, (line_num, line))
    elif opcode == "xor":
        dst = line[1]
        src = line[2]
        registers[dst] = registers[dst] ^ getval(src, (line_num, line))
    elif opcode == "call":
        gate = line[1]
        result = gates[gate](registers["edi"], registers["esi"])
        registers["eax"] = result
    else:
        raise Exception(f"Unknown opcode: {opcode}; {line}")


s = Solver()
s.add(registers["eax"] == 0)
print(s.check())
print(s.model())
```

After ~30 minutes of execution time, and 30+ GiB of RAM in constant use, it
still hadn't finished.

@ubuntor took the script, and switched out z3 to CVC5 ([full script](./solv_cvc5.py)):

``` diff
@@ -1,4 +1,7 @@
-from z3 import *
+import sys
+
+sys.path += ["/usr/local/lib/", "/usr/local/lib/python3.11/site-packages/"]
+import cvc5.pythonic as cvc5
 
 with open("./gatecodegate.asm", "r") as f:
     code = f.read()
@@ -13,7 +16,7 @@
 code = [x.strip() for x in code]
 
 registers = {
-    x: BitVec(x, 32)
+    x: cvc5.BitVec(x, 32)
     for x in [
         "eax",
         "ebx",
@@ -38,7 +41,7 @@
     "gate_xor": lambda x, y: x ^ y,
     "gate_not": lambda x, y: ~x,
     "gate_shl": lambda x, y: x << y,
-    "gate_shr": lambda x, y: LShR(x, y),
+    "gate_shr": lambda x, y: cvc5.LShR(x, y),
 }

.....
```

This completed in ~5 minutes, and used ~4 GiB of memory to do so.

Flage!
