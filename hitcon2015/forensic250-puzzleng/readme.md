## puzzleng - Forensic 250 Problem - Writeup by Robert Xiao (@nneonneo)

### Description

> Next Generation of Puzzle!
> 
> puzzleng-edb16f6134bafb9e8b856b441480c117.tgz

### Solution

We're given a small file encrypted with the provided binary. Reversing the binary shows that the encryption algorithm is basically

    pw = sha1(password)
    data = bytearray(open(infile))
    piecelen = (len(data)+19) // 20

    for i in range(20):
        idx = i*piecelen
        data[idx:idx+piecelen] = [c^pw[i] for c in data[idx:idx+piecelen]]

in other words, it is encrypting each successive 1/20th of the file with a different xor key. For the provided encrypted file, the piece size is 57 bytes.

We bruteforce the 256 possible xor keys for the first piece and discover that it's a PNG. PNG files have a very simple structure: they consist of a sequence of *chunks*, which each consist of a 4-byte length, 4-byte "tag", chunk content, and a 4-byte CRC-32 checksum. The main data chunk, tagged "IDAT", consists of `zlib` compressed data containing the image data.

### Piece 0

The first 57-byte piece yields a PLTE (color palette) PNG chunk which specifies two colors: 8F77B5 and 8F77B4. Since these are basically indistinguishable colors, I put in a little hack that changes the palette colors to 000000 and FFFFFF (black and white).

### Piece 1
The first piece ends with the partial chunk tag `tR`. From the PNG spec, we guess that this is the `tRNS` (transparency) tag, yielding a second valid piece with an `IDAT` chunk and 20 bytes of `zlib` compressed data.

We can use Python's `zlib.decompressobj` object to attempt to decode partial `zlib` streams, but on this first 20 bytes of compressed data we get nothing.

### Piece 2
For the next piece, we try all 256 xor keys and only accept keys where the resulting data decompresses successfully. Luckily, only one key produces valid zlib data. The decompression of this piece yields some meaningful image data, but there's just a lot of white so far and only one partial line with black pixels.

### Piece 3
We try the same thing again with the next piece, trying all keys and taking those which decompress successfully. Unfortunately, almost all of these decompress successfully. I therefore just dumped the partially decompressed data for each key and inspected them manually. The image is 912x912, encoded as bits, so each row is 114 bytes long. PNG prepends a single header byte to each row (which in our image appears to always be 0x00), so in total each row is 115 bytes long and we can thus dump our decompressed data as an image.

