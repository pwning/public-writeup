import sys

TRANSFORMS = {
    "MOVIqq": lambda a,b: "{} = {}".format(a, b),
    "MOVIqd": lambda a,b: "{} = {}".format(a, b),
    "MOVIqw": lambda a,b: "{} = {}".format(a, b),
    "MOVqw": lambda a,b: "{} = {}".format(a, b),
    "ADD": lambda a,b: "{} += {}".format(a, b),
    "SUB": lambda a,b: "{} -= {}".format(a, b),
    "XOR": lambda a,b: "{} ^= {}".format(a, b),
    "NOT": lambda a,b: "{} = ~{}".format(a, b),
    "NEG": lambda a,b: "{} = -{}".format(a, b),
    "AND": lambda a,b: "{} &= {}".format(a, b),
    "OR": lambda a,b: "{} |= {}".format(a, b),
    "SHR": lambda a,b: "{} = LShR({}, {})".format(a, a, b),
    "SHL": lambda a,b: "{} <<= {}".format(a, b),
    "MULU": lambda a,b: "{} *= {}".format(a, b),
    "CMPeq": lambda a,b: "solve.add({} == {})\nR1 = v".format(a, b),

}

def transform(op, arg1, arg2):
    return TRANSFORMS[op](arg1, arg2)

def do(s):
    z3 = []
    z3.append('v = BitVector(64)')
    z3.append('R1 = v')
    ls = s.split('\n')
    for l in ls:
        if l == '':
            continue
        op, arg1, arg2 = l.split()[-3:]
        arg1 = arg1[:-1]
        z3.append(transform(op, arg1, arg2))
    z3.append('solve.add(R1 == R7)')
    return '\n'.join(z3)

if __name__ == '__main__':
    print(do(open(sys.argv[1]).read()))
