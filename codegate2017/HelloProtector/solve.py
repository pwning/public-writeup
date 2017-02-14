#!/usr/bin/python

buf = 'c0nGr47uRaTioN!_Y0u_F0uNd_A_k3y!'
enc = '370610663A38504D020163013663537F4A624B2D4D64767D25755E6E740C7C18'.decode('hex')

prev = 0
vol = ''
for i in xrange(len(buf)):
    key = ord(enc[i]) ^ ord(buf[i])
    vol += chr(prev ^ key)
    prev = key

print vol