Most of the outputs look like garbage, but at key=194, we see a very regular pattern ('X' = 0xff, ' ' = 0x00):

            XXXXXXXXXXXXXX  XXXXXX  XXXX        XXXX  XXXX  XX  XXXXXXXXXX  XX  XXXX        XX  XXXXXXXXXXXXXX        
            XXXXXXXXXXXXXX  XXXXXX  XXXX        XXXX  XXXX  XX  XXXXXXXXXX  XX  XXXX        XX  XXXXXXXXXXXXXX        
            XXXXXXXXXXXXXX  XXXXXX  XXXX        XXXX  XXXX  XX  XXXXXXXXXX  XX  XXXX        XX  XXXXXXXXXXXXXX        
            XXXXXXXXXXXXXX  XXXXXX  XXXX        XXXX  XXXX  XX  XXXXXXXXXX  XX  XXXX        XX  XXXXXXXXXXXXXX        
            XXXXXXXXXXXXXX  XXXXXX  XXXX        XXXX  XXXX  XX  XXXXXXXXXX  XX  XXXX        XX  XXXXXXXXXXXXXX        
            XXXXXXXXXXXXXX  XXXXXX  XXXX        XXXX  XXXX  XX  XXXXXXXXXX  XX  XXXX        XX  XXXXXXXXXXXXXX        
            XXXXXXXXXXXXXX  XXXXXX  XXXX        XXXX  XXXX  XX  XXXXXXXXXX  XX  XXXX        XX  XXXXXXXXXXXXXX        
            XXXXXXXXXXXXXX  XXXXXX  XXXX        XXXX  XXXX  XX  XXXXXXXXXX  XX  XXXX        XX  XXXXXXXXXXXXXX        
            XXXXXXXXXXXXXX  XXXXXX  XXXX        XXXX  XXXX  XX  XXXXXXXXXX  XX  XXXX        XX  XXXXXXXXXXXXXX        
            XXXXXXXXXXXXXX  XXXXXX  XXXX        XXXX  XXXX  XX  XXXXXXXXXX  XX  XXXX        XX  XXXXXXXXXXXXXX        
            XXXXXXXXXXXXXX  XXXXXX  XXXX        XXXX  XXXX  XX  XXXXXXXXXX  XX  XXXX        XX  XXXXXXXXXXXXXX        
            XXXXXXXXXXXXXX  XXXXXX  XXXX        XXXX  XXXX  XX  XXXXXXXXXX  XX  XXXX        XX  XXXXXXXXXXXXXX        
            XXXXXXXXXXXXXX  XXXXXX  XXXX        XXXX  XXXX  XX  XXXXXXXXXX  XX  XXXX        XX  XXXXXXXXXXXXXX        
            XXXXXXXXXXXXXX  XXXXXX  XXXX        XXXX  XXXX  XX  XXXXXXXXXX  XX  XXXX        XX  XXXXXXXXXXXXXX        
            XXXXXXXXXXXXXX  XXXXXX  XXXX        XXXX  XXXX  XX  XXXXXXXXXX  XX  XXXX        XX  XXXXXXXXXXXXXX        
            XXXXXXXXXXXXXX  XXXXXX  XXXX        XXXX  XXXX  XX  XXXXXXXXXX  XX  XXXX        XX  XXXXXXXXXXXXXX        
            XX          XX        XX  XXXXXX  XXXX      XX  XX      XXXXXXXX  XXXX  XXXXXXXXXX  XX          XX        
            XX          XX        XX  XXXXXX  XXXX      XX  XX      XXXXXXXX  XXXX  XXXXXXXXXX  XX          XX        
            XX          XX        XX  XXXXXX  XXXX      XX  XX      XXXXXXXX  XXXX  XXXXXXXXXX  XX          XX        
            XX          XX        XX  XXXXXX  XXXX      XX  XX      XXXXXXXX  XXXX  XXXXXXXXXX  XX          XX        
            XX          XX        XX  XXXXXX  XXXX      XX  XX      XXXXXXXX  XXXX  XXXXXXXXXX  XX          XX        
            XX          XX        XX  XXXXXX  XXXX      XX  XX      XXXXXXXX  XXXX  XXXXXXXXXX  XX          XX        
            XX          XX        XX  XXXXXX  XXXX      XX  XX      XXXXXXXX  XXXX  XXXXXXXXXX  XX          XX        
            XX          XX        XX  XXXXXX  XXXX      XX  XX      XXXXXXXX  XXXX  XXXXXXXXXX  XX          XX        
            XX          XX        XX  XXXXXX  XXXX      XX  XX      XXXXXXXX  XXXX  XXXXXXXXXX  XX          XX        
            XX          XX        XX  XXXXXX  XXXX      XX  XX      XXXXXXXX  XXXX  XXXXXXXXXX  XX          XX        
            XX          XX        XX  XXXXXX  XXXX      XX  XX      XXXXXXXX  XXXX  XXXXXXXXXX  XX          XX        
            XX          XX        XX  XXXXXX  XXXX      XX  XX      XXXXXXXX  XXXX  XXXXXXXXXX  XX          XX        
            XX          XX        XX  XXXXXX  XXXX      XX  XX      XXXXXXXX  XXXX  XXXXXXXXXX  XX          XX        
            XX          XX        XX  XXXXXX  XXXX      XX  XX      XXXXXXXX  XXXX  XXXXXXXXXX  XX          XX        
            XX          XX        XX  XXXXXX  XXXX      XX  XX      XXXXXXXX  XXXX  XXXXXXXXXX  XX          XX        
            XX          XX        XX  XXXXXX  XXXX      XX  XX      XXXXXXXX  XXXX  XXXXXXXXXX  XX          XX        
            XX  XXXXXX  XX    XX    XXXX            XXXXXXXX  XX  XX  XX  XX              XXXX  XX  XXXXXX  XX        
            XX  XXXXXX  XX    XX    XXXX            XXXXXXXX  XX  XX  XX  XX              XXXX  XX  XXXXXX  XX        
            XX  XXXXXX  XX    XX    XXXX            XXXXXXXX  XX  XX  XX  XX              XXXX  XX  XXXXXX  XX        
            XX  XXXXXX  XX    XX    XXXX            XXXXXXXX  XX  XX  XX  XX              XXXX  XX  XXXXXX  XX        
            XX  XXXXXX  XX    XX    XXXX            XXXXXXXX  XX  XX  XX  XX              XXXX  XX  XXXXXX  XX        
            XX  XXXXXX  XX    XX    XXXX            XXXXXXXX  XX  XX  XX  XX              XXXX  XX  XXXXXX  XX        
            XX  XXXXXX  XX    XX    XXXX            XXXXXXXX  XX  XX  XX  XX              XXXX  XX  XXXXXX  XX        
            XX  XXXXXX  XX    XX    XXXX            XXXXXXXX  XX  XX  XX  XX              XXXX  XX  XXXXXX  XX        
            XX  XXXXXX  XX    XX    XXXX            XXXXXXXX  XX  XX  XX  XX              XXXX  XX  XXXXXX  XX        
            XX  XXXXXX  XX    XX    XXXX            XXXXXXXX  XX  XX  XX  XX              XXXX  XX  XXXXXX  XX        
            XX  XXXXXX  XX    XX    XXXX            XXXXXXXX  XX  XX  XX  XX              XXXX  XX  XXXXXX  XX        
            XX  XXXXXX  XX    XX    XXXX            XXXXXXXX  XX  XX  XX  XX              XXXX  XX  XXXXXX  XX        
            XX  XXXXXX  XX    XX    XXXX            XXXXXXXX  XX  XX  XX  XX              XXXX  XX  XXXXXX  XX        
            XX  XXXXXX  XX    XX    XXXX            XXXXXXXX  XX  XX  XX  XX              XXXX  XX  XXXXXX  XX        
            XX  XXXXXX  XX    XX    XXXX            XXXXXXXX  XX  XX  XX  XX              XXXX  XX  XXXXXX  XX        
            XX  XXXXXX  XX    XX    XXXX            XXXXXXXX  XX  XX  XX  XX              XXXX  XX  XXXXXX  XX        
            XX  XXXXXX  XX  XX    XXXXXX    XX    XX  XX    XX    XX          XX      XX  XX
  
It looks very regular! Let's go with the assumption that every row is formatted like this, and in future chunks only select chunks which produce data in this format (starts with 8 `\x00`, then 49 `\x00\x00` or `\xff\xff` pairs, then a final 8 `\x00`). This is quite easy to do with a regex over the decompressed data.

# Piece 4+

It turns out our assumption is good, and subsequently we are able to guess each key byte completely uniquely (i.e. exactly one value for the key yields decompressed data that matches our pattern, for each piece). The decryption program is provided in `decrypt.py`.

In the end, it turns out that the output is a QR code (`flag.png`), and the final flag is

    hitcon{qrencode -s 16 -o flag.png -l H --foreground 8F77B5 --background 8F77B4}
