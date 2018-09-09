import ctypes
encrypt = ctypes.CDLL('encrypt.so')
tables = []
for i in range(4):
    table = {encrypt.encrypt_t1_1(i, c)&0xff: c for c in range(256)}
    if len(table) != 256:
        raise Exception("you screwed up round %d" % i)
    tables.append(table)

t4 = [
    [0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1,],
    [0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0,],
    [1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1,],
    [0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1,],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1,],
    [1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0,],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0,],
    [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0,],
    [1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1,],
    [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0,],
    [0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1,],
    [0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0,],
    [0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0,],
    [1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0,],
    [1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0,],
    [0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1,],
    [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0,],
    [0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0,],
    [0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0,],
]

def decrypt_t4(round, buf, key):
    for i in range(16):
        buf[i] ^= key[i] ^ t4[round][i]

def decrypt_t3(buf):
    for i in range(0, 16, 4):
        c = buf[i] ^ buf[i+1] ^ buf[i+2] ^ buf[i+3]
        buf[i] ^= c
        buf[i+1] ^= c
        buf[i+2] ^= c
        buf[i+3] ^= c

t2 = [0, 10, 5, 15, 14, 4, 11, 1, 9, 3, 12, 6, 7, 13, 2, 8]
t2i = {j:i for i,j in enumerate(t2)}
def decrypt_t2(buf):
    buf[:] = [buf[t2i[i]] for i in range(16)]

def decrypt_t1(round, buf):
    for i in range(16):
        buf[i] = tables[round%4][buf[i]]

def xorkey(buf, key):
    for i in range(16):
        buf[i] ^= key[i]

def decrypt(buf, key):
    xorkey(buf, key)
    decrypt_t1(19, buf)
    for i in range(18, -1, -1):
        decrypt_t4(i, buf, key)
        decrypt_t3(buf)
        decrypt_t2(buf)
        decrypt_t1(i, buf)
    xorkey(buf, key)

if __name__ == '__main__':
    key = bytearray([0] * 16)
    buf = bytearray([0x9c,0x89,0x07,0x04,0xb0,0x9a,0x5d,0x18,0x56,0x6b,0xfe,0x64,0xe0,0x31,0x30,0xc7])
    decrypt(buf, key)
    assert buf == bytearray([0] * 16)

    key = bytearray(range(16))
    buf = bytearray([0x81,0x22,0x56,0xb3,0x85,0xb8,0x3f,0x30,0xe7,0x80,0x1d,0xff,0x32,0xca,0x3c,0x5a])
    decrypt(buf, key)
    assert buf == bytearray(range(16, 32))
