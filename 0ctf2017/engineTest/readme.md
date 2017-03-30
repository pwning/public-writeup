## engineTest – Reversing

engineTest was a VM-keygenme style reversing challenge.

The engineTest binary is not strictly a VM interpreter. Rather, it seemed to be a model-finder for a given system of boolean logical equations.

### Solution

Even though engineTest is not strictly a VM interpreter, it can be solved like one. The second half of the program essentially executes a fixed sequence of boolean And/Or/Xor/Ite instructions (which are generated during the first half of program). 

Similar to many VMs (or real architectures), each of these instructions takes 2-3 source operands, performs its operation, and then stores the result into a destination operand. In memory, each instruction consists of 5 64-bit integers: the opcode (1 thru 4), 3 source operands (indexes into a global bit array; the third operand is -1 for all the 2-operand instructions, which is everything except Ite), and a destination operand (also an index into the global bit array).

I dumped the instructions using the following gdb script:

```gdb
set height unlimited
set width unlimited
b *0x402DD7
commands
x/5gx $rax
continue
end
run
```

Some casual playing around with the engineTest binary (and associated datafiles) shows that for most inputs, a "FAILURE" message gets printed. I checked the dumped instructions to see how this message was being constructed, and found that the last several instructions were all Ite instructions with bit 34792 as their condition operand, bits that spelt out "FAILURE" as their false operand, and bits that spelt out "SUCCESS" as their true operand.

So, we're looking for an input to the program such that after the bytecode executes, bit 34792 is left set. With some regexes, I transformed the gdb output into a python array '`trace[n][5]`', then applied the following z3py interpreter.

```python
from z3 import *

trace = eval(open('dump.txt').read())

maxidx = max(max(i) for i in trace)
bits = [Bool('x%d' % i) for i in range(maxidx+1)]
# This models the interpreter loop
for code, x, y, z, w in trace:
  if   code == 1: bits[w] = And(bits[x], bits[y])
  elif code == 2: bits[w] = Or(bits[x], bits[y])
  elif code == 3: bits[w] = Xor(bits[x], bits[y])
  elif code == 4: bits[w] = If(bits[x], bits[y], bits[z])
  else: assert False

S = Solver()
# Bit 34792 controls whether the VM bytecode prints a
# success or failure message.
S.add(bits[34792])
print S.check()

# Print the input that satisfies the constraint (i.e. the flag)
for i in range(2, 0x112, 8):
  x = 0
  for j in range(i, i+8)[::-1]:
    x <<= 1
    x |= int(str(m[Bool('x%d' % j)]) == 'True')
  if x != 0:
    print chr(x)
```
