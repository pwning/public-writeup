import re
from ast import literal_eval

import base64
from Crypto.Cipher import DES
from Crypto.Util.Padding import unpad
import struct

p1 = 4557847193904795529 ^ -1787229411635844770
mapping = {}
for p0, row in enumerate(open("strings.txt")):
    key = bytearray([0] * 8)
    key[0] = (p1 >> 56) & 0xff
    for i in range(1, 8):
        key[i] = (((p1 << (i * 8)) >> 56) << (p0 & 63)) & 0xff

    res = DES.new(key, mode=DES.MODE_CBC, iv=b"\0" * 8).decrypt(base64.b64decode(row))
    mapping[p0] = unpad(res, 8).decode()

code = open("darkmagic.procyon", "r").read()
code = code.replace("xor:long(ldc:long(-1787229411635844770L), ldc:long(96L))", "ldc:long(-1787229411635844802L)")
code = re.sub(r"and:int\((ldc:int\(\d+\)), ldc:int\(-1\)\)", r"\1", code)
code = re.sub(
    r"invokedynamic:String\(invokestatic com/rw/rwctf2023/DarkMagic.v0007_1c4783e5646d75c310ec:\(Ljava/lang/invoke/MethodHandles\$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;\)Ljava/lang/Object;, [^,]+, ldc:int\((\d+)\), ldc:long\(-1787229411635844802L\)\)",
    lambda m: '"' + mapping[int(m.group(1))] + '"',
    code)
code = code.replace(r'\"', r'\u0022')
def xor(x, key):
    return "".join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(x))
def decrypt_v0014(m):
    key = literal_eval(m.group(6))
    cls = xor(literal_eval(m.group(3)), key)
    meth = xor(literal_eval(m.group(4)), key)
    sig = xor(literal_eval(m.group(5)), key)
    return f"{cls}::{meth}("
code = re.sub(
    r"""invokedynamic:[^(]+\(invokestatic com/rw/rwctf2023/DarkMagic.v0014_0cc215bba1599024528ec63:\(Ljava/lang/Object;Ljava/lang/String;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/String;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;\)Ljava/lang/Object;, \w+:([^-]+)("[^"]+"|[^,]+), ("[^"]+"|[^,]+), ("[^"]+"|[^,]+), ("[^"]+"|[^,]+), ("[^"]+"|[^,]+), ("[^"]+"|[^,]+), ("[^"]+"|[^,]+), ("[^"]+"|[^,]+), ("[^"]+"|[^,]+), ("[^"]+"|[^,]+)(, )?""",
    decrypt_v0014,
    code)

with open("darkmagic-deobfuscated.procyon", "w") as outf:
    outf.write(code)
