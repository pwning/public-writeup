from prog import prog

# XXX division is float rounded
arith_ops = {1: "add", 2: "sub", 3: "mul", 4: "div", 10: "cmp", 11: "and", 12: "or", 13: "xor"}
jmp_ops = {5: "jmp", 6: "jg", 7: "jl", 8: "je", 9: "jne"}
# vm starts at 0x2F7
for pc in range(len(prog)):
    amode, opc, x, y = prog[pc]
    print(f'0x{pc:04x}: ', end="")
    if opc == 0:
        print("halt")
    elif opc in arith_ops:
        op = arith_ops[opc]
        if amode == 0:
            print(f"{op} r{x}, mem[r{y}]")
        elif amode == 1:
            print(f"{op} r{x}, {y:#x}")
        elif amode == 2:
            print(f"{op} r{x}, r{y}")
        else: raise NotImplementedError()
    elif opc in jmp_ops:
        op = jmp_ops[opc]
        if amode == 1:
            print(f"{op} 0x{x:04x}")
        elif amode == 2:
            print(f"{op} r{x}")
        else: raise NotImplementedError()
    elif opc == 15:
        if amode == 0:
            print(f"mov r{x}, mem[r{y}]")
        elif amode == 1:
            print(f"mov r{x}, {y:#x}")
        elif amode == 2:
            print(f"mov r{x}, r{y}")
        elif amode == 3:
            print(f"mov mem[{x}], r{y}")
        else: raise NotImplementedError()
    elif opc == 16:
        print(f"call 0x{x:04x}")
    elif opc == 17:
        print(f"ret")
    elif opc == 14:
        print(f"not r{x}")
    elif opc == 18:
        print(f"push r{x}")
    elif opc == 19:
        print(f"pop r{x}")
    elif opc == 20:
        print(f"xchg r{x}, r{y}")
    elif opc in [21, 22]:
        op = {21: "shl", 22: "shr"}[opc]
        if amode == 1:
            print(f"{op} r{x}, {y}")
        elif amode == 2:
            print(f"{op} r{x}, r{y}")
        else: raise NotImplementedError()
    elif opc == 23:
        print("pushad")
    elif opc == 24:
        print("popad")
    else: raise NotImplementedError()
