from z3 import *

smt = Solver()
input = [BitVec("input%s" % i, 8) for i in range(39)]
possible_char = list('0123456789abcdef')
freq_char = [3, 2, 2, 0, 3, 2, 1, 3, 3, 1, 1, 3, 1, 2, 2, 3]
condition_v1 = (0x15E, 0xDA, 0x12F, 0x131, 0x100, 0x131, 0xFB, 0x102)
condition_v2 = (0x52, 0x0c, 0x01, 0x0f, 0x5c, 0x05, 0x53, 0x58)
condition_v3 = (0x129, 0x103, 0x12b, 0x131, 0x135, 0x10b, 0xff, 0xff)
condition_v4 = (0x1, 0x57, 0x7, 0x0d, 0x0d, 0x53, 0x51, 0x51)
condition_v5 = (128, 128, 255, 128, 255, 255, 255, 255, 128, 255, 255, 128, 128, 255, 255, 128, 255, 255, 128, 255, 128, 128, 255, 255, 255, 255, 128, 255, 255, 255, 128, 255L)
input_prefix = 'TWCTF{'

for i in range(len(input_prefix)):
    smt.add(input[i] == ord(input_prefix[i]))
smt.add(input[38] == ord('}'))
smt.add(input[7] == 102)
smt.add(input[11] == 56)
smt.add(input[12] == 55)
smt.add(input[23] == 50)
smt.add(input[37] == 53)
smt.add(input[31] == 52)

for i, j in zip(freq_char, possible_char):
    smt.add(i == Sum([If(input[i] == ord(j), 1, 0) for i in range(0,39)]))

for k in range(0, 8):
    smt.add(input[4*k+6] + input[4*k+7] + input[4*k+8] + input[4*k+9] == condition_v1[k])
    smt.add(input[4*k+6] ^ input[4*k+7] ^ input[4*k+8] ^ input[4*k+9] == condition_v2[k])
    smt.add(input[6+k] + input[8+6+k] + input[16+6+k] + input[24+6+k] == condition_v3[k])
    smt.add(input[6+k] ^ input[8+6+k] ^ input[16+6+k] ^ input[24+6+k] == condition_v4[k])

for i in range(len(condition_v5)):
    if condition_v5[i] == 0x80:
        smt.add(And(96 < input[6 + i], input[6 + i] <= 102))
    elif condition_v5[i] == 0xff:
        smt.add(And(47 < input[6 + i], input[6 + i] <= 57))

sumTerms = [input[2*(i+3)] for i in range(0, 16)]
smt.add(Sum(sumTerms) == 1160)

if smt.check() == sat:
    print 'sat!'
    m = smt.model()
    print ''.join(chr(m[input[i]].as_long()) for i in range(39))
else:
    print 'unsat!'

# TWCTF{df2b4877e71bd91c02f8ef6004b584a5}
