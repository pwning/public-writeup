"""Script that implements the VM from arc4_stranger. It infinite loops printing
the flag over and over, and the flag text is oddly doubled... but whatever,
it was good enough for a CTF :P"""

# This is the UTF-8 "HEXAGRAM" data that serves as bytecode.
# Instead of unicode characters U+4DC0 - U+DFF, they're here as integers 0-63
x = [0, 48, 0, 33, 5, 0, 16, 0, 8, 33, 16, 34, 8, 32, 0, 12, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 16, 1, 0, 0, 20, 20, 22, 0, 0, 3, 5, 0, 12, 4, 0, 1, 1, 1, 0, 0, 12, 20, 0, 48, 16, 0, 4, 0, 20, 4, 1, 0, 13, 45, 0, 0, 12, 20, 0, 48, 16, 0, 4, 0, 4, 0, 0, 49, 16, 3, 1, 0, 0, 16, 1, 16, 16, 4, 0, 55, 16, 0, 0, 49, 16, 3, 1, 0, 0, 16, 1, 16, 16, 4, 0, 55, 16, 0, 0, 49, 16, 3, 1, 0, 0, 16, 25, 48, 0, 3, 5, 0, 12, 4, 0, 1, 1, 55, 0, 0, 12, 20, 0, 48, 16, 0, 4, 0, 4, 0, 0, 49, 16, 3, 1, 0, 0, 16, 1, 16, 16, 4, 0, 54, 28, 0, 0, 49, 16, 3, 1, 0, 0, 16, 19, 48, 0, 3, 5, 0, 12, 4, 0, 1, 1, 39, 0, 0, 12, 20, 0, 48, 16, 0, 4, 4, 48, 0, 0, 49, 16, 3, 1, 0, 0, 16, 1, 16, 16, 4, 0, 52, 48, 0, 0, 49, 16, 3, 1, 0, 0, 16, 21, 32, 0, 3, 5, 0, 12, 4, 0, 1, 1, 39, 0, 0, 12, 20, 0, 48, 16, 0, 4, 0, 4, 0, 0, 49, 16, 3, 1, 0, 0, 16, 1, 16, 16, 4, 0, 53, 32, 0, 0, 49, 16, 3, 1, 0, 0, 16, 27, 32, 0, 3, 5, 0, 12, 4, 0, 1, 1, 9, 0, 0, 12, 20, 0, 48, 16, 0, 4, 6, 20, 0, 0, 49, 16, 3, 1, 0, 0, 16, 1, 16, 16, 4, 0, 54, 28, 0, 0, 49, 16, 3, 1, 0, 0, 16, 21, 48, 0, 3, 5, 0, 12, 4, 0, 1, 0, 1, 0, 0, 12, 20, 0, 48, 16, 0, 4, 0, 20, 4, 1, 0, 13, 33, 0, 0, 12, 20, 0, 48, 16, 0, 4, 5, 28, 0, 0, 49, 16, 3, 1, 0, 0, 16, 22, 16, 0, 3, 5, 0, 12, 4, 0, 1, 1, 33, 0, 0, 12, 20, 0, 48, 16, 0, 4, 0, 20, 4, 1, 0, 12, 1, 0, 0, 12, 20, 0, 48, 16, 0, 4, 0, 20, 4, 1, 0, 13, 37, 0, 0, 12, 20, 0, 48, 16, 0, 4, 7, 12, 0, 0, 49, 16, 3, 1, 0, 0, 16, 30, 0, 0, 3, 5, 0, 12, 4, 0, 1, 1, 51, 0, 0, 12, 20, 0, 48, 16, 0, 4, 0, 20, 4, 1, 0, 13, 33, 0, 0, 12, 20, 0, 48, 16, 0, 4, 0, 4, 0, 0, 49, 16, 3, 1, 0, 0, 16, 1, 16, 16, 4, 0, 55, 16, 0, 0, 49, 16, 3, 1, 0, 0, 16, 25, 32, 0, 3, 5, 0, 12, 4, 0, 1, 1, 52, 0, 0, 12, 20, 0, 48, 16, 0, 4, 0, 20, 4, 1, 0, 13, 54, 0, 0, 12, 20, 0, 48, 16, 0, 4, 0, 4, 0, 0, 49, 16, 3, 1, 0, 0, 16, 1, 16, 16, 4, 0, 55, 8, 0, 0, 49, 16, 3, 1, 0, 0, 16, 22, 16, 0, 3, 5, 0, 12, 4, 0, 1, 1, 50, 0, 0, 12, 20, 0, 48, 16, 0, 4, 5, 36, 0, 0, 49, 16, 3, 1, 0, 0, 16, 1, 16, 16, 4, 0, 48, 4, 0, 0, 49, 16, 3, 1, 0, 0, 16, 1, 16, 16, 4, 0, 53, 4, 0, 0, 49, 16, 3, 1, 0, 0, 16, 27, 48, 0, 3, 5, 0, 12, 4, 0, 1, 0, 5, 1, 0, 16, 3, 21, 48, 0, 3, 5, 0, 12, 4, 0, 1, 1, 23, 0, 0, 12, 20, 0, 48, 16, 0, 4, 5, 28, 0, 0, 49, 16, 3, 1, 0, 0, 16, 19, 16, 0, 3, 5, 0, 12, 4, 0, 1, 0, 1, 0, 0, 12, 20, 0, 48, 16, 0, 4, 0, 20, 4, 1, 0, 13, 22, 0, 0, 12, 20, 0, 48, 16, 0, 4, 7, 8, 0, 0, 49, 16, 3, 1, 0, 0, 16, 26, 32, 0, 3, 5, 0, 12, 4, 0, 1, 1, 1, 0, 0, 12, 20, 0, 48, 16, 0, 4, 7, 20, 0, 0, 49, 16, 3, 1, 0, 0, 16, 1, 16, 16, 4, 0, 54, 28, 0, 0, 49, 16, 3, 1, 0, 0, 16, 26, 0, 0, 3, 5, 0, 12, 4, 0, 1, 1, 56, 0, 0, 12, 20, 0, 48, 16, 0, 4, 0, 4, 0, 0, 49, 16, 3, 1, 0, 0, 16, 1, 16, 16, 4, 0, 52, 32, 0, 0, 49, 16, 3, 1, 0, 0, 16, 1, 16, 16, 4, 0, 54, 40, 0, 0, 49, 16, 3, 1, 0, 0, 16, 0, 16, 0, 3, 5, 0, 12, 4, 0, 1, 0, 5, 1, 0, 16, 3, 30, 16, 0, 3, 5, 0, 12, 4, 0, 1, 1, 49, 0, 0, 12, 20, 0, 48, 16, 0, 4, 4, 12, 0, 0, 49, 16, 3, 1, 0, 0, 16, 24, 16, 0, 3, 5, 0, 12, 4, 0, 1, 0, 5, 1, 0, 16, 3, 0, 16, 0, 3, 5, 0, 12, 4, 0, 1, 0, 5, 1, 0, 16, 3, 27, 32, 0, 3, 5, 0, 12, 4, 0, 1, 1, 48, 0, 0, 12, 20, 0, 48, 16, 0, 4, 6, 24, 0, 0, 49, 16, 3, 1, 0, 0, 16, 25, 0, 0, 3, 5, 0, 12, 4, 0, 1, 0, 5, 1, 0, 16, 3, 0, 16, 0, 3, 5, 0, 12, 4, 0, 1, 0, 5, 1, 0, 16, 3, 22, 0, 0, 3, 5, 0, 12, 4, 0, 1, 1, 41, 0, 0, 12, 20, 0, 48, 16, 0, 4, 4, 12, 0, 0, 49, 16, 3, 1, 0, 0, 16, 1, 16, 16, 4, 0, 53, 16, 0, 0, 49, 16, 3, 1, 0, 0, 16, 22, 0, 0, 3, 5, 0, 12, 4, 0, 1, 0, 1, 0, 0, 12, 20, 0, 48, 16, 0, 4, 0, 20, 4, 1, 0, 13, 47, 0, 0, 12, 20, 0, 48, 16, 0, 4, 0, 20, 4, 1, 0, 13, 57, 0, 0, 12, 20, 0, 48, 16, 0, 4, 0, 4, 0, 0, 49, 16, 3, 1, 0, 0, 16, 1, 16, 16, 4, 0, 54, 16, 0, 0, 49, 16, 3, 1, 0, 0, 16, 1, 16, 16, 4, 0, 55, 36, 0, 0, 49, 16, 3, 1, 0, 0, 16, 28, 0, 0, 3, 5, 0, 12, 4, 0, 1, 0, 1, 0, 0, 12, 20, 0, 48, 16, 0, 4, 0, 20, 4, 1, 0, 13, 51, 0, 0, 12, 20, 0, 48, 16, 0, 4, 6, 28, 0, 0, 49, 16, 3, 1, 0, 0, 16, 26, 0, 0, 3, 5, 0, 12, 4, 0, 1, 1, 37, 0, 0, 12, 20, 0, 48, 16, 0, 4, 0, 20, 4, 1, 0, 12, 1, 0, 0, 12, 20, 0, 48, 16, 0, 4, 0, 20, 4, 1, 0, 13, 44, 0, 0, 12, 20, 0, 48, 16, 0, 4, 5, 0, 0, 0, 49, 16, 3, 1, 0, 0, 16, 21, 0, 0, 3, 5, 0, 12, 4, 0, 1, 0, 46, 0, 0, 12, 20, 0, 48, 16, 0, 4, 0, 20, 4, 1, 0, 12, 3, 0, 0, 12, 20, 0, 48, 16, 0, 4, 0, 20, 4, 1, 0, 12, 0, 0, 0, 16, 20, 62, 32, 0, 20, 5, 14, 60, 0, 2, 49, 16, 0, 1, 0, 24, 15, 1, 32, 24, 10, 2, 47, 40, 0, 3, 1, 16, 12, 2, 32, 0, 12, 1, 16, 16, 4, 0, 48, 0, 4, 1, 48, 60, 5, 1, 0, 16, 3, 61, 48, 0, 21, 5, 0, 24, 20, 0, 1, 0, 5, 5, 1, 16, 3, 1, 16, 28, 7, 1, 1, 20, 7, 0, 0, 48, 0, 0, 0, 0, 11, 2, 48, 24, 0, 3, 15, 40, 0, 1, 1, 16, 0, 0, 0, 12, 18, 0, 0, 16, 6, 3, 48, 24, 3, 0, 48, 16, 33, 0, 48, 0, 12, 1, 16, 16, 4, 0, 48, 0, 0, 0, 49, 8, 0, 1, 0, 24, 15, 1, 32, 12, 3, 1, 2, 4, 3, 0, 0, 48, 5, 1, 0, 16, 3, 0, 0, 0, 3, 4, 32, 0, 4, 1, 32, 60, 6, 0, 48, 12, 4, 8, 16, 12, 0, 3, 0, 20, 4, 1, 0, 12, 0, 0, 0, 12, 18, 0, 0, 16, 6, 3, 48, 24, 3, 0, 48, 16, 33, 0, 48, 0, 12, 1, 16, 16, 4, 0, 48, 0, 0, 0, 49, 8, 0, 1, 0, 24, 15, 1, 32, 12, 3, 1, 2, 4, 3, 0, 0, 48, 5, 1, 0, 16, 3, 0, 0, 0, 3, 4, 32, 0, 4, 1, 32, 60, 6, 0, 48, 12, 4, 8, 16, 12, 0, 3, 0, 20, 4, 1, 0, 12, 0, 0, 0, 12, 18, 0, 0, 16, 6, 3, 48, 24, 3, 0, 48, 16, 33, 0, 48, 0, 12, 1, 16, 16, 4, 0, 48, 0, 0, 0, 49, 8, 0, 1, 0, 24, 15, 1, 32, 12, 3, 1, 2, 4, 3, 0, 0, 48, 5, 1, 0, 16, 3, 0, 0, 0, 3, 4, 32, 0, 4, 1, 32, 60, 6, 0, 48, 12, 4, 8, 16, 12, 0, 3, 0, 20, 4, 1, 0, 12, 0, 0, 0, 12, 18, 0, 0, 16, 6, 3, 48, 24, 3, 0, 48, 16, 33, 0, 48, 0, 12, 1, 16, 16, 4, 0, 48, 0, 0, 0, 49, 8, 0, 1, 0, 24, 15, 1, 32, 12, 3, 1, 2, 4, 3, 0, 0, 48, 5, 1, 0, 16, 3, 0, 0, 0, 3, 4, 32, 0, 4, 1, 32, 60, 6, 0, 48, 12, 4, 8, 16, 12, 0, 3, 0, 20, 4, 1, 0, 12, 0, 0, 0, 12, 18, 0, 0, 16, 6, 3, 48, 24, 3, 0, 48, 16, 33, 0, 48, 0, 12, 1, 16, 16, 4, 0, 48, 0, 0, 0, 49, 8, 0, 1, 0, 24, 15, 1, 32, 12, 3, 1, 2, 4, 3, 0, 0, 48, 5, 1, 0, 16, 3, 0, 0, 0, 3, 4, 32, 0, 4, 1, 32, 60, 6, 0, 48, 12, 4, 8, 16, 12, 0, 3, 0, 20, 4, 1, 0, 12, 0, 0, 0, 12, 18, 0, 0, 16, 6, 3, 48, 24, 3, 0, 48, 16, 33, 0, 48, 0, 12, 1, 16, 16, 4, 0, 48, 0, 0, 0, 49, 8, 0, 1, 0, 24, 15, 1, 32, 12, 3, 1, 2, 4, 3, 0, 0, 48, 5, 1, 0, 16, 3, 0, 0, 0, 3, 4, 32, 0, 4, 1, 32, 60, 6, 0, 48, 12, 4, 8, 16, 12, 0, 3, 0, 20, 4, 1, 0, 12, 0, 0, 0, 12, 18, 0, 0, 16, 6, 3, 48, 24, 3, 0, 48, 16, 33, 0, 48, 0, 12, 1, 16, 16, 4, 0, 48, 0, 0, 0, 49, 8, 0, 1, 0, 24, 15, 1, 32, 12, 3, 1, 2, 4, 3, 0, 0, 48, 5, 1, 0, 16, 3, 21, 48, 0, 3, 5, 0, 0, 3, 0, 1, 13, 41, 0, 0, 12, 20, 0, 0, 12, 0, 4, 54, 56, 0, 0, 49, 16, 0, 0, 48, 0, 19, 0, 0, 0, 0, 1, 32, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


# This first step is just base64-decode.

bits = []
for i in x:
  bits.append((i>>5) & 1)
  bits.append((i>>4) & 1)
  bits.append((i>>3) & 1)
  bits.append((i>>2) & 1)
  bits.append((i>>1) & 1)
  bits.append((i>>0) & 1)

bytes = []
for b in range(0, len(bits), 8):
  bytes.append(chr(int(''.join(map(str, bits[b:b+8])), 2)))

# Now, we implement a bunch of the VM methods and use python
# arrays/dicts to represent program memory.

off_6EE8 = []

dword_277D8 = {}

from sys import stdin, stdout

unk_7158 = [0]*128
unk_71B4 = [0]*128
unk_7210 = [0]*128
off_6EEC = [0, unk_7158, unk_71B4, unk_7210, 0]
pc = 0

def sub_10A4(): # Seems to be some kind of "flush output" method
  s = ''.join(ggg).replace('\x00', '').replace('\x01', '').replace('\x03', '')
  print repr(s)
  return None

# These functions named with their address in the binary.
def f580(a, b):
  return sub_10A4()

def f1e4(a, b):
  off_6EE8.append(a)
  return 0

def f210(a, b):
  return off_6EE8.pop()

def f274_add(a, b):
  return a+b

def f274_sub(a, b):
  return a-b

def f260_or(a, b):
  return a|b

def f274_xor(a, b):
  return a^b

def f288_inv(a, b):
  return a^0xFFFFFFFF

def f344(a, b):
  return a << (b & 0x1f)

def f380(a, b):
  return a >> (b & 0x1f) # TODO: Arithmetic

def f29c_notA(a, b):
  return int(a == 0) # Might be inverted, probably not

def f56c_nop(a, b):
  return 0

def f408_ifAjmpB(a, b):
  global pc
  if a == 0:
    pc += 1
  else:
    pc = b
  return 0

def f448(a, b):
  global pc
  pc = a
  return 0

def f464(a, b):
  global pc
  off_6EE8.append(pc+1)
  pc = a
  return 0

def f4a4(a, b):
  #print (a, b)
  return ord(ggg[a])
  
  if a <= 0x7FFF:
    pass
  else:
    a = sub_10A4()
  a = dword_277D8.get(a, 0)
  return a

ggg = ['\x00']*10240
def f4ec(a, b): # Something like "output B to location A of the display"
  ggg[a] = chr(b)
  # if b == 1:
  #   ggg[a] = '_'
  #print (a, chr(b))
  return 0
  # if a <= 0x7FFF:
  #   pass
  # else:
  #   a = 0
  #   print 'sub_10A4(%r, %r)' % (a, b)
  # dword_277D8[a] = b
  # return 0

def f5a4(a,b):
  # Originally I thought this was some kind of input,
  # because the VM seems to do some kind of validation
  # on this input. However, the flag it validates is
  # just the string that gets printed out, so whatever.
  # return ord(raw_input('(%r,%r)> ' % (a,b))[0])
  return 0

def f600(a,b):
  print 'NYI f600'

def f538(a,b):
  return (a<<8) + b

def f720(a,b):
  print 'NYI f720'

def f6c0(a,b):
  print 'NYI f6c0'

def f730(a,b):
  print 'NYI f730'

def f778(a,b):
  print 'NYI f778'

def f87c(a,b):
  print 'NYI f87c'

def f93c(a,b):
  print 'NYI f93c'

def f978(a,b):
  print 'NYI f978'

def f7dc(a,b):
  print 'NYI f7dc'
def f804(a,b):
  print 'NYI f804'
def f7b4(a,b):
  print 'NYI f7b4'
def f840(a,b):
  print 'NYI f840'
def f9f0(a,b):
  print 'NYI f9f0'
def f2b8(a,b):
  print 'NYI f2b8'
def f2d4(a,b):
  print 'NYI f2d4'
def f328(a,b):
  print 'NYI f328'
def f30c(a,b):
  print 'NYI f30c'
def f2f0(a,b):
  print 'NYI f2f0'
def fa30(a,b):
  print 'NYI fa30'
def fa68(a,b):
  print 'NYI fa68'
def fa7c(a,b):
  print 'NYI fa7c'
def f3bc(a,b):
  print 'NYI f3bc'
def f3e8(a,b):
  print 'NYI f3e8'

# At 0x6CE8. Note that ida might display shifted addresses, i.e. (ptr>>2) instead of ptr.
func_table = [
  f580,
  f1e4,
  f210,
  f274_add,
  f274_sub,
  f260_or,
  f274_xor,
  f288_inv,
  f344,
  f380,
  f29c_notA,
  f56c_nop,
  f408_ifAjmpB,
  f448,
  f464,
  f4a4,
  f4ec,
  f580,
  f5a4,
  f600,
  f538,
  f720,
  f6c0,
  f730,
  f778,
  f87c,
  f93c,
  f978,
  f7dc,
  f804,
  f7b4,
  f840,
  f9f0,
  f2b8,
  f2d4,
  f328,
  f30c,
  f2f0,
  fa30,
  fa68,
  fa7c,
  f3bc,
  f3e8,
  f56c_nop, f56c_nop, f56c_nop, f56c_nop, f56c_nop, f56c_nop, f56c_nop, f56c_nop, f56c_nop, f56c_nop, f56c_nop, f56c_nop, f56c_nop, f56c_nop, f56c_nop, f56c_nop, f56c_nop, f56c_nop, f56c_nop, f56c_nop, f56c_nop
]

# Presumably, this is an array of registers.
output_words = [None] * 1024

try:
 while True: # The VM loop at 0x0DB4
   byte1, byte2, byte3, byte4 = map(ord, bytes[4*pc:4*pc+4])
   if byte4 != 0x14: # Presumably:
     byte4 &= 0x3f   # <- the instruction
     byte3 &= 0xBF   # <- dest register
     byte2 &= 0xbf   # <- src register 1
     byte1 &= 0xbf   # <- src register 2
                     # So I guess I named the bytes backwards.
     
     # Our arrays represent words, not bytes, so don't do the up-shifts
     # byte2 <<= 2
     # byte1 <<= 2
     byte2 = output_words[byte2]
     byte1 = output_words[byte1]
   
   # byte4 <<= 2
   # byte3 <<= 2
   fff = func_table[byte4]
   #print pc, fff.__name__, byte2, byte1
   output_words[byte3] = fff(byte2, byte1)
   if (byte4 - 0xc) & 0xFFFFFFFF <= 1:
     pass
   else:
     pc += 1
except:
  raise
