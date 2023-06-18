import sys
sys.path += ['/usr/local/lib/', '/usr/local/lib/python3.11/site-packages/']
import cvc5.pythonic as cvc5

with open("./gatecodegate.asm", "r") as f:
    code = f.read()

code = (
    code.split(" ___isoc99_scanf", 1)[1]
    .split("lea     rdi, aCorrectCodegat", 1)[0]
    .strip()
)

code = code.split("\n")
code = [x.strip() for x in code]

registers = {
    x: cvc5.BitVec(x, 32)
    for x in [
        "eax",
        "ebx",
        "ecx",
        "edx",
        "esi",
        "edi",
        "[rsp+1C8h+var_4C]",
        "[rsp+1C8h+var_50]",
        "[rsp+1C8h+var_54]",
        "[rsp+1C8h+var_58]",
        "[rsp+1C8h+var_5C]",
        "[rsp+1C8h+var_60]",
        "[rsp+1C8h+var_64]",
        "[rsp+1C8h+var_68]",
    ]
}

gates = {
    "gate_and": lambda x, y: x & y,
    "gate_or": lambda x, y: x | y,
    "gate_xor": lambda x, y: x ^ y,
    "gate_not": lambda x, y: ~x,
    "gate_shl": lambda x, y: x << y,
    "gate_shr": lambda x, y: cvc5.LShR(x, y),
}


def getval(x, line):
    if x in registers:
        return registers[x]
    elif x.endswith("h"):
        return cvc5.BitVecVal(int(x[:-1], 16), 32)
    elif x.isdigit():
        return cvc5.BitVecVal(int(x), 32)
    else:
        raise Exception(f"Unknown operand: {x}; {line}")

print('building...')

for line_num, line in enumerate(code):
    if line_num%1000 == 0: print(line_num/len(code))
    line = line.replace(",", "").split()
    opcode = line[0]
    if opcode == "mov":
        dst = line[1]
        src = line[2]
        registers[dst] = getval(src, (line_num, line))

    elif opcode == "xor":
        dst = line[1]
        src = line[2]

        registers[dst] = registers[dst] ^ getval(src, (line_num, line))

    elif opcode == "call":
        gate = line[1]

        result = gates[gate](registers["edi"], registers["esi"])
        registers["eax"] = result

    else:
        raise Exception(f"Unknown opcode: {opcode}; {line}")

print('built!')

s = cvc5.Solver()
s.add(registers["eax"] == 0)
print(s.check())
print(s.model())
