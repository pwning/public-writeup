## PyProt3ct

We are provided with an obfuscated python file and a simple wrapper that calls into it with ```code``` and ```flag```. It returns true if the flag is correct, so we need to reverse the operations to determine the correct flag.

From the obfuscated code and the fact we are provided a file called ```code```, it is obvious that the obfuscated python implements a VM. We start by analyzing the functions that implement various opcodes and adding print statements based on their behavior, for example:

```
    OOOO0OOO0000O0000=O0OO0OOOOO0OOOOO0^OOO0OO000OOO0O0OO
    print 'xor [%s], %x, %x' % (mem_addr(O00O0OOO00O00OOO0), O0OO0OOOOO0OOOOO0, OOO0OO000OOO0O0OO)
    OOO00O0OO0000O000[O00O0OOO00O00OOO0]=OOOO0OOO0000O0000
```
```
    print 'call "%s", "%s"' % (OOO0OOO00O00O0OOO, O0O000O00O0O0000O)
    OO0OOOO000O00OOO0=eval(OOO0OOO00O00O0OOO)
    O00O0OO00000OOO0O=OO0OOOO000O00OOO0(O0O000O00O0O0000O)
    OO00OOO000OO00O0O[OOOOO0OO0OOOOO000]=O00O0OO00000OOO0O
```
```
    print 'beq %x, %x, %x' % (O0000O0OOO0O0OOOO, OO0O00OO0O0OO0000, OOO00OOOOO0000OO0)
    if OO0O00OO0O0OO0000==OOO00OOOOO0000OO0:
        OO000000OO0000000[O0OOO0OO0OOO00OO0]=O0000O0OOO0O0OOOO
```

Now when we run the wrapper, we get a trace that we can use to perform dynamic analysis without completely deobfuscating the python or building a real disassembler for the VM:

```
...
ld.int [k153], afa418dff9713a5
ld.int [k154], 3bd7108df4bb3e6d
add [k155], afa418dff9713a5, 3bd7108df4bb3e6d
ld.int [k156], 293ec57e400bd73
ld.int [k157], 1b28d3b808b4905
xor [k158], 293ec57e400bd73, 1b28d3b808b4905
...
```

As you can see from the trace, even the VM code is obfuscated with random constants and such. We can ignore this noise by focusing on the control flow (e.g. branches). For instance, if we provide a flag that is 100 characters, the end of the trace is:

```
beq 81608, 64, 8
ld.int [k3129], 0
ld.int [k3130], 19628b1465e7435
ld.int [k3131], f5d2ef9e80093cd0
ld.int [k3132], 243dc2ce758432d2
ld.int [k3133], 22fb721e939067e
beq 80abb, 243dc2ce758432d2, 22fb721e939067e
ld.int [k3134], ff7eae4cf9610a1
ld.int [k3135], c1e66e7933ddc8cc
ld.int [k3136], ea09687cf0e72548
add [k3137], 19628b1465e7435, ff7eae4cf9610a1
return [k3138], 0
:(
```

Clearly the flag length should be 8 so that we can pass this branch. Next, we can observe that the flag bytes are converted into a 64-bit number, for example with the flag string '01234567':

```
add [k3070], 3031323334353600, 37
```

Then this number is processed many times. It was fairly apparent that this was an encryption algorithm with 127 rounds. The relevant trace for the first round (minimized):

```
bgte 91b2d, 0, 7f
shr k3360, 3031323334353637, 32
xor [k3360], 30313233, ffc2bdec
add [k3360], cff38fdf, ffc2bdec
and k3360, 1cfb64dcb, ffffffff
and k3380, 3031323334353637, ffffffff
xor [k3380], 34353637, ffc2bdec
add [k3380], cbf78bdb, ffc2bdec
and k3380, 1cbba49c7, ffffffff
shl k3070, cbba49c7, 32
or k3070, cbba49c700000000, cfb64dc
and k3424, cbba49c7cfb64dcb, 7f
shr k3070, cbba49c7cfb64dcb, 7
shl k3424, 4b, 57
or k3070, 19774938f9f6c9b, 9600000000000000
and k3070, 979774938f9f6c9b, ffffffffffffffff
add [k3345], 0, 1
b 8bea8
```

We assume that ```0xffc2bdec``` represents some secret value, e.g. a key. Then the round can be described succintly as:

 - Split 64-bit input block into a 32-bit left half and 32-bit right half
 - On each half, XOR secret and then ADD secret
 - Swap left and right, and concatenate to form a 64-bit block
 - Rotate right 7 bits

This round is repeated 127 times to produce an output value. The output value is compared to ```0xd274a5ce60ef2dca```:

```
bgte 91b2d, 7f, 7f
bne 9230f, 2975a4126dacaa59, d274a5ce60ef2dca
...
return [k3496], 0
:(
```

The round is trivial to reverse, so we can produce a decryption algorithm:

```
S = 0xffc2bdec
CT = 0xd274a5ce60ef2dca

x = CT
for _ in xrange(127):
    # rotate left
    x = (x << 7) | (x >> 57)
    L = (x >> 32) & 0xffffffff
    R = x & 0xffffffff

    L, R = R, L

    L = (L - S) ^ S
    R = (R - S) ^ S

    x = ((L & 0xffffffff) << 32) | (R & 0xffffffff)

print hex(x)
```

The decryption result is the correct input flag:

```
0x6433346450593237
d34dPY27
```
