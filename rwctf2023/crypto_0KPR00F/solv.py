"""Solver for 0KPR00F."""

from py_ecc import bn128 as lib

FQ, FQ2, FQ12, field_modulus = lib.FQ, lib.FQ2, lib.FQ12, lib.field_modulus
G1, G2, G12, b, b2, b12, is_inf, is_on_curve, eq, add, double, curve_order, multiply = (
    lib.G1,
    lib.G2,
    lib.G12,
    lib.b,
    lib.b2,
    lib.b12,
    lib.is_inf,
    lib.is_on_curve,
    lib.eq,
    lib.add,
    lib.double,
    lib.curve_order,
    lib.multiply,
)
pairing, neg = lib.pairing, lib.neg

from ast import literal_eval
from pwn import *

conn = remote("47.254.47.63", 13337)
conn.recvline()
conn.recvline()
conn.recvline()
PK = literal_eval(conn.recvline().decode())
conn.recvuntil(b"now give me your proof\n")

PKC = [(FQ(a), FQ(b)) for a, b in PK[0]]
PKCa = [(FQ(a), FQ(b)) for a, b in PK[1]]

# Consider PiH to be G1
PiH = G1
# PiC = [t^4 - 10 t^3 + 35 t^2 - 50 t + 24]G1
PiC_4 = PKC[4]
PiC_3 = neg(multiply(PKC[3], 10))
PiC_2 = multiply(PKC[2], 35)
PiC_1 = neg(multiply(PKC[1], 50))
PiC_0 = multiply(PKC[0], 24)
PiC = add(PiC_4, add(PiC_3, add(PiC_2, add(PiC_1, PiC_0))))
# PiCa = [a t^4 - 10 a t^3 + 35 a t^2 - 50 a t + 24 a]G1
PiCa_4 = PKCa[4]
PiCa_3 = neg(multiply(PKCa[3], 10))
PiCa_2 = multiply(PKCa[2], 35)
PiCa_1 = neg(multiply(PKCa[1], 50))
PiCa_0 = multiply(PKCa[0], 24)
PiCa = add(PiCa_4, add(PiCa_3, add(PiCa_2, add(PiCa_1, PiCa_0))))

proof = (PiC, PiCa, PiH)

conn.sendline(str(proof).encode())

log.info("Sent proof, now waiting for flag to show up")
log.success(conn.recvline().decode())
# Congratulations,Here is flag:rwctf{How_do_you_feel_about_zero_knowledge_proof?}
