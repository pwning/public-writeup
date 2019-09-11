# EBC
### Category: Reversing

The EBC challenge is a classical reverse engineering challenge where you are 
given a binary that validates the flag you give it. For this challenge we 
recieved a PE binary with machine type EBC, or EFI Byte Code -- a type VM 
language that runs in the EFI bootloader to allow creation of cross platform 
drivers.

## Reversing

Reversing this challenge was difficult because the ABI for native calls from 
EBC is not well documented and the call tables that allow these to work were 
not implemented in the VM's we found for running the binary. This mean that we 
were stuck statically guessing the meaning of external function calls, 
particularly print, read, flush, etc.

After deciding where input was recieved, we were able to focus on the input 
validation. From the input handling code and the final flag output, we were 
able to determine that the flag was "TWCTF{" + 32 characters + "}". Then 
validation algorithm was roughly as follows (where `hash` is an unknown native 
hash function call):

```
def validate(flag):
    f1, f2, f3, f4 = eight_byte_chunk(flag)

    validate_1 = xor_decrypt(g_xor_key, enc_validate_1)
    if validate_1(f1) is fail:
        return fail

    validate_2 = xor_decrypt(hash(f1), enc_validate_2)
    if validate_2(f2) is fail:
        return fail

    validate_3 = xor_decrypt(hash(f2), enc_validate_3)
    if validate_3(f3) is fail:
        return fail

    validate_4 = xor_decrypt(hash(f3), enc_validate_4)
    if validate_4(hash(f4), f4) is fail:
        return fail

    return success
```

As we can see, all of the validation steps are the same except the last chunk, 
which relies on both the last 8 bytes of the flag and its hash. This will be 
relevant later.

## Solution

Since the first xor key is stored as a global, we can use this to decrypt to 
the first validate function. Doing so gives:

```
MOVqw       R1, [SP+arg_0]
MOVIqq      R2, 0xFFFFFFFF95F628F2
MOVIqq      R3, 0xFFFFFFFFC6737B8B
MOVIqq      R4, 0x5D685155
MOVIqq      R5, 0xFFFFFFFFD2083355
MOVIqq      R6, 0xFFFFFFFFB2FF5134
MOVIqq      R7, 0xFFFFFFFFE369AB3D
ADD64       R1, R6
SUB64       R1, R5
MOVIqq      R7, 0xFFFFFFFFCBB452AE
XOR64       R1, R7
...
MOVIqq      R7, 0x3032FAED
CMP64eq     R1, R7
JMP8cc      success
MOVIqw      R1, 1
JMP8        fail
success:
MOVIqw      R1, 0
fail:
MOVqw       R7, R1
RET
```

Basically, we just do some math over the first 8 bytes of the flag and check 
that it is equal to some value. From this, we can translate to Z3 and solve for 
the flag input. This is especially easy because it is just straight line code 
(see convert.py).  The outputted Z3 code looks roughly like:

```python
v = BitVector(64)
R1 = v
R2 = 0xFFFFFFFF95F628F2
...
R7 = 0x3032FAED
solve.add(R1 == R7)
```

Using this, we get `f1` = 0x65376e315f434245 = `EBC_1n7e`.

We don't know the hash function to compute the xor key to decrypt the rest of 
the validate functions, however the first instruction is likely the same 
(`MOVqw R1, [SP+arg_0]`). We can use this to recover the xor key for the other 
functions and decrypt. The next two validation functions are the same as the 
first, with just a few new instructions added (shifts, muliplies, etc). We can 
use the same method as the first validate function to find next two flag chunks 
and find that `f2` = 0x5f72337465727072 = `rpret3r_` and `f3` = 
0x5f3364346d5f7331 = `1s_m4d3_`.

For the final 8 bytes, the validation function was slightly different. Instead 
of taking just the 8 flag bytes, it also took its hash.
The validation function validated both the hash and the flag bytes separately 
and returned true if both were correct. When, we tried solving for either one 
with Z3 we found that the equations were too satisfiable. Therefore, we needed 
both together to full constrain the last 8 bytes.

However, as mentioned above, the hash function is a native code call that we 
don't have access to. Based on its signature in the byte code (it takes a 
buffer and length), we can guess that it is some kind of string based hash. 
Additionally, we have access to hashed and unhashed pairs thanks to the 
recovered xor keys. After trying a few "hash" functions on these pairs, we 
found that it was CRC32. This allowed us to compute the hash on the Z3 
bitvector and constrain the two checksums against each other and find that `f4` 
= 0x6c346e303174706f = `opt10n4l`.

## Note

At some point, we realized that the numbers Z3 was giving us back were correct, 
but truncated. For example, instead of `EBC_1n7e` for `f1`, we got `EBC_`. This 
is because IDA's disassembly of the EBC instruction immediates was also 
truncated. At this point, we used `ebcvm` to do the disassembly of the 
decrypted sections. After this, Z3 gaves us the full 8 bytes for each chunk.

## Flag

`TWCTF{EBC_1n7erpret3r_1s_m4d3_opt10n4l}`

## Resources used
- IDA Pro
- Z3
- https://github.com/yabits/ebcvm
- http://vzimmer.blogspot.com/2015/08/efi-byte-code.html

## convert.py
```python
import sys

TRANSFORMS = {
    "MOVIqq": lambda a,b: "{} = {}".format(a, b),
    "MOVIqd": lambda a,b: "{} = {}".format(a, b),
    "MOVIqw": lambda a,b: "{} = {}".format(a, b),
    "MOVqw": lambda a,b: "{} = {}".format(a, b),
    "ADD": lambda a,b: "{} += {}".format(a, b),
    "SUB": lambda a,b: "{} -= {}".format(a, b),
    "XOR": lambda a,b: "{} ^= {}".format(a, b),
    "NOT": lambda a,b: "{} = ~{}".format(a, b),
    "NEG": lambda a,b: "{} = -{}".format(a, b),
    "AND": lambda a,b: "{} &= {}".format(a, b),
    "OR": lambda a,b: "{} |= {}".format(a, b),
    "SHR": lambda a,b: "{} = LShR({}, {})".format(a, a, b),
    "SHL": lambda a,b: "{} <<= {}".format(a, b),
    "MULU": lambda a,b: "{} *= {}".format(a, b),
    "CMPeq": lambda a,b: "solve.add({} == {})\nR1 = v".format(a, b),
}

def transform(op, arg1, arg2):
    return TRANSFORMS[op](arg1, arg2)

def do(s):
    z3 = []
    z3.append('v = BitVector(64)')
    z3.append('R1 = v')
    ls = s.split('\n')
    for l in ls:
        if l == '':
            continue
        op, arg1, arg2 = l.split()[-3:]
        arg1 = arg1[:-1]
        z3.append(transform(op, arg1, arg2))
    z3.append('solve.add(R1 == R7)')
    return '\n'.join(z3)

if __name__ == '__main__':
    print(do(open(sys.argv[1]).read()))
```
