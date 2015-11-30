smt = 'boolector'

# Define some functions for cross-compatability between z3 and boolector.
# (When working on this challenge, I started with z3 and then switched to
# boolector for performance reasons).
if smt == 'z3':
  from z3 import *
  def AShR(x, y):
    return x >> y
  
  Const = BitVecVal
  Var = BitVec
  def width(x):
    return x.size()
elif smt == 'boolector':
  from boolector import *
  def AShR(x, y):
    return x.btor.Sra(x, y)
  def LShR(x, y):
    return x.btor.Srl(x, y)
  def width(x):
    return x.width
  
  ctxt = Boolector()
  ctxt.Set_opt('model_gen', 1)
  Const = ctxt.Const
  def simplify(x):
    return x
  def Var(name, width):
    return ctxt.Var(width, name)
  def Concat(*args):
    return reduce(ctxt.Concat, args)
  def Extract(high, low, x):
    return ctxt.Slice(x, high, low)
  def SignExt(ext, x):
    return ctxt.Sext(x, ext)
  def ZeroExt(ext, x):
    return ctxt.Uext(x, ext)

class Reg(object):
  """Represents an x86 register, or a slice thereof. (Also used for stack slots)"""
  def __init__(self, name, high, low):
    if isinstance(name, Reg):
      parent = name
      name = parent.name
      low += parent.low
      high += parent.low
      assert high <= parent.high

    assert high >= low
    self.dat = name, high, low

  @property
  def name(self):
    return self.dat[0]
  @property
  def high(self):
    return self.dat[1]
  @property
  def low(self):
    return self.dat[2]

  @property
  def bits(self):
    return self.high - self.low + 1

  def __getitem__(self, index):
    assert isinstance(index, slice) and index.step is None
    return Reg(self, index.start, index.stop)

rax = Reg('rax', 63, 0)
rcx = Reg('rcx', 63, 0)
rdx = Reg('rdx', 63, 0)
rbx = Reg('rbx', 63, 0)
rbp = Reg('rbp', 63, 0)
rsi = Reg('rsi', 63, 0)
rdi = Reg('rdi', 63, 0)
r8 = Reg('r8', 63, 0)
r9 = Reg('r9', 63, 0)
r10 = Reg('r10', 63, 0)
r11 = Reg('r11', 63, 0)
r12 = Reg('r12', 63, 0)
r13 = Reg('r13', 63, 0)
r14 = Reg('r14', 63, 0)
r15 = Reg('r15', 63, 0)
gpregs = [rax, rcx, rdx, rbx, rbp, rsi, rdi, r8, r9, r10, r11, r12, r13, r14, r15]

eax = Reg(rax, 31, 0)
ecx = Reg(rcx, 31, 0)
edx = Reg(rdx, 31, 0)
ebx = Reg(rbx, 31, 0)
ebp = Reg(rbp, 31, 0)
esi = Reg(rsi, 31, 0)
edi = Reg(rdi, 31, 0)
r8d = Reg(r8, 31, 0)
r9d = Reg(r9, 31, 0)
r10d = Reg(r10, 31, 0)
r11d = Reg(r11, 31, 0)
r12d = Reg(r12, 31, 0)
r13d = Reg(r13, 31, 0)
r14d = Reg(r14, 31, 0)
r15d = Reg(r15, 31, 0)

ax = Reg(rax, 15, 0)
cx = Reg(rcx, 15, 0)
dx = Reg(rdx, 15, 0)
bx = Reg(rbx, 15, 0)
bp = Reg(rbp, 15, 0)
si = Reg(rsi, 15, 0)
di = Reg(rdi, 15, 0)
r8w = Reg(r8, 15, 0)
r9w = Reg(r9, 15, 0)
r10w = Reg(r10, 15, 0)
r11w = Reg(r11, 15, 0)
r12w = Reg(r12, 15, 0)
r13w = Reg(r13, 15, 0)
r14w = Reg(r14, 15, 0)
r15w = Reg(r15, 15, 0)

al = Reg(rax, 7, 0)
cl = Reg(rcx, 7, 0)
dl = Reg(rdx, 7, 0)
bl = Reg(rbx, 7, 0)
bpl = Reg(rbp, 7, 0)
sil = Reg(rsi, 7, 0)
dil = Reg(rdi, 7, 0)
r8b = Reg(r8, 7, 0)
r9b = Reg(r9, 7, 0)
r10b = Reg(r10, 7, 0)
r11b = Reg(r11, 7, 0)
r12b = Reg(r12, 7, 0)
r13b = Reg(r13, 7, 0)
r14b = Reg(r14, 7, 0)
r15b = Reg(r15, 7, 0)

ah = Reg(rax, 15, 8)
ch = Reg(rcx, 15, 8)
dh = Reg(rdx, 15, 8)
bh = Reg(rbx, 15, 8)

var_68 = 33
var_51 = 32
var_50 = 31
var_4F = 30
var_4E = 29
var_4D = 28
var_4C = 27
var_4B = 26
var_4A = 25
var_49 = 24
var_48 = 23
var_47 = 22
var_46 = 21
var_45 = 20
var_44 = 19
var_43 = 18
var_42 = 17
var_41 = 16
var_40 = 15
var_3F = 14
var_3E = 13
var_3D = 12
var_3C = 11
var_3B = 10
var_3A = 9
var_39 = 8
var_38 = 7
var_37 = 6
var_36 = 5
var_35 = 4
var_34 = 3
var_33 = 2
var_32 = 1
var_31 = 0

