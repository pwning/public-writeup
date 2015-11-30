## imaged - Steganography 90 Problem

### Description

`imaged` is a cute PNG in which the CRC checksums for the image blocks spell
out the key

### Solution

So opening this image things look pretty normal. It is a stego problem, but the
LSBs don't reveal anything useful. Next on the stego checklist is the palette,
which looks fairly normal, but seems very... random. Then we notice that the
CRC checksum is all ASCII!

The flag turned out to be short enough to read off by hand, but anticipating
something long, we wrote a short script to do it nicely, using a 010 PNG
template. (This uses the pfp library for parsing 010 templates in Python)

```
import pfp, struct
print ''.join([struct.pack(">I",c.crc._pfp__value) for c in pfp.parse(data_file="imaged.png", template=open("/home/tyler/Documents/SweetScape/010 Templates/PNGTemplate.bt").read())._pfp__children[1]])
```

This prints out the key (as well as all the other CRC checksums, which
turn out to not spell anything nice): `9447{Steg0_redunDaNcy_CHeck}`
