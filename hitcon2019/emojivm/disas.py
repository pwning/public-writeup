#!/usr/bin/env python3
OP_TABLE = {
    127539: 1,
    10133: 2,
    10134: 3,
    10060: 4,
    10067: 5,
    10062: 6,
    128107: 7,
    128128: 8,
    128175: 9,
    128640: 10,
    127542: 11,
    127514: 12,
    9196: 13,
    128285: 14,
    128228: 15,
    128229: 16,
    127381: 17,
    127379: 18,
    128196: 19,
    128221: 20,
    128289: 21,
    128290: 22,
    128721: 23,
}
DATA_TABLE = {
    128512: 0,
    128513: 1,
    128514: 2,
    129315: 3,
    128540: 4,
    128516: 5,
    128517: 6,
    128518: 7,
    128521: 8,
    128522: 9,
    128525: 10,
}

OP_NAMES = {
    1: 'nop',
    2: 'add',
    3: 'sub',
    4: 'mul',
    5: 'mod',
    6: 'xor',
    7: 'and',
    8: 'lt',
    9: 'eq',
    10: 'jmp',
    11: 'jnz',
    12: 'jz',
    13: 'push', # immediate
    14: 'pop',
    15: 'gget',
    16: 'gset',
    17: 'galloc',
    18: 'gfree',
    19: 'gread',
    20: 'gwrite',
    21: 'dumpstack',
    22: 'printint',
    23: 'halt',
}

import sys
f = open(sys.argv[1], 'r').read()
pos = 0
while pos < len(f):
    print('%02d:' % pos, end=' ')
    c = ord(f[pos])
    assert c in OP_TABLE
    op = OP_TABLE[c]
    if op == 13:
        pos += 1
        val = DATA_TABLE[ord(f[pos])]
        print(OP_NAMES[op], val)
    else:
        print(OP_NAMES[op])
    pos += 1
