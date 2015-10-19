#!/usr/bin/env python3

data = bytearray(open('flag.puzzle', 'rb').read())
piecesz = (len(data) + 19) // 20
pieces = [data[i:i+piecesz] for i in range(0, len(data), piecesz)]
out = open('flag.png', 'wb')
def bxor(a, b):
    return bytearray(c^b for c in a)

# piece 0
p0 = b'\x89PNG'
c0 = bxor(pieces[0], pieces[0][0] ^ p0[0])
print(pieces[0][0] ^ p0[0])
# fix colors
c0 = c0.replace(b'\x8f\x77\xb5\x8f\x77\xb4\x6d\xc4\x59\xac', b'\x00\x00\x00\xff\xff\xff\xa5\xd9\x9f\xdd')
out.write(c0)

# piece 1
p1 = b'N' # from tRNS
c1 = bxor(pieces[1], pieces[1][0] ^ p1[0])
print(pieces[1][0] ^ p1[0])
out.write(c1)

idat = c1[-20:]

# piece 2
import zlib
for i in range(256):
    obj = zlib.decompressobj()
    piece = bxor(pieces[2], i)
    try:
        obj.decompress(idat)
        obj.decompress(piece)
    except Exception:
        continue
    print(i)
    break

out.write(piece)
idat += piece

# remaining pieces
w, h = 912, 912
datasize = ((w+7)//8 + 1) * h

idats = [idat]

# regex to check if each line is in the right format
import re
dataformat = re.compile(b'^(?:\x00\xff{8}(?:\x00\x00|\xff\xff){49}\xff{8})+.{0,115}$')

def try_piece(c):
    if c == 19:
        p19 = b'IEND'
        c19 = bxor(pieces[19], pieces[19][-8] ^ p19[0])
        print(pieces[19][-8] ^ p19[0])
        idats.append(c19)
        idat_chunk = b'IDAT' + b''.join(idats)[:-16]
        if zlib.crc32(idat_chunk) != 0xd9bf3b6a:
           return False
        out.write(b''.join(idats[1:]))
        return True
    possibles = []
    for i in reversed(range(256)):
        obj = zlib.decompressobj()
        piece = bxor(pieces[c], i)
        try:
            outdat = obj.decompress(b''.join(idats))
            outdat += obj.decompress(piece)
            if len(outdat) > datasize:
                continue
            if not re.match(dataformat, outdat):
                continue
        except Exception as e:
            continue
        possibles.append(i)

    print("possibles", c, possibles)
    for i in possibles:
        piece = bxor(pieces[c], i)
        idats.append(piece)
        if try_piece(c+1):
            return True
        idats.pop()

    return False

try_piece(3)

# sha1hash = 653056c378ff4bbff74737e36f53264c25f4d11b
# flag = hitcon{qrencode -s 16 -o flag.png -l H --foreground 8F77B5 --background 8F77B4}