# We treat the i/o buffers and stack slots as registers;
# a quick peek at the asm confirms that, in this case,
# the approach is sound.
outbuf = [Reg('y'+str(i), 7, 0) for i in range(0x1F)]
inbuf = [Reg('x'+str(i), 7, 0) for i in range(0x12)]
stack = [Reg('t'+str(i), 7, 0) for i in range(34)]

class State(object):
  def __init__(self):
    self.dict = {reg.name:Var(reg.name, reg.bits) for reg in gpregs+outbuf+inbuf+stack}
  def __getitem__(self, reg):
    """Get the current expression for a particular register. Passes through integers."""
    if isinstance(reg, (int, long)):
      return reg
    val = self.dict[reg.name]
    if reg.low == 0 and reg.bits == width(val):
      return val
    else:
      return Extract(reg.high, reg.low, val)
  def __setitem__(self, reg, val):
    """Update the state with an expression (auto-converts integers to BitVec constants)."""
    if isinstance(val, (int, long)):
      val = Const(val, reg.bits)
    else:
      assert width(val) == reg.bits

    oldval = self.dict[reg.name]
    top = width(oldval) - 1
    newval = filter(None, [
      Extract(top, reg.high+1, oldval) if top != reg.high else None,
      val,
      Extract(reg.low-1, 0, oldval) if reg.low != 0 else None,
    ])
    self.dict[reg.name] = simplify(Concat(*newval) if len(newval) > 1 else newval[0])

state = State()

# Implementations of the instructions used by nobranch.

def _mov(dst, src):
  state[dst] = state[src]

def _movzx(dst, src):
  state[dst] = ZeroExt(dst.bits-src.bits, state[src])

def _and(dst, src):
  state[dst] &= state[src]

def _shr(dst, src):
  state[dst] = LShR(state[dst], state[src])

def _add(dst, src):
  state[dst] += state[src]

def _sar(dst, src):
  state[dst] = AShR(state[dst], state[src])

def _shl(dst, src):
  state[dst] <<= state[src]

def lea(args):
  dst, src = args.split(', ', 1)
  dst = eval(dst)
  assert src[0] == '[' and src[-1] == ']'

  val = Const(0, 64)
  for term in src[1:-1].replace('-', '+-').split('+'):
    if '*' in term:
      x, y = term.split('*', 1)
      val += state[eval(x)] * state[eval(y)]
    else:
      val += state[eval(term)]

  if dst.bits == 32:
    state[dst] = Extract(31, 0, val)
  else:
    state[dst] = val

def _sub(dst, src):
  state[dst] -= state[src]

def _imul(*args):
  if len(args) == 1:
    src, = args
    if src.bits == 8:
      state[ax] = SignExt(8, state[al]) * SignExt(8, state[src])
    elif src.bits == 16:
      res = SignExt(16, state[ax]) * SignExt(16, state[src])
      state[dx] = Extract(31, 16, res)
      state[ax] = Extract(15,  0, res)
    elif src.bits == 32:
      res = SignExt(32, state[eax]) * SignExt(32, state[src])
      state[edx] = Extract(63, 32, res)
      state[eax] = Extract(31,  0, res)
    else:
      assert False
  elif len(args) == 2:
    dst, src = args
    state[dst] *= state[src]
  elif len(args) == 3:
    dst, src1, src2 = args
    state[dst] = state[src1] * state[src2]
  else:
    assert False

def _neg(dst):
  state[dst] = -state[dst]

def _or(dst, src):
  state[dst] |= state[src]

def _not(dst):
  state[dst] = ~state[dst]

def _xor(dst, src):
  state[dst] ^= state[src]

print "executing...", 

counter = 0
for line in open('nobranch.txt'):
  counter += 1
  if counter % (27015/100) == 0:
    print str(counter*100 / 27015) + '%',
  line = line.strip()
  if not line: continue
  f, args = line.split('\t', 1)
  try:
    if f == 'lea':
      lea(args)
    else:
      eval('_%s(%s)' % (f, args))
  except:
    print
    print line
    raise

print "\nsolving..."

if smt == 'z3':
  s = Solver()
  
  # The real chal
  s.add(*[state[x] == ord(y) for x, y in zip(outbuf, 'HMQhQLi6VqgeOj78AbiaqquK3noeJt')])
  
  # For testing:
  # 'AAAAAAAAAAAAAAAAAA'
  # s.add(*[state[x] == ord(y) for x, y in zip(outbuf, 'jw6wLPdwMYxqPyQJqs0hqRXCUaSKYT')])
  
  print s.check()
  m = s.model()
  print repr(''.join(chr(m[state[x]].as_long()) for x in inbuf))

elif smt == 'boolector':
  ctxt.Assert(*[state[x] == ord(y) for x, y in zip(inbuf, '9447{')])
  ctxt.Assert(*[state[x] == ord(y) for x, y in zip(outbuf, 'HMQhQLi6VqgeOj78AbiaqquK3noeJt')])
  print {10:"sat", 20:"unsat", 0:"unknown", 1:"parse error"}.get(ctxt.Sat())
  print repr(''.join(chr(int(state[x].assignment, 2)) for x in inbuf))
