import new_opcodes
import dis
import marshal

code = marshal.loads(open('crypt.pyc', 'rb').read()[8:])
print "module:"
dis.dis(code)
print "encrypt:"
dis.dis(code.co_consts[2])
print "decrypt:"
dis.dis(code.co_consts[3])
