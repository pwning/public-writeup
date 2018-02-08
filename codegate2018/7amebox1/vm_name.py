#!/usr/bin/env python

import string
import random
import _7amebox
from hashlib import sha1

'''
# proof of work
print """
------------------------------------------------------------------------------------
if not (answer.startswith(prefix) and sha1(answer).hexdigest().endswith('000000')):
    print 'nope'
    exit(-1)
------------------------------------------------------------------------------------
"""
prefix = ''.join(random.sample(string.letters + string.digits, 6))
print 'prefix : {}'.format(prefix)
answer = raw_input('answer : ')
if not (answer.startswith(prefix) and sha1(answer).hexdigest().endswith('000000')):
    print 'nope'
    exit(-1)
'''

firmware = 'mic_check.firm'

def run(stdin, stdout):
    emu = _7amebox.EMU()
    emu.filesystem.load_file('flag')
    emu.register.init_register()
    emu.init_pipeline(stdin, stdout)
    emu.load_firmware(firmware)
    emu.bp(0xf5f9e)
    emu.execute()
    #emu.disas(_7amebox.CODE_DEFAULT_BASE, limit=9999999)

import socketserver
class EMUHandler(socketserver.StreamRequestHandler):
    def handle(self):
        run(self.rfile, self.wfile)

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

HOST, PORT = "localhost", 1235
server = ReusableTCPServer((HOST, PORT), EMUHandler)
server.allow_reuse_address = True
server.serve_forever()

