import reedsolo
reedsolo.init_tables(0x11d)

colors = 'ROYGCBVW'
def decode_im(im):
    print im
    out = bytearray([0] * 24)
    for i in range(0, 24, 3):
        res = 0
        for j in range(8):
            res |= (im[i/3*8+j] << ((7-j)*3))
        out[i] = res >> 16
        out[i+1] = (res >> 8) & 0xff
        out[i+2] = res & 0xff

    input = out[:]
    mes, ecc = reedsolo.rs_correct_msg(input, 8)
    err = 0
    for x, y in zip((mes+ecc), input):
        err += sum(map(int, '{:08b}'.format(x ^ y)))
    print "%d errors" % err
    return mes

import ast
data = ast.literal_eval(open('data.txt').read())

key = [3, 5, 5, 3, 1, 2, 3, 2, 7, 3, 3, 6, 7, 0, 0, 0, 0, 2, 1, 5, 6, 7, 3, 1, 5, 5, 0, 0, 0, 3, 2, 0, 4, 4, 2, 5, 3, 5, 7, 5, 2, 6, 0, 1, 3, 7, 6, 2, 2, 6, 4, 6, 6, 2, 4, 7, 7, 1, 4, 2, 5, 5, 5, 7]
key = decode_im(key)
print 'key =', repr(key)

from mycrypt import decrypt

outf = open('test.jpg', 'wb')
for i, frame in enumerate(data[1:]):
    print i
    try:
        buf = decode_im(frame)
    except Exception as e:
        print "FAILED:", e
        continue

    print 'enc =', repr(buf)
    decrypt(buf, key)
    print 'dec =', repr(buf)
    outf.write(buf)
