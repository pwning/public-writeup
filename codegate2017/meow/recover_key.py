from z3 import *
import hashlib

s = Solver()
k = [BitVec('k%d' % i, 8) for i in xrange(10)]
for i in xrange(10):
    # assume ASCII
    s.add(k[i] >= 0x20)
    s.add(k[i] <= 0x7f)

# prologue
s.add(k[2] ^ k[5] ^ 0x0d == 0x55) # push rbp
s.add(k[2] ^ k[3] ^ 0x48 == 0x48) # mov rbp, rsp
s.add(k[1] ^ k[8] ^ 0xf5 == 0x89)
s.add(k[3] ^ k[9] ^ 0xaf == 0xe5)
s.add(k[0] ^ k[3] ^ k[5] ^ k[9] ^ 0x4d == 0x48) # sub rsp, 0x??
s.add(k[1] ^ k[3] ^ k[5] ^ k[6] ^ 0xad == 0x83)
s.add(k[2] ^ k[5] ^ k[6] ^ k[7] ^ 0xbe == 0xec)
# s.add(k[0] ^ k[3] ^ k[7] ^ k[8] ^ 0x77 == 0x??)
s.add(k[3] ^ k[4] ^ 0x4c == 0x48) # some x64 operation

# epilogue
s.add(k[1] ^ k[3] ^ 0xa7 == 0xc3) # ret

while True:
    s.check()
    m = s.model()
    code = ''.join(chr(m[ki].as_long()) for ki in k)
    if hashlib.md5(code).hexdigest() == '9f46a92422658f61a80ddee78e7db914':
        print code
        break
    # reject this solution
    s.add( Not(And(*[ki == m[ki].as_long() for ki in k])) )

# $W337k!++y
