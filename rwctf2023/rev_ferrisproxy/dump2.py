from Crypto.Cipher import ARC4
from collections import defaultdict
import struct

ciphers = defaultdict(lambda: ARC4.new(b"explorer"))
streams = defaultdict(lambda: bytearray())

for row in open("dump1.txt"):
    stream, dstport, data = row.split()
#     print(stream, dstport, ciphers[stream, dstport].decrypt(bytes.fromhex(data)).hex(), sep="\t")
    streams[stream, dstport] += ciphers[stream, dstport].decrypt(bytes.fromhex(data))
    while len(streams[stream, dstport]) >= 4:
        plen, = struct.unpack(">I", streams[stream, dstport][:4])
        if len(streams[stream, dstport]) < 4 + plen:
            break
        pkt = streams[stream, dstport][4:4+plen]
        streams[stream, dstport] = streams[stream, dstport][4+plen:]
        if len(pkt) >= 8:
            cmd, mid = struct.unpack(">II", pkt[:8])
            print(stream, dstport, cmd, mid, pkt[8:].hex(), sep="\t")
        else:
            print(stream, dstport, -1, -1, pkt.hex(), sep="\t")

for stream, dstport in streams:
    if streams[stream, dstport]:
        print("???", stream, dstport, streams[stream, dstport].hex(), sep="\t")
