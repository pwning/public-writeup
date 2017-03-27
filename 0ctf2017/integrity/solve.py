#!/usr/bin/python -u

from hashlib import md5
from Crypto import Random
import socket

HOST, PORT = "202.120.7.217", 8221
s = socket.create_connection((HOST,PORT))

def read_until(c):
    buf = ""
    while not buf.endswith(c):
        buf += s.recv(1)
    return buf

def enc(name):
    s.send("r\n{}\n".format(name))
    read_until("Here is your secret:")
    read_until("\n")
    secret = read_until("\n")[:-1].decode('hex')
    return [secret[16*i: 16*i+16] for i in range(len(secret) / 16)]

def login(x):
    s.send("l\n{}\n".format("".join(x).encode('hex')))
    print read_until("\n")
    print read_until("\n")
    print read_until("\n")

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 

m = md5(pad("admin")).digest() + "admin"
g = enc(m)
login(g[1:])
