from pwn import *

import struct

def parse_boxes():
    with open('./eop', 'rb') as f:
        f.seek(0x12020)
        s = f.read(0x1130)
    whiten_init = struct.unpack('<IIII', s[0:0x10])
    whiten_fin = struct.unpack('<IIII', s[0x10:0x20])
    aux = struct.unpack('<' + 'I' * 32, s[0x20:0xa0])
    sbox0 = struct.unpack('<' + 'I' * 256, s[0x100:0x500])
    sbox1 = struct.unpack('<' + 'I' * 256, s[0x500:0x900])
    sbox2 = struct.unpack('<' + 'I' * 256, s[0x900:0xD00])
    sbox3 = struct.unpack('<' + 'I' * 256, s[0xD00:0x1100])
    to_match = s[0x1100:0x1130]

    return (whiten_init, whiten_fin, aux, sbox0, sbox1, sbox2, sbox3, to_match)

def forward(inp, all_boxes):
    whiten_init, whiten_fin, aux, sbox0, sbox1, sbox2, sbox3, _ = all_boxes

    out8_cur = '\x00' * 8
    out8_next = '\x00' * 8

    out = ''

    s = [0 for _ in xrange(6)]
    
    def S0123(o, i):
        e = p32(s[i])
        s[o] = sbox0[ord(e[0])] ^ sbox1[ord(e[1])] ^ sbox2[ord(e[2])] ^ sbox3[ord(e[3])]

    def S1230(o, i):
        e = p32(s[i])
        s[o] = sbox1[ord(e[0])] ^ sbox2[ord(e[1])] ^ sbox3[ord(e[2])] ^ sbox0[ord(e[3])]

    def A(o, i):
        s[o] ^= (aux[i] + s[4] + s[5]) & 0xffffffff

    def A2(o, i):
        s[o] ^= (aux[i] + s[4] + 2 * s[5]) & 0xffffffff

    def R(o):
        s[o] = ror(s[o], 1, word_size=32)

    def L(o):
        s[o] = rol(s[o], 1, word_size=32)

    def dump():
        print 'S:', map(hex, s)
        print 'out8_cur:', out8_cur.encode('hex')
        print 'out8_next:', out8_next.encode('hex')

    assert len(inp) == 0x30

    for blk in xrange(3):
        cur8s = ''
        for (i, o) in zip(inp[blk * 16:blk * 16 + 8], out8_cur):
            cur8s += chr(ord(i) ^ ord(o))
        next8s = ''
        for (i, o) in zip(inp[blk * 16 + 8:blk * 16 + 16], out8_next):
            next8s += chr(ord(i) ^ ord(o))

        s[0], s[1] = struct.unpack('<II', cur8s)
        s[2], s[3] = struct.unpack('<II', next8s)
        s[0] ^= whiten_init[0]
        s[1] ^= whiten_init[1]
        s[2] ^= whiten_init[2]
        s[3] ^= whiten_init[3]
        dump()

        aux_ctr = 0;

        for _ in xrange(8):
            S0123(4, 0)
            dump()
            S1230(5, 1)
            dump()
            A(2, aux_ctr)
            aux_ctr += 1
            dump()
            R(2)
            dump()
            L(3)
            dump()
            A2(3, aux_ctr)
            aux_ctr += 1
            dump()

            S0123(4, 2)
            dump()
            S1230(5, 3)
            dump()
            A(0, aux_ctr)
            aux_ctr += 1
            dump()
            R(0)
            dump()
            L(1)
            dump()
            A2(1, aux_ctr)
            aux_ctr += 1
            dump()

        s[0] ^= whiten_fin[2]
        s[1] ^= whiten_fin[3]
        s[2] ^= whiten_fin[0]
        s[3] ^= whiten_fin[1]
        dump()

        out8_cur = p32(s[2]) + p32(s[3])
        out8_next = p32(s[0]) + p32(s[1])
        dump()

        out += out8_cur + out8_next

    return out

def invert(all_boxes):
    whiten_init, whiten_fin, aux, sbox0, sbox1, sbox2, sbox3, to_match = all_boxes

    cur8 = '\x00' * 8
    next8 = '\x00' * 8

    out = to_match
    inp = ''

    s = [0 for _ in xrange(6)]
    
    def S0123(o, i):
        e = p32(s[i])
        s[o] = sbox0[ord(e[0])] ^ sbox1[ord(e[1])] ^ sbox2[ord(e[2])] ^ sbox3[ord(e[3])]

    def S1230(o, i):
        e = p32(s[i])
        s[o] = sbox1[ord(e[0])] ^ sbox2[ord(e[1])] ^ sbox3[ord(e[2])] ^ sbox0[ord(e[3])]

    def A(o, i):
        s[o] ^= (aux[i] + s[4] + s[5]) & 0xffffffff

    def A2(o, i):
        s[o] ^= (aux[i] + s[4] + 2 * s[5]) & 0xffffffff

    def R(o):
        s[o] = ror(s[o], 1, word_size=32)

    def L(o):
        s[o] = rol(s[o], 1, word_size=32)

    def dump():
        print 'S:', map(hex, s)
        print 'out8_cur:', out8_cur.encode('hex')
        print 'out8_next:', out8_next.encode('hex')

    for blk in xrange(2, -1, -1):
        s[2], s[3] = struct.unpack('<II', out[blk * 16:blk * 16 + 8])
        s[0], s[1] = struct.unpack('<II', out[blk * 16 + 8:blk * 16 + 16])

        s[0] ^= whiten_fin[2]
        s[1] ^= whiten_fin[3]
        s[2] ^= whiten_fin[0]
        s[3] ^= whiten_fin[1]

        aux_ctr = 31

        for _ in xrange(7, -1, -1):
            S0123(4, 2)
            S1230(5, 3)
            A2(1, aux_ctr)
            aux_ctr -= 1
            R(1)
            L(0)
            A(0, aux_ctr)
            aux_ctr -= 1

            S0123(4, 0)
            S1230(5, 1)
            A2(3, aux_ctr)
            aux_ctr -= 1
            R(3)
            L(2)
            A(2, aux_ctr)
            aux_ctr -= 1

        if blk > 0:
            old_out8_cur0, old_out8_cur1, old_out8_next0, old_out8_next1 = struct.unpack('<IIII', out[(blk - 1) * 16:(blk - 1) * 16 + 16])
        else:
            old_out8_cur0, old_out8_cur1, old_out8_next0, old_out8_next1 = 0, 0, 0, 0
        
        s[0] = s[0] ^ whiten_init[0] ^ old_out8_cur0
        s[1] = s[1] ^ whiten_init[1] ^ old_out8_cur1
        s[2] = s[2] ^ whiten_init[2] ^ old_out8_next0
        s[3] = s[3] ^ whiten_init[3] ^ old_out8_next1

        inp = p32(s[0]) + p32(s[1]) + p32(s[2]) + p32(s[3]) + inp

    return inp

if __name__ == '__main__':
    all_boxes = parse_boxes()
    #res = forward('12345678' * 6, all_boxes)
    #print res.encode('hex')
    print invert(all_boxes)
