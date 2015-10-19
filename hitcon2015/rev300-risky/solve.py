from z3 import *
import struct

s = Solver()

s0 = BitVec('s0', 32)
s1 = BitVec('s1', 32)
s2 = BitVec('s2', 32)
s3 = BitVec('s3', 32)
s5 = BitVec('s5', 32)

s.add(s1*s5 + s3*s2 + s0 == 0x181a9c5f)
s.add(s3*s1 + s2 + s0 == 0x2deacccb)
s.add(s2 + s3 + s1 + s5 + s0 == 0x8e2f6780)
s.add((s1 + s2 + s0)*(s3 + s5) == 0xb3da7b5f)
s.add(s1 + s2 + s0 == 0xe3b0cdef)
s.add(s3*s0 == 0x4978d844)
s.add(s2*s1 == 0x9bcd30de)
s.add(s2*s1*s1*s5*s0 == 0x41c7a3a0)
s.add(s1*s5 == 0x313ac784)

print s.check()
d = s.model()
for e in d:
    print e, d[e]
print ''

'''
s2 1295338573
s5 1362445638
s3 1497977931
s1 1379355478
s0 1145321036
'''

s = []
s += [struct.pack('<I',1497977931)]
s += [struct.pack('<I',1295338573)]
s += [struct.pack('<I',1379355478)]
s += [struct.pack('<I',1362445638)]
s += [struct.pack('<I',1145321036)]
print '-'.join(s)

s = struct.pack('<I',1497977931 ^ 0x2c280d2f)
s += struct.pack('<I',1295338573 ^ 0x38053525)
s += struct.pack('<I',1379355478 ^ 0x6b5c2a24)
s += struct.pack('<I',1362445638 ^ 0x27542728)
s += struct.pack('<I',1145321036 ^ 0x2975572f)

print 'hitcon{%s}' % s
