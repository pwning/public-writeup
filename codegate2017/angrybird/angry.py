#!/usr/bin/env python2.7
from z3 import *

def main():
  S = Solver()

  s = [BitVec('x%d'%i, 8) for i in range(20)]

  #sub_40070C(); hmmmmmm
  #strncmp((const char *)&off_606038, "hello", 5uLL)

  off_606018 = BitVec('off_606018', 8)
  off_606020 = BitVec('off_606020', 8)
  off_606022 = BitVec('off_606022', 8)
  off_606028 = BitVec('off_606028', 8)
  off_606029 = BitVec('off_606029', 8)
  off_606038 = BitVecVal(ord('h'), 8)
  off_606039 = BitVecVal(ord('e'), 8)
  off_60603A = BitVecVal(ord('l'), 8)
  off_60603B = BitVecVal(ord('l'), 8)

  v8 = s[0] ^ s[1]
  S.add(Not( (s[0] ^ s[1]) <= 15 ))
  v8 = s[0] & s[1]
  S.add(Not( (s[0] & s[1]) > 80 ))
  v8 = s[18] & s[1]
  S.add(Not( (s[18] & s[1]) > 48 ))
  v8 = s[7] & s[4] ^ s[0]
  S.add(Not( v8 > 44 ))
  v8 = s[0] & s[2]
  S.add(Not( (s[0] & s[2]) <= 72 ))
  v8 = s[11] & s[17]
  S.add(Not( (s[11] & s[17]) <= 72 ))
  v8 = s[0] ^ s[13]
  S.add(Not( (s[0] ^ s[13]) <= 43 ))
  v8 = s[13] ^ s[10]
  S.add(Not( (s[13] ^ s[10]) <= 66 ))
  v8 = s[11] ^ s[16]
  S.add(Not( (s[11] ^ s[16]) > 16 ))
  v8 = s[10] ^ s[8]
  S.add(Not( (s[10] ^ s[8]) > 83 ))
  v8 = s[19] ^ s[5]
  S.add(Not( (s[19] ^ s[5]) <= 117 ))
  v8 = s[0] | s[1]
  S.add(Not( (s[0] | s[1]) <= 16 ))
  v8 = s[17] & s[3]
  S.add(Not( (s[17] & s[3]) <= 80 ))
  v8 = off_606038 ^ s[1]
  S.add(Not( (off_606038 ^ s[1]) > 23 ))
  v8 = ~s[14]
  S.add(Not( ~s[14] > 1 ))
  v8 = s[13] | s[15]
  S.add(Not( (s[13] | s[15]) <= 116 ))
  v8 = s[0] >> 5
  S.add(Not( (s[0] >> 5) <= 0 ))
  v8 = ~s[19]
  S.add(Not( ~s[19] > 1 ))
  v8 = s[1] ^ s[11]
  S.add(Not( (s[1] ^ s[11]) <= 28 ))
  v8 = s[12] ^ s[15]
  S.add(Not( (s[12] ^ s[15]) > 18 ))
  v8 = s[13] & s[1]
  S.add(Not( (s[13] & s[1]) <= 47 ))
  v8 = (s[10] ^ s[19]) & s[12]
  S.add(Not( v8 > 108 ))
  v8 = ~s[6]
  S.add(Not( ~s[6] > 1 ))
  v8 = s[1] ^ s[9]
  S.add(Not( (s[1] ^ s[9]) <= 7 ))
  v8 = s[16] >> 1
  S.add(Not( (s[16] >> 1) <= 25 ))
  v8 = off_606018 ^ s[8]
  S.add(Not( (off_606018 ^ s[8]) <= 99 ))
  v8 = ~s[6]
  S.add(Not( ~s[6] > 1 ))
  v8 = s[4] & s[12]
  S.add(Not( (s[4] & s[12]) <= 41 ))
  v8 = s[16] >> 1
  S.add(Not( (s[16] >> 1) <= 14 ))
  v8 = ~s[14]
  S.add(Not( ~s[14] > 1 ))
  v8 = s[0] >> 5
  S.add(Not( (s[0] >> 5) > 48 ))
  v8 = ~s[19]
  S.add(Not( ~s[19] > 1 ))
  v8 = s[0] ^ s[1]
  S.add(Not( (s[0] ^ s[1]) > 45 ))
  v8 = s[0] & s[1]
  S.add(Not( (s[0] & s[1]) <= 0 ))
  v8 = ~s[14]
  S.add(Not( ~s[14] > 1 ))
  v8 = s[0] ^ s[19]
  S.add(Not( (s[0] ^ s[19]) <= 95 ))
  v8 = s[0] >> 5
  S.add(Not( (s[0] >> 5) > 12 ))
  v8 = off_606020 ^ s[13]
  S.add(Not( (off_606020 ^ s[13]) <= 29 ))
  v8 = s[16] | s[7]
  S.add(Not( (s[16] | s[7]) <= 121 ))
  # v4 = BYTE4(off_606038)
  v8 = s[7] ^ s[17]
  S.add(Not( (s[7] ^ s[17]) > 42 ))
  v8 = ~s[19]
  S.add(Not( ~s[19] > 1 ))
  v8 = s[15] & s[3]
  S.add(Not( (s[15] & s[3]) <= 61 ))
  v8 = s[19] ^ s[15]
  S.add(Not( (s[19] ^ s[15]) > 94 ))
  v8 = s[0] ^ s[1]
  S.add(Not( (s[0] ^ s[1]) > 125 ))
  v8 = s[18] & s[1]
  S.add(Not( (s[18] & s[1]) <= 0 ))
  v8 = (s[16] ^ s[5]) & s[1]
  S.add(Not( v8 > 66 ))
  v8 = ~s[14]
  S.add(Not( ~s[14] > 1 ))
  v8 = s[0] >> 5
  S.add(Not( (s[0] >> 5) <= 0 ))
  v8 = off_606029 ^ s[17]
  S.add(Not( v8 <= 46 ))
  v8 = ~s[19]
  S.add(Not( ~s[19] > 1 ))
  v8 = s[4] ^ s[19]
  S.add(Not( (s[4] ^ s[19]) > 106 ))
  v8 = s[8] & s[7]
  S.add(Not( (s[8] & s[7]) <= 33 ))
  v8 = s[6] | s[7]
  S.add(Not( (s[6] | s[7]) <= 118 ))
  v8 = s[18] & s[1]
  S.add(Not( (s[18] & s[1]) > 58 ))
  v8 = s[2] ^ s[8]
  S.add(Not( (s[2] ^ s[8]) <= 42 ))
  v8 = s[2] ^ s[13]
  S.add(Not( (s[2] ^ s[13]) <= 46 ))
  v8 = s[3] & s[8]
  S.add(Not( (s[3] & s[8]) <= 94 ))
  v8 = s[16] ^ s[18]
  S.add(Not( (s[16] ^ s[18]) <= 66 ))
  v8 = off_606022 ^ s[15]
  S.add(Not( v8 <= 35 ))
  v8 = s[10] ^ s[9]
  S.add(Not( (s[10] ^ s[9]) <= 23 ))
  v8 = s[18] & s[1]
  S.add(Not( (s[18] & s[1]) <= 17 ))
  v8 = s[0] & s[1]
  S.add(Not( (s[0] & s[1]) > 90 ))
  v8 = s[16] ^ s[1]
  S.add(Not( (s[16] ^ s[1]) > 63 ))
  v8 = s[18] & s[1]
  S.add(Not( (s[18] & s[1]) > 102 ))
  v8 = s[18] & s[3]
  S.add(Not( (s[18] & s[3]) <= 49 ))
  v8 = s[9] ^ s[1]
  S.add(Not( (s[9] ^ s[1]) > 26 ))
  v8 = off_606038 ^ s[15]
  S.add(Not( (off_606038 ^ s[15]) > 40 ))
  v8 = s[0] ^ s[1]
  S.add(Not( (s[0] ^ s[1]) > 55 ))
  v8 = s[13] & s[1]
  S.add(Not( (s[13] & s[1]) > 103 ))
  v8 = s[18] & s[1]
  S.add(Not( (s[18] & s[1]) <= 0 ))
  v8 = s[0] ^ s[1]
  S.add(Not( (s[0] ^ s[1]) <= 34 ))
  v8 = s[0] & s[1]
  S.add(Not( (s[0] & s[1]) > 90 ))
  v8 = s[11] ^ s[14]
  S.add(Not( (s[11] ^ s[14]) > 4 ))
  v8 = s[5] ^ s[11]
  S.add(Not( (s[5] ^ s[11]) > 50 ))
  v8 = s[18] & s[1]
  S.add(Not( (s[18] & s[1]) <= 37 ))
  v8 = s[0] ^ s[6]
  S.add(Not( (s[0] ^ s[6]) > 48 ))
  v8 = s[2] << 6
  S.add(Not( (s[2] << 6) > 1 ))
  v8 = s[0] | s[1]
  S.add(Not( (s[0] | s[1]) <= 85 ))
  v8 = s[9] ^ s[10]
  S.add(Not( (s[9] ^ s[10]) <= 66 ))
  v8 = s[10] & s[8]
  S.add(Not( (s[10] & s[8]) <= 30 ))
  v8 = s[19] ^ s[17]
  S.add(Not( (s[19] ^ s[17]) > 118 ))
  v8 = s[0] & s[17] | s[8]
  S.add(Not( v8 <= 59 ))
  v8 = s[17] ^ s[18]
  S.add(Not( (s[17] ^ s[18]) <= 94 ))
  v8 = s[18] & s[9]
  S.add(Not( (s[18] & s[9]) <= 30 ))
  v8 = s[3] ^ s[6]
  S.add(Not( (s[3] ^ s[6]) > 32 ))
  v8 = 16 * s[16]
  S.add(Not( (16 * s[16]) > 1 ))
  v8 = s[7] ^ s[3] | s[17]
  S.add(Not( v8 <= 94 ))
  v8 = s[0] | s[1]
  S.add(Not( (s[0] | s[1]) > 120 ))
  v8 = s[10] & s[18]
  S.add(Not( (s[10] & s[18]) > 81 ))
  v8 = s[6] | s[7]
  S.add(Not( (s[6] | s[7]) > 119 ))
  v8 = s[0] ^ s[6]
  S.add(Not( (s[0] ^ s[6]) <= 16 ))
  v8 = 2 * s[12]
  S.add(Not( (2 * s[12]) > 1 ))
  v8 = s[0] | s[1]
  S.add(Not( (s[0] | s[1]) <= 66 ))
  v8 = s[6] & s[1]
  S.add(Not( (s[6] & s[1]) <= 84 ))
  v8 = s[18] & s[1]
  S.add(Not( (s[18] & s[1]) > 118 ))
  v8 = s[0] ^ s[6]
  S.add(Not( (s[0] ^ s[6]) > 47 ))
  v8 = s[0] | s[1]
  S.add(Not( (s[0] | s[1]) <= 60 ))
  v8 = s[18] & s[1]
  S.add(Not( (s[18] & s[1]) <= 13 ))
  v8 = s[0] ^ s[6]
  S.add(Not( (s[0] ^ s[6]) <= 38 ))
  v8 = s[13] ^ s[10]
  S.add(Not( (s[13] ^ s[10]) > 67 ))
  v8 = 16 * s[2]
  S.add(Not( (16 * s[2]) > 1 ))
  v8 = s[0] | s[1]
  S.add(Not( (s[0] | s[1]) <= 94 ))
  v8 = s[0] & s[11]
  S.add(Not( (s[0] & s[11]) > 67 ))
  v8 = s[18] & s[1]
  S.add(Not( (s[18] & s[1]) > 48 ))
  v8 = s[0] ^ s[6]
  S.add(Not( (s[0] ^ s[6]) > 102 ))
  v8 = s[0] ^ s[19]
  S.add(Not( (s[0] ^ s[19]) > 96 ))
  v8 = s[14] ^ s[18] | s[3]
  S.add(Not( v8 != 127 ))
  v8 = 4 * s[14]
  S.add(Not( (4 * s[14]) > 1 ))
  v8 = off_60603B ^ s[11]
  S.add(Not( v8 > 97 ))
  v8 = s[6] | s[1]
  S.add(Not( (s[6] | s[1]) <= 43 ))
  v8 = s[5] & s[1]
  S.add(Not( (s[5] & s[1]) > 95 ))
  v8 = (s[14] ^ s[3]) & s[10]
  S.add(Not( v8 <= 2 ))
  v8 = s[18] & s[1]
  S.add(Not( (s[18] & s[1]) > 65 ))
  v8 = s[0] ^ s[6]
  S.add(Not( (s[0] ^ s[6]) <= 24 ))
  v8 = ~s[6]
  S.add(Not( ~s[6] > 1 ))
  v8 = s[9] ^ s[10]
  S.add(Not( (s[9] ^ s[10]) > 67 ))
  v8 = 2 * s[7]
  S.add(Not( (2 * s[7]) > 1 ))
  v8 = s[9] & s[17]
  S.add(Not( (s[9] & s[17]) > 101 ))
  v8 = s[16] & s[15] | s[18]
  S.add(Not( v8 <= 121 ))
  v8 = s[0] ^ s[16]
  S.add(Not( (s[0] ^ s[16]) <= 40 ))
  v8 = s[18] & s[3]
  S.add(Not( (s[18] & s[3]) > 50 ))
  v8 = s[3] << 6
  S.add(Not( (s[3] << 6) > 1 ))
  v8 = s[0] | s[1]
  S.add(Not( (s[0] | s[1]) <= 12 ))
  v8 = ~s[14]
  S.add(Not( ~s[14] > 1 ))
  v8 = s[0] >> 5
  S.add(Not( (s[0] >> 5) > 79 ))
  v8 = ~s[19]
  S.add(Not( ~s[19] > 1 ))
  v8 = s[0] ^ s[6]
  S.add(Not( (s[0] ^ s[6]) > 44 ))
  v8 = s[9] & s[5] | s[0]
  S.add(Not( v8 <= 28 ))
  v8 = s[0] | s[1]
  S.add(Not( (s[0] | s[1]) <= 93 ))
  v8 = s[12] | s[4]
  S.add(Not( (s[12] | s[4]) <= 40 ))
  v8 = ~s[14]
  S.add(Not( ~s[14] > 1 ))
  v8 = s[0] >> 5
  S.add(Not( (s[0] >> 5) <= 0 ))
  v8 = ~s[19]
  S.add(Not( ~s[19] > 1 ))
  v8 = ~s[14]
  S.add(Not( ~s[14] > 1 ))
  v8 = s[1] ^ s[9]
  S.add(Not( (s[1] ^ s[9]) > 8 ))
  v8 = ~s[19]
  S.add(Not( ~s[19] > 1 ))
  v8 = s[11] ^ s[14]
  S.add(Not( (s[11] ^ s[14]) <= 3 ))
  v8 = s[11] | s[9]
  S.add(Not( (s[11] | s[9]) <= 102 ))
  v8 = s[12] ^ s[15]
  S.add(Not( (s[12] ^ s[15]) > 68 ))
  v8 = s[0] & s[2]
  S.add(Not( (s[0] & s[2]) > 73 ))
  v8 = s[13] & s[1]
  S.add(Not( (s[13] & s[1]) <= 68 ))
  v8 = 16 * s[7]
  S.add(Not( (16 * s[7]) > 125 ))
  v8 = s[13] ^ s[5]
  S.add(Not( (s[13] ^ s[5]) > 79 ))
  v8 = s[12] ^ s[14]
  S.add(Not( (s[12] ^ s[14]) > 6 ))
  v8 = s[9] & s[4]
  S.add(Not( (s[9] & s[4]) <= 16 ))
  v8 = ~s[6]
  S.add(Not( ~s[6] > 1 ))
  v8 = ~s[14]
  S.add(Not( ~s[14] > 1 ))
  v8 = s[0] >> 5
  S.add(Not( (s[0] >> 5) > 74 ))
  v8 = ~s[19]
  S.add(Not( ~s[19] > 1 ))
  v8 = s[11] | s[9]
  S.add(Not( (s[11] | s[9]) <= 89 ))
  v8 = s[12] ^ s[15]
  S.add(Not( (s[12] ^ s[15]) > 46 ))
  v8 = 16 * s[7]
  S.add(Not( (16 * s[7]) <= 29 ))
  v8 = s[19] | s[7]
  S.add(Not( (s[19] | s[7]) <= 77 ))
  v8 = s[4] ^ s[6]
  S.add(Not( (s[4] ^ s[6]) > 12 ))
  v8 = ~s[6]
  S.add(Not( ~s[6] > 1 ))
  #v5 = BYTE1(off_606038)
  v8 = ~s[14]
  S.add(Not( ~s[14] > 1 ))
  v8 = s[0] >> 5
  S.add(Not( (s[0] >> 5) > 27 ))
  v8 = ~s[19]
  S.add(Not( ~s[19] > 1 ))
  v8 = s[11] | s[9]
  S.add(Not( (s[11] | s[9]) > 122 ))
  v8 = s[12] ^ s[15]
  S.add(Not( (s[12] ^ s[15]) <= 3 ))
  v8 = s[13] & s[1]
  S.add(Not( (s[13] & s[1]) <= 56 ))
  v8 = 16 * s[7]
  S.add(Not( (16 * s[7]) <= 3 ))
  v8 = s[2] ^ s[8]
  S.add(Not( (s[2] ^ s[8]) > 43 ))
  v8 = s[13] ^ s[5]
  S.add(Not( (s[13] ^ s[5]) <= 16 ))
  v8 = ~s[6]
  S.add(Not( ~s[6] > 1 ))
  v8 = ~s[6]
  S.add(Not( ~s[6] > 1 ))
  v8 = ~s[14]
  S.add(Not( ~s[14] > 1 ))
  v8 = s[0] >> 5
  S.add(Not( (s[0] >> 5) > 88 ))
  v8 = ~s[19]
  S.add(Not( ~s[19] > 33 ))
  v8 = s[12] ^ s[15]
  S.add(Not( (s[12] ^ s[15]) > 46 ))
  v8 = ~s[5]
  S.add(Not( ~s[5] > 1 ))
  v8 = s[6] & s[7] | s[3]
  S.add(Not( v8 <= 9 ))
  v8 = s[13] ^ s[5]
  S.add(Not( (s[13] ^ s[5]) > 96 ))
  v8 = ~s[6]
  S.add(Not( ~s[6] > 1 ))
  v8 = ~s[14]
  S.add(Not( ~s[14] > 1 ))
  v8 = s[0] >> 5
  S.add(Not( (s[0] >> 5) > 91 ))
  v8 = ~s[19]
  S.add(Not( ~s[19] > 1 ))
  v8 = s[11] | s[9]
  S.add(Not( (s[11] | s[9]) <= 32 ))
  v8 = s[9] & s[11]
  S.add(Not( (s[9] & s[11]) <= 32 ))
  v8 = ~s[6]
  S.add(Not( ~s[6] > 1 ))
  v8 = ~s[14]
  S.add(Not( ~s[14] > 1 ))
  v8 = ~s[19]
  S.add(Not( ~s[19] > 1 ))
  v8 = s[11] | s[9]
  S.add(Not( (s[11] | s[9]) <= 90 ))
  v8 = off_60603A ^ s[5]
  S.add(Not( v8 > 120 ))
  v8 = s[12] ^ s[15]
  S.add(Not( (s[12] ^ s[15]) > 32 ))
  v8 = 16 * s[7]
  S.add(Not( (16 * s[7]) <= 61 ))
  v8 = s[13] ^ s[5]
  S.add(Not( (s[13] ^ s[5]) <= 33 ))
  v8 = s[0] >> 5
  S.add(Not( (s[0] >> 5) > 16 ))
  v8 = ~s[19]
  S.add(Not( ~s[19] > 64 ))
  v8 = s[11] | s[9]
  S.add(Not( (s[11] | s[9]) <= 95 ))
  v8 = s[12] ^ s[15]
  S.add(Not( (s[12] ^ s[15]) > 48 ))
  v8 = s[13] & s[1]
  S.add(Not( (s[13] & s[1]) > 113 ))
  v8 = s[7] ^ s[17]
  S.add(Not( (s[7] ^ s[17]) <= 41 ))
  v8 = 16 * s[7]
  S.add(Not( (16 * s[7]) <= 63 ))
  v8 = ~s[6]
  S.add(Not( ~s[6] > 1 ))
  v8 = s[4] & s[12]
  S.add(Not( (s[4] & s[12]) <= 94 ))
  v8 = s[2] ^ s[8]
  S.add(Not( (s[2] ^ s[8]) > 43 ))
  v8 = s[16] >> 1
  S.add(Not( (s[16] >> 1) <= 57 ))
  v8 = ~s[6]
  S.add(Not( ~s[6] > 1 ))
  v8 = s[4] & s[12]
  S.add(Not( (s[4] & s[12]) > 103 ))
  v8 = s[16] >> 1
  S.add(Not( (s[16] >> 1) > 92 ))
  v8 = s[0] >> 5
  v8 = off_606039 ^ s[4]
  S.add(Not( v8 > 57 ))
  v8 = ~s[19]
  S.add(Not( ~s[19] > 1 ))
  v8 = s[19] & s[4] | s[2]
  S.add(Not( v8 <= 16 ))
  v8 = s[11] | s[9]
  S.add(Not( (s[11] | s[9]) <= 20 ))
  v8 = s[12] ^ s[15]
  S.add(Not( (s[12] ^ s[15]) > 82 ))
  v8 = s[13] | s[15]
  S.add(Not( (s[13] | s[15]) > 117 ))
  v8 = s[13] & s[1]
  S.add(Not( (s[13] & s[1]) <= 50 ))
  v8 = s[19] ^ s[5]
  S.add(Not( (s[19] ^ s[5]) > 118 ))
  v8 = s[13] ^ s[5]
  S.add(Not( (s[13] ^ s[5]) == 127 ))
  v8 = ~s[6]
  S.add(Not( ~s[6] > 1 ))
  v8 = s[4] & s[12]
  S.add(Not( (s[4] & s[12]) <= 67 ))
  v8 = s[5] & s[17]
  S.add(Not( (s[5] & s[17]) <= 56 ))
  v8 = s[16] >> 1
  S.add(Not( (s[16] >> 1) > 95 ))
  v8 = ~s[6]
  S.add(Not( ~s[6] > 1 ))
  v8 = s[7] ^ s[3] | s[17]
  S.add(Not( v8 > 95 ))
  v8 = s[4] & s[12]
  S.add(Not( (s[4] & s[12]) <= 78 ))
  v8 = s[16] >> 1
  S.add(Not( (s[16] >> 1) <= 7 ))
  v8 = s[0] >> 5
  S.add(Not( (s[0] >> 5) > 123 ))
  v8 = ~s[19]
  S.add(Not( ~s[19] > 1 ))
  v8 = s[11] | s[9]
  S.add(Not( (s[11] | s[9]) <= 101 ))
  v8 = s[13] & s[1]
  S.add(Not( (s[13] & s[1]) <= 61 ))
  v8 = 16 * s[7]
  S.add(Not( (16 * s[7]) <= 73 ))
  v8 = s[13] ^ s[5]
  S.add(Not( (s[13] ^ s[5]) <= 34 ))
  v8 = ~s[6]
  S.add(Not( ~s[6] > 1 ))
  v8 = s[4] & s[12]
  S.add(Not( (s[4] & s[12]) <= 5 ))
  v8 = ~s[6]
  S.add(Not( ~s[6] > 85 ))
  v8 = s[4] & s[12]
  S.add(Not( (s[4] & s[12]) > 113 ))
  v8 = s[16] >> 1
  S.add(Not( (s[16] >> 1) > 61 ))
  v8 = s[16] >> 1
  S.add(Not( (s[16] >> 1) > 90 ))
  v8 = s[0] >> 5
  S.add(Not( (s[0] >> 5) > 106 ))
  v8 = ~s[19]
  S.add(Not( ~s[19] > 1 ))
  v8 = s[0] ^ s[1]
  S.add(Not( (s[0] ^ s[1]) > 84 ))
  v8 = s[0] & s[1]
  S.add(Not( (s[0] & s[1]) > 81 ))
  v8 = ~s[14]
  S.add(Not( ~s[14] > 1 ))
  v8 = s[0] >> 5
  S.add(Not( (s[0] >> 5) > 49 ))
  v8 = ~s[19]
  S.add(Not( ~s[19] > 1 ))
  v8 = s[0] ^ s[1]
  S.add(Not( (s[0] ^ s[1]) > 66 ))
  v8 = s[0] & s[1]
  S.add(Not( (s[0] & s[1]) > 81 ))
  v8 = s[18] & s[1]
  S.add(Not( (s[18] & s[1]) > 41 ))
  v8 = s[0] ^ s[1]
  S.add(Not( (s[0] ^ s[1]) > 82 ))
  v8 = s[17] & s[3]
  S.add(Not( (s[17] & s[3]) > 84 ))
  v8 = s[0] & s[1]
  S.add(Not( (s[0] & s[1]) <= 34 ))
  v8 = s[18] & s[1]
  S.add(Not( (s[18] & s[1]) > 66 ))
  v8 = s[0] & s[1]
  S.add(Not( (s[0] & s[1]) > 90 ))
  v8 = s[18] & s[4]
  S.add(Not( (s[18] & s[4]) > 73 ))
  v8 = s[18] & s[1]
  S.add(Not( (s[18] & s[1]) <= 12 ))
  v8 = s[0] ^ s[1]
  S.add(Not( (s[0] ^ s[1]) <= 9 ))
  v8 = s[2] ^ s[8]
  S.add(Not( (s[2] ^ s[8]) <= 42 ))
  v8 = s[13] ^ s[0]
  S.add(Not( (s[13] ^ s[0]) > 44 ))
  v8 = s[0] & s[1]
  S.add(Not( (s[0] & s[1]) <= 14 ))
  v8 = s[0] & s[1]
  S.add(Not( (s[0] & s[1]) <= 16 ))
  v8 = s[18] & s[1]
  S.add(Not( (s[18] & s[1]) > 74 ))
  v8 = s[0] ^ s[6]
  S.add(Not( (s[0] ^ s[6]) > 102 ))
  v8 = 4 * s[2]
  S.add(Not( (4 * s[2]) <= 16 ))
  v8 = s[0] | s[1]
  S.add(Not( (s[0] | s[1]) <= 87 ))
  v8 = s[1] ^ s[11]
  S.add(Not( (s[1] ^ s[11]) > 29 ))
  v8 = s[18] & s[1]
  S.add(Not( (s[18] & s[1]) > 51 ))
  v8 = s[0] ^ s[6]
  S.add(Not( (s[0] ^ s[6]) > 74 ))
  v8 = 4 * s[2]
  S.add(Not( (4 * s[2]) <= 103 ))
  v8 = s[0] | s[1]
  S.add(Not( (s[0] | s[1]) <= 56 ))
  v8 = s[4] ^ s[6]
  S.add(Not( (s[4] ^ s[6]) <= 11 ))
  v8 = s[0] & s[1]
  S.add(Not( (s[0] & s[1]) <= 16 ))
  v8 = s[18] & s[1]
  S.add(Not( (s[18] & s[1]) <= 22 ))
  v8 = s[16] & s[15] | s[18]
  S.add(Not( v8 > 122 ))
  v8 = s[0] ^ s[6]
  S.add(Not( (s[0] ^ s[6]) > 74 ))
  v8 = 4 * s[2]
  S.add(Not( (4 * s[2]) <= 16 ))
  v8 = s[16] ^ s[18]
  S.add(Not( (s[16] ^ s[18]) > 67 ))
  v8 = s[0] & s[1]
  S.add(Not( (s[0] & s[1]) > 102 ))
  v8 = s[0] ^ s[6]
  S.add(Not( (s[0] ^ s[6]) > 74 ))
  v8 = s[9] | s[13]
  S.add(Not( (s[9] | s[13]) <= 27 ))
  v8 = 4 * s[2]
  S.add(Not( (4 * s[2]) <= 58 ))
  v8 = 4 * s[2]
  S.add(Not( (4 * s[2]) <= 77 ))
  v8 = s[0] | s[1]
  S.add(Not( (s[0] | s[1]) <= 3 ))
  v8 = s[0] & s[1]
  S.add(Not( (s[0] & s[1]) <= 13 ))
  v8 = s[0] ^ s[6]
  S.add(Not( (s[0] ^ s[6]) > 47 ))
  v8 = s[7] & s[4]
  S.add(Not( (s[7] & s[4]) <= 39 ))
  v8 = s[16] | s[7]
  S.add(Not( (s[16] | s[7]) == 127 ))
  v8 = s[0] | s[1]
  S.add(Not( (s[0] | s[1]) <= 66 ))
  v8 = s[0] & s[1]
  S.add(Not( (s[0] & s[1]) <= 47 ))
  v8 = s[18] & s[1]
  S.add(Not( (s[18] & s[1]) > 63 ))
  v8 = s[13] & s[3]
  S.add(Not( (s[13] & s[3]) > 122 ))
  v8 = 4 * s[2]
  S.add(Not( (4 * s[2]) <= 65 ))
  v8 = s[0] & s[1]
  S.add(Not( (s[0] & s[1]) > 120 ))
  v8 = 4 * s[2]
  S.add(Not( (4 * s[2]) <= 83 ))
  v8 = s[0] | s[1]
  S.add(Not( (s[0] | s[1]) <= 99 ))
  v8 = ~s[14]
  S.add(Not( ~s[14] > 1 ))
  v8 = s[0] >> 5
  S.add(Not( (s[0] >> 5) > 42 ))
  v8 = ~s[19]
  S.add(Not( ~s[19] > 1 ))
  v8 = s[0] ^ s[6]
  S.add(Not( (s[0] ^ s[6]) > 110 ))
  v8 = 4 * s[2]
  S.add(Not( (4 * s[2]) <= 92 ))
  v8 = s[0] | s[1]
  S.add(Not( (s[0] | s[1]) <= 59 ))
  v8 = s[8] | s[0]
  S.add(Not( (s[8] | s[0]) <= 1 ))
  v8 = ~s[14]
  S.add(Not( ~s[14] > 1 ))
  v8 = ~s[19]
  S.add(Not( ~s[19] > 1 ))
  v8 = ~s[14]
  S.add(Not( ~s[14] > 17 ))
  v8 = ~s[19]
  S.add(Not( ~s[19] > 1 ))
  v8 = s[11] | s[9]
  S.add(Not( (s[11] | s[9]) <= 78 ))
  v8 = s[12] ^ s[15]
  S.add(Not( (s[12] ^ s[15]) > 47 ))
  v8 = s[13] & s[1]
  S.add(Not( (s[13] & s[1]) <= 90 ))
  v8 = 16 * s[7]
  S.add(Not( (16 * s[7]) <= 78 ))
  v8 = s[13] ^ s[5]
  S.add(Not( (s[13] ^ s[5]) <= 30 ))
  v8 = ~s[6]
  S.add(Not( ~s[6] > 1 ))
  v8 = ~s[14]
  S.add(Not( ~s[14] > 1 ))
  v8 = ~s[19]
  S.add(Not( ~s[19] > 1 ))
  v8 = s[11] | s[9]
  S.add(Not( (s[11] | s[9]) <= 17 ))
  v8 = s[12] ^ s[15]
  S.add(Not( (s[12] ^ s[15]) > 86 ))
  v8 = s[12] & s[4]
  S.add(Not( (s[12] & s[4]) > 120 ))
  v8 = 16 * s[7]
  S.add(Not( (16 * s[7]) <= 46 ))
  v8 = s[13] ^ s[5]
  S.add(Not( (s[13] ^ s[5]) > 63 ))
  v8 = s[12] ^ s[14]
  S.add(Not( (s[12] ^ s[14]) <= 5 ))
  v8 = ~s[6]
  S.add(Not( ~s[6] > 17 ))
  v8 = ~s[14]
  S.add(Not( ~s[14] > 113 ))
  v8 = ~s[19]
  S.add(Not( ~s[19] > 1 ))
  v8 = s[11] | s[9]
  S.add(Not( (s[11] | s[9]) <= 73 ))
  v8 = s[12] ^ s[15]
  S.add(Not( (s[12] ^ s[15]) > 60 ))
  v8 = s[13] & s[1]
  S.add(Not( (s[13] & s[1]) > 119 ))
  v8 = ~s[6]
  S.add(Not( ~s[6] > 21 ))
  v8 = ~s[19]
  S.add(Not( ~s[19] > 107 ))
  v8 = s[12] ^ s[15]
  S.add(Not( (s[12] ^ s[15]) > 44 ))
  v8 = s[13] & s[1]
  S.add(Not( (s[13] & s[1]) <= 57 ))
  v8 = s[13] ^ s[5]
  S.add(Not( (s[13] ^ s[5]) > 59 ))
  v8 = ~s[6]
  S.add(Not( ~s[6] > 1 ))
  v8 = ~s[14]
  S.add(Not( ~s[14] > 1 ))
  v8 = s[0] >> 5
  S.add(Not( (s[0] >> 5) > 58 ))
  v8 = ~s[9]
  S.add(Not( ~s[9] > 1 ))
  v8 = s[11] | s[9]
  S.add(Not( (s[11] | s[9]) <= 101 ))
  v8 = s[13] & s[1]
  S.add(Not( (s[13] & s[1]) <= 99 ))
  v8 = 16 * s[7]
  S.add(Not( (16 * s[7]) <= 78 ))
  v8 = s[13] ^ s[4]
  S.add(Not( (s[13] ^ s[4]) > 16 ))
  v8 = ~s[16]
  S.add(Not( ~s[16] > 10 ))
  v8 = ~s[4]
  S.add(Not( ~s[4] > 1 ))
  v8 = s[0] >> 5
  S.add(Not( (s[0] >> 5) > 3 ))
  v8 = ~s[19]
  S.add(Not( ~s[19] > 1 ))
  v8 = s[11] | s[9]
  S.add(Not( (s[11] | s[9]) > 118 ))
  v8 = s[12] ^ s[15]
  S.add(Not( (s[12] ^ s[15]) <= 1 ))
  v8 = 16 * s[7]
  S.add(Not( (16 * s[7]) <= 0 ))
  v8 = s[13] ^ s[5]
  S.add(Not( (s[13] ^ s[5]) > 101 ))
  v8 = s[0] >> 5
  S.add(Not( (s[0] >> 5) > 18 ))
  v8 = ~s[19]
  S.add(Not( ~s[19] > 1 ))
  v8 = s[11] | s[9]
  S.add(Not( (s[11] | s[9]) <= 0 ))
  v8 = s[12] ^ s[15]
  S.add(Not( (s[12] ^ s[15]) > 67 ))
  v8 = s[13] & s[1]
  S.add(Not( (s[13] & s[1]) > 103 ))
  v8 = 16 * s[4]
  S.add(Not( (16 * s[4]) > 1 ))
  v8 = s[13] ^ s[5]
  S.add(Not( (s[13] ^ s[5]) <= 38 ))
  v8 = ~s[6]
  S.add(Not( ~s[6] > 1 ))
  v8 = s[4] & s[12]
  S.add(Not( (s[4] & s[12]) <= 94 ))
  v8 = s[16] >> 1
  S.add(Not( (s[16] >> 1) > 63 ))
  v8 = ~s[6]
  S.add(Not( ~s[6] > 1 ))
  v8 = s[16] >> 1
  S.add(Not( (s[16] >> 1) <= 47 ))
  v8 = s[0] >> 5
  S.add(Not( (s[0] >> 5) <= 0 ))
  v8 = ~s[19]
  S.add(Not( ~s[19] > 1 ))
  v8 = s[11] | s[9]
  S.add(Not( (s[11] | s[9]) > 118 ))
  v8 = s[12] ^ s[15]
  S.add(Not( (s[12] ^ s[15]) > 58 ))
  v8 = s[13] & s[1]
  S.add(Not( (s[13] & s[1]) <= 91 ))
  v8 = 16 * s[7]
  S.add(Not( (16 * s[7]) <= 72 ))
  v8 = s[13] ^ s[5]
  S.add(Not( (s[13] ^ s[5]) > 63 ))
  v8 = ~s[6]
  S.add(Not( ~s[6] > 1 ))
  v8 = s[4] & s[12]
  S.add(Not( (s[4] & s[12]) <= 94 ))
  v8 = s[16] >> 1
  S.add(Not( (s[16] >> 1) <= 57 ))
  v8 = ~s[6]
  S.add(Not( ~s[6] > 1 ))
  v8 = s[4] & s[12]
  S.add(Not( (s[4] & s[12]) > 99 ))
  v8 = s[16] >> 1
  S.add(Not( (s[16] >> 1) > 63 ))
  v8 = s[0] >> 5
  S.add(Not( (s[0] >> 5) > 81 ))
  v8 = ~s[19]
  S.add(Not( ~s[19] > 1 ))
  v8 = s[11] | s[9]
  S.add(Not( (s[11] | s[9]) > 118 ))
  v8 = s[8] ^ s[15]
  S.add(Not( (s[8] ^ s[15]) > 1 ))
  v8 = s[7] & s[1]
  S.add(Not( (s[7] & s[1]) <= 72 ))
  v8 = 16 * s[17]
  S.add(Not( (16 * s[17]) > 1 ))
  v8 = s[3] ^ s[5]
  S.add(Not( (s[3] ^ s[5]) > 110 ))
  v8 = ~s[6]
  S.add(Not( ~s[6] > 1 ))
  v8 = s[4] & s[12]
  S.add(Not( (s[4] & s[12]) <= 68 ))
  v8 = s[16] >> 1
  S.add(Not( (s[16] >> 1) > 91 ))
  v8 = ~s[6]
  S.add(Not( ~s[6] > 1 ))
  v8 = s[4] & s[12]
  S.add(Not( (s[4] & s[12]) > 99 ))
  v8 = s[16] >> 1
  S.add(Not( (s[16] >> 1) <= 40 ))
  v8 = s[16] >> 1
  S.add(Not( (s[16] >> 1) <= 31 ))
  v8 = ~s[14]
  S.add(Not( ~s[14] > 1 ))
  v8 = s[0] >> 5
  S.add(Not( (s[0] >> 5) > 96 ))
  v8 = ~s[19]
  S.add(Not( ~s[19] > 1 ))
  v8 = s[3] ^ s[1]
  S.add(Not( (s[3] ^ s[1]) > 42 ))
  v8 = s[4] & s[1]
  S.add(Not( (s[4] & s[1]) > 118 ))
  v8 = s[16] >> 1
  S.add(Not( (s[16] >> 1) > 94 ))
  v8 = ~s[14]
  S.add(Not( ~s[14] > 1 ))
  v8 = ~s[19]
  S.add(Not( ~s[19] > 1 ))
  v8 = s[0] ^ s[1]
  S.add(Not( (s[0] ^ s[1]) > 64 ))
  v8 = s[0] & s[1]
  S.add(Not( (s[0] & s[1]) > 110 ))
  v8 = 4 * s[2]
  S.add(Not( (4 * s[2]) <= 104 ))
  v8 = s[0] | s[1]
  S.add(Not( (s[0] | s[1]) > 112 ))
  v8 = s[0] & s[1]
  S.add(Not( (s[0] & s[1]) <= 62 ))
  v8 = s[18] & s[1]
  S.add(Not( (s[18] & s[1]) > 48 ))
  v8 = s[0] ^ s[6]
  S.add(Not( (s[0] ^ s[6]) > 58 ))
  v8 = 4 * s[2]
  S.add(Not( (4 * s[2]) <= 104 ))
  v8 = s[8] | s[1]
  S.add(Not( (s[8] | s[1]) <= 50 ))
  v8 = s[5] & s[1]
  S.add(Not( (s[5] & s[1]) <= 38 ))
  v8 = s[18] & s[1]
  S.add(Not( (s[18] & s[1]) > 85 ))
  v8 = s[0] ^ s[6]
  S.add(Not( (s[0] ^ s[6]) <= 18 ))
  v8 = 4 * s[2]
  S.add(Not( (4 * s[2]) <= 97 ))
  v8 = s[0] | s[1]
  S.add(Not( (s[0] | s[1]) <= 94 ))
  v8 = s[18] & s[1]
  S.add(Not( (s[18] & s[1]) <= 26 ))
  v8 = s[0] ^ s[6]
  S.add(Not( (s[0] ^ s[6]) > 67 ))
  v8 = 4 * s[2]
  S.add(Not( (4 * s[2]) <= 103 ))
  v8 = s[18] & s[1]
  S.add(Not( (s[18] & s[1]) > 50 ))
  v8 = s[0] ^ s[6]
  S.add(Not( (s[0] ^ s[6]) <= 22 ))
  v8 = 4 * s[2]
  S.add(Not( (4 * s[2]) <= 103 ))
  v8 = s[0] | s[1]
  S.add(Not( (s[0] | s[1]) <= 38 ))
  v8 = s[0] & s[1]
  S.add(Not( (s[0] & s[1]) <= 52 ))
  v8 = s[18] & s[1]
  S.add(Not( (s[18] & s[1]) <= 17 ))
  v8 = 4 * s[9]
  S.add(Not( (4 * s[9]) > 1 ))
  v8 = s[0] | s[1]
  S.add(Not( (s[0] | s[1]) <= 92 ))
  v8 = s[0] & s[1]
  S.add(Not( (s[0] & s[1]) <= 55 ))
  v8 = s[8] ^ s[6]
  S.add(Not( (s[8] ^ s[6]) > 81 ))
  v8 = 4 * s[12]
  S.add(Not( (4 * s[12]) > 1 ))
  v8 = s[0] | s[1]
  S.add(Not( (s[0] | s[1]) <= 94 ))
  v8 = ~s[12]
  S.add(Not( ~s[12] > 1 ))
  v8 = ~s[1]
  S.add(Not( ~s[1] > 1 ))
  v8 = s[0] ^ s[6]
  S.add(Not( (s[0] ^ s[6]) > 101 ))
  v8 = 4 * s[4]
  S.add(Not( (4 * s[4]) > 1 ))
  v8 = s[0] | s[1]
  S.add(Not( (s[0] | s[1]) <= 44 ))
  v8 = ~s[14]
  S.add(Not( ~s[14] > 1 ))
  v8 = ~s[14]
  S.add(Not( ~s[14] > 1 ))
  v8 = ~s[19]
  S.add(Not( ~s[19] > 120 ))
  
  print S.check()
  m = S.model()
  print repr(''.join(chr(m[c].as_long()) for c in s))

if __name__ == "__main__":
  main()
