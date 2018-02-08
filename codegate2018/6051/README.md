## 6051 - Reversing Challenge

We are given a 64-bit ELF [binary](2d7acadf10224ffdabeab505970a8934.zip). It reads a line from stdin and
passes it into **sub\_1190**, which returns true if the input was correct.

**sub\_1190** is a fairly complex function, but since we know it needs to return true we start from the
bottom. It returns true if the result of **sub\_1080** matches **byte\_202020**. This function loops over
every byte of its input and outputs a byte or finds a run of characters and outputs a 3-byte sequence:
0x16, run length, character. This matches the behavior of a typical RLE encoder.

One weird thing about **sub\_1080** is that it also obfuscates the output by passing the run length
through a S-box and the characters summed with **rand() - 48**. Since **srand** is never called, we know
the result of calling **rand** and we can undo the obfuscation and the RLE encoding. A decoder written
in C is included at [undo\_rle.c](undo_rle.c).

```
111111100000011111100000000000001111111111011100000011110010100010110000100000010010101101111110111110001010011101001110000000001011000000000010000110011111000000000000000000000001000000110101000011110001111111111111110000111111111111110111111111111111111100100101111100010111001100101101111010111011111110010011111111111111111000000000000100100000000000000000111011011110011010111001011100100111010101111101000000000010000010001100011000110111011110000000
```

The output of decoding the RLE data is a stream of ASCII digits of 0 and 1, which is clearly a binary sequence.
This leads us to suspect that the beginning of **sub\_1190** will convert our input into a binary stream. The
next question is what operation does **sub\_850** and the loop immediately before it perform.

A breakpoint on **sub\_850** and looking at *rdi* we notice that it is an array of strings, where each is
our input rotated by one, two, etc. At this point, we assume that this challenge is a BWT + RLE compressor.
We steal the inverse BWT code from Wikipedia, we find this flag as one of the possible inputs
([ibwt.py](ibwt.py)):

```
FLAG{w0w_w0w_w0w_s1mp13_str1n9_c0mpr3ss10n_1011110100011}
```
