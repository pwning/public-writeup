## dec dec dec - Reversing Challenge - Writeup by Robert Xiao (@nneonneo)

### Description

A simple binary that encodes your input and compares it to a fixed string.

### Solution

The binary passes your input through three encoding stages:

- The first stage is base64, easily recognized by the embedded string table ("ABCDEF...XYZabcdef...XYZ0123456789+/").
- The next stage is rot13, which can be deduced from the fact that it checks for alphabetic characters and adds a constant mod 26 to them.
- The final stage is uuencoding, an older encoding technique. This is like base64, but uses a different alphabet (ASCII characters 32-96) and prepends a length byte to the input.

A simple Python program can decode all three:

    import binascii

    t = '@25-Q44E233=,>E-M34=,,$LS5VEQ45)M2S-),7-$/3T '
    t = binascii.a2b_uu(t).decode('rot13').decode('base64')
    print t

and we get the flag `TWCTF{base64_rot13_uu}`.
