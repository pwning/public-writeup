# solve script for lost_modulus
# author: f0xtr0t

from pwn import *
from Crypto.Util.number import *
from gmpy import *
from os import getenv
from random import random


commands_run = 0
commands_run_prog = log.progress("Commands run")


def cmd(c, inp):
    global commands_run
    commands_run += 1
    commands_run_prog.status(str(commands_run))
    conn.recvuntil("cmd: ")
    conn.sendline(c)
    conn.recvuntil("input: ")
    conn.sendline(long_to_bytes(inp).encode('hex'))
    return bytes_to_long(conn.recvline().strip().decode('hex'))


def cmdA(inp):
    return cmd('A', inp)


def cmdB(inp):
    return cmd('B', inp)


def stage0():
    global conn, flag_enc
    if getenv('LOCAL') != "TRUE":
        conn = remote('13.112.92.9', 21701)
    else:
        conn = process('./crypto-33dee9470e5b5639777f7c50e4c650e3.py')
    conn.recvline()
    flag_enc = conn.recvline().strip()
    flag_enc = bytes_to_long(flag_enc.decode('hex'))
    log.success("Stage 0: Complete")


memo = {}


def stage1():
    global memo
    prog = log.progress("Stage 1")
    for i in xrange(1024):
        prog.status(str(i))
        if i % 2 == 0:
            val = cmdA(2 ** i)
        else:
            prev = memo[2 ** (i - 1)]
            val = prev * prev
        memo[2 ** i] = val
    prog.success("Complete")


def encode(inp):
    global memo
    if random() < 0.1:
        memo[inp] = cmdA(inp)
        return memo[inp]
    val = None
    inp_copy = inp
    for k in sorted(memo.keys())[::-1]:
        while k <= inp:
            if val is None:
                val = 1
            val *= memo[k]
            inp -= k
    memo[inp_copy] = val
    assert inp == 0, repr(inp)
    return val


def stage2():
    global n
    checks = 0
    low = 0
    high = 2**1023
    prog = log.progress("Stage 2")
    while low <= high:
        mid = (low + high) // 2
        checks += 1
        prog.status("low = %s, high = %s" %
                    (hex(low), hex(high)))
        test = mid * 2 + 1
        y = cmdB(encode(test))
        x = test % 256
        if x != y:
            high = mid - 1
        elif x == y:
            low = mid + 1
        else:
            assert False
    prog.success("Complete")
    n = low * 2 + 1


def stage3():
    global flag
    shifter = invert(256, n * n)
    known_flag = []
    prog = log.progress("Stage 3")
    for lsh in xrange(128):
        assert lsh == len(known_flag)
        val = flag_enc
        prev_lsh = lsh - 1
        subtr_val = 0
        while prev_lsh >= 0:
            prev = known_flag[prev_lsh]
            subtr_val *= 256
            subtr_val += prev
            prev_lsh -= 1
        if lsh > 0:
            neg = ((n * n) - subtr_val) % (n * n)
            val = val * cmdA(neg)
        test = pow(val, shifter ** lsh, n * n)
        known_flag.append(cmdB(test))
        if known_flag[-1] == 0:
            break
        prog.status(repr(''.join(map(chr, known_flag))[::-1]))
    flag = ''.join(map(chr, known_flag))[::-1].strip('\0')
    prog.success("Complete")


stage0()
stage1()
stage2()
stage3()
log.success("FLAGE!!! " + repr(flag))
