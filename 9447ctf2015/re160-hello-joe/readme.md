## Hello, Joe - Reverse Engineering 160 Problem

### Description

We get a 64 bit binary and some weird text about Mario that doesn't make sense.
Popping things open in IDA, we notice a few odd subroutines which are kept as
memory and then copied and jumped to later. The addresses are `0x6010c5`,
`0x601625`, `0x601b05`, `0x602060`, `0x6025c5`, and `0x602ac5`; we call these
set1, set2, set3, set4, set5, and set6, respectively.

### Solution
We notice the binary runs a bit slow, and has these weird `rdtsc` things
scattered about which delay a bit. The first thing we try is to replace
those loops with effectively nops, and then use instruction counting. Sadly,
this stops working after recovering the prefix `9447{`. 

Looking a bit more closely, it seems that each of the functions we label
set1-set6 define some possible allowed sets of values for some of the
input bytes. Set6 just checks the obvious things, that the flag starts with
`9447{` and ends with `}`, so we ignore it and only pay attention to
the other functions. We decompile each of the functions using Hex-Rays,
and save the output in files named set1-set5. 

We then write a quick python script to parse through the C output and
give us a flag. We used Z3 for this because we're used to using Z3 for
CTF challenges, but this was actually much simpler than that.

```
from z3 import *

a = BitVecs(' '.join("a_%d"%i for i in xrange(38)), 4)
s = Solver()

def orr(index, vals):
  return Or(a[index] == vals[0], Or(a[index] == vals[1], a[index] == vals[2]))

for setn in xrange(1,6):
  set5 = open('set%d'%setn).read().split("\n")
  set5_vars = [x.split()[0] for x in set5 if '_BYTE' in x]

  #all but the last..
  for i, var in enumerate(set5_vars[:-1]):
    check = [filter(lambda y:y.startswith('0x'), x.split()) for x in set5 if (('==' in x) and ((var+" ") in x))]
    if check:
      vals = [int(chr(int(x,0)),16) for x in check[0]]
      print setn, i, vals
      s.add(orr(i, vals))

s.check()
print "9447{"+''.join(["%x"%s.model()[v].as_long() for v in a[5:-1]])+"}"
```

This gives us our flag: `9447{94ea5e32f2b5b37d947eea3a38932ae1}`
