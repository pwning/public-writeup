from __future__ import print_function
import ast
import collections
import sys

sys.setrecursionlimit(100000)

with open('test.txt') as inf:
    rl = lambda: inf.readline().strip().split()
    tree = rl()
    conds = [(rl(), rl(), rl()) for _ in range(16)]

Node = collections.namedtuple('Node', 'B V1 V2')

stack = []
value = False
for i in tree[3:]: # skip C D C initialization
    if i.endswith(']') and i[0] in 'ch':
        bit = ast.literal_eval(i[1:])
        op = i[0]
    elif i in 'cdhi':
        bit = i in 'di'
        op = i
    else:
        raise ValueError("unexpected operation %s" % i)

    if op in 'cd':
        stack.append(value)
        value = bit
    else:
        x = stack.pop()
        value = Node(bit, value, x)


def parse_cond(cond):
    assert len(cond) % 2 == 1
    cur = value
    b = True
    c = []
    M = []
    B = []

    for i in range(0, len(cond)-1, 2):
        e = cond[i] == 'e'
        f = cond[i+1] == 'e'

        b1 = cur.B
        if e:
            cur = cur.V1
        else:
            cur = cur.V2

        assert isinstance(b1, bool)

        b2 = cur.B
        if f:
            cur = cur.V1
        else:
            cur = cur.V2

        if e ^ b1:
            c.append(b2)
        else:
            Mr = [False] * 96
            Br = True
            for bit in c:
                if isinstance(bit, bool):
                    Br ^= bit
                else:
                    Mr[bit[0]] ^= True
            M.append(Mr)
            B.append(Br)
            c = [b2]

        print(e == b1, b2)
    print()
    return M, B

equations = []
for a, b, c in conds:
    ac = parse_cond(a)
    bc = parse_cond(b)
    cc = parse_cond(c)
    equations.append((ac, bc, cc))

import gf2

for i in range(1<<16):
    if i % 100 == 0:
        print(i)
    As = []
    Bs = []
    for j in range(16):
        if i & (1 << j):
            As += equations[j][0][0]
            Bs += equations[j][0][1]
            As += equations[j][1][0]
            Bs += equations[j][1][1]
        else:
            As += equations[j][2][0]
            Bs += equations[j][2][1]
    for soln in gf2.solve_gf2(As, Bs):
        print(soln)

# [0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0]
