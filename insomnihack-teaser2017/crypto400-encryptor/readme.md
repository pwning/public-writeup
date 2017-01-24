## encryptor - Reversing/Crypto 400 Problem - Writeup by Robert Xiao (@nneonneo)

### Description

We need your skillz because one G**gle car has become mad and tries to kill as many pedestrians as possible. Fortunately, we have recovered an encryptor that it uses to protect its firmware thanks to a master key of type INS{...}. Please help us, implement the corresponding decryptor and recover the master key that can be found in the provided ciphertext.

### Solution

We are provided an [encryption program](encryptor) and a [ciphertext](ciphertext) file. The encryption program takes no parameters (i.e. no external key) so we "only" have to implement a decryption program.

Opening the program in IDA, we see that it's almost entirely AVX2 instructions, which IDA doesn't decompile. We'll have to attack the assembly directly. Below, a "yword" is a 256-bit (32-byte) quantity, named after the `ymmN` 256-bit AVX2 registers.

The `main` function has a fairly simple outer structure:

    load 19 constant ywords to [rbp-0x930..rbp-0x6d0] ("constants")
    load code bytes from the text section to [rbp-0xb50..rbp-0xad0] ("passkey")
    vzeroupper
    call func1 to generate keys in [rbp-0x6d0..rbp-0x50] ("keys")

    f = open("/tmp/plaintext")
    buf = f.read()
    while 1:
        block = buf[pos:pos+0x80]
        if len(block) < 0x80:
            break
        inblock = rearrange block with AVX2 instructions
        outblock = func2(inblock, keys, constants)
        buf[pos:pos+0x80] = rearrange outblock
        pos += 0x80

    open("/tmp/ciphertext", "wb").write(buf)

We can run the program in `gdb` and dump out the `constants`, `passkey`, and `keys` just before it reads the input file. Also, with a little bit of GDB sleuthing, we figure out that the block rearrangements just amount to reversing the 16-bit words in the block, i.e.

    00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F 10 11 12 13 14 15 16 17 18 19 1A 1B 1C 1D 1E 1F

becomes

    1E 1F 1C 1D 1A 1B 18 19 16 17 14 15 12 13 10 11 0E 0F 0C 0D 0A 0B 08 09 06 07 04 05 02 03 00 01

which is a self-inverting function. So, now all we have to do is reverse engineer `func2` (note that we didn't even look at `func1`, because it's only called to generate the `keys`). `func2` appears to take a single block of 0x80 = 128 bytes and encrypt it; no block chaining is used (so two consecutive identical blocks encrypt to the same identical output blocks).

----

`func2` is just a huge function with a normal function prologue and epilogue, with 625 AVX2 instructions in the middle - no jumps, conditionals, or even any non-AVX instructions in between. This seems like a super-daunting task to reverse - each instruction operates on 32 bytes of data, so plugging the whole mess into Z3 will probably fail (I didn't even try).

So, what I did instead was just try to visualize how data flowed through these instructions. I wrote [`analyze.py`](analyze.py) to create a data flow graph, where nodes are the instructions (and `mov`s are elided for simplicity). The first few `analyze.py` attempts produced really bad graphs because I was leaving constants as separate inputs, even though they were used by many, many instructions (see [`flow_bad.pdf`](flow_bad.pdf)). After moving constants into the node labels, I got a much nicer graph ([`flow.pdf`](flow.pdf)) which immediately revealed some high-level structure.

First, it's obvious from the flow graph (at a high level, zoomed all the way out) that there are eight repeats of the same basic structure, suggesting an 8-round cipher (albeit one with 1024-bit block sizes). Second, one particular pattern stands out frequently: the use of a `vpmullw/vpmulhuw/vpor - vpsubusw/vpsubw - vpcmpeqw - vpsrlw/vpand/vpaddw/vpsubw` network to turn two inputs into a single output. Because every instruction in this pattern operates either word-wise or bitwise, we can analyze the network's effect on a single pair of 16-bit inputs. As it turns out (through some lucky guessing and checking), this network computes `(x * y) % 65537`, but where 0 is swapped for 65536. It's a very clever function, and it's invertible if you know one of the inputs.

At this point, I started to code the cipher in the forward direction to check my understanding - see the first half of [`decrypt.py`](decrypt.py). By simply tracing the flow of data through one round and reimplementing the AVX instructions in Python, it was fairly easy to build the forward encryption algorithm (liberal amounts of debugging and tracing with `gdb` were used to check that each step was implemented correctly). After a couple hours, I got it working (producing identical output to the original program), so it was time to run the algorithm in reverse.

The round function breaks down as

    r0 = vmul65537(invecs[0], getvec(keys, keyoff + 0))
    r1 =    vpaddw(invecs[1], getvec(keys, keyoff + 0x20))
    r2 =    vpaddw(invecs[2], getvec(keys, keyoff + 0x40))
    r3 = vmul65537(invecs[3], getvec(keys, keyoff + 0x60))
    x0 = vpxor(r0, r2)
    x1 = vpxor(r1, r3)
    y0 = vmul65537(x0, getvec(keys, keyoff + 0x80))
    y1 = vmul65537(vshufnet(vpaddw(y0, x1)), getvec(keys, keyoff + 0xa0))
    y2 = vpaddw(y1, y0)

    o0 = vpxor(y1, r0)
    o1 = vpshufb(vpxor(y1, r2), getvec(constants, 0x200))
    o2 = vpshufb(vpxor(y2, r1), getvec(constants, 0x220))
    o3 = vpshufb(vpxor(y2, r3), getvec(constants, 0x240))

where `vshufnet` is a complicated function mapping a single input to a single output involving a bunch of weird shifts and such. The `vpshufb`s are all invertible thanks to the particular constants chosen.

By calculating `o0 ^ invshuf(o1)` we can recover `r0^r2 = x0`, which lets us get `y0`. Similarly, `invshuf(o2) ^ invshuf(o3)` gives `r1^r3 = x1`, which yields `y1` and then `y2` (just by running the forward calculations for `y0`, `y1`, and `y2`). With `y1` and `y2`, we can calculate `r0` through `r3` and thereby invert the round function.

Finally, we just invert all eight round functions to produce a [decryptor](decrypt.py) - note that at no point do we have to invert `vshufnet`. When we're done, we get a nice plaintext JPG, [`plaintext.jpg`](plaintext.jpg), with our flag:

    INS{XuejiaLai_StudentOfJim_YOUROCK}
