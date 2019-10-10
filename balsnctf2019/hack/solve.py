from z3 import *

flag = [Int('f%d' % i) for i in range(26)]
s = Solver()

v=-314
v+=flag[5]
v+=flag[6]
v+=flag[13]
v+=flag[15]
s.add(v == 82)

v=-243
v+=flag[22]
v+=flag[24]
v+=flag[22]
s.add(v == 21)

v=-28
v+=flag[1]
v+=flag[11]
v+=flag[17]
v+=flag[3]
s.add(v == 314)

v=257
v+=flag[20]
v+=flag[7]
v+=flag[10]
v+=flag[24]
s.add(v == 585)

v=40
v+=flag[4]
v+=flag[25]
v+=flag[21]
s.add(v == 374)

v=-151
v+=flag[9]
v+=flag[9]
v+=flag[16]
v+=flag[21]
s.add(v == 239)

v=-447
v+=flag[1]
v+=flag[21]
v+=flag[8]
v+=flag[8]
s.add(v == -23)

v=-14
v+=flag[10]
v+=flag[11]
v+=flag[11]
s.add(v == 149)

v=248
v+=flag[16]
v+=flag[19]
v+=flag[21]
v+=flag[19]
s.add(v == 656)

v=-346
v+=flag[12]
v+=flag[22]
v+=flag[0]
v+=flag[4]
s.add(v == -18)

v=-403
v+=flag[24]
v+=flag[9]
v+=flag[1]
s.add(v == -97)

v=69
v+=flag[1]
v+=flag[5]
v+=flag[21]
v+=flag[12]
s.add(v == 465)

v=8
v+=flag[0]
v+=flag[12]
v+=flag[7]
s.add(v == 246)

v=-197
v+=flag[15]
v+=flag[18]
v+=flag[15]
s.add(v == 50)

v=-139
v+=flag[13]
v+=flag[25]
v+=flag[0]
s.add(v == 164)

v=442
v+=flag[23]
v+=flag[1]
v+=flag[20]
s.add(v == 692)

v=-207
v+=flag[3]
v+=flag[23]
v+=flag[8]
s.add(v == 123)

v=477
v+=flag[18]
v+=flag[3]
v+=flag[19]
v+=flag[24]
s.add(v == 905)

v=120
v+=flag[20]
v+=flag[15]
v+=flag[15]
v+=flag[22]
s.add(v == 399)

v=-368
v+=flag[14]
v+=flag[18]
v+=flag[19]
v+=flag[14]
s.add(v == -71)

v=436
v+=flag[22]
v+=flag[1]
v+=flag[5]
v+=flag[9]
s.add(v == 826)

v=-330
v+=flag[12]
v+=flag[17]
v+=flag[3]
v+=flag[18]
s.add(v == 39)

v=362
v+=flag[11]
v+=flag[12]
v+=flag[3]
s.add(v == 602)

v=-456
v+=flag[15]
v+=flag[14]
v+=flag[1]
s.add(v == -234)

v=458
v+=flag[20]
v+=flag[0]
v+=flag[14]
v+=flag[11]
s.add(v == 673)

v=307
v+=flag[5]
v+=flag[17]
v+=flag[22]
s.add(v == 587)

v=-91
v+=flag[18]
v+=flag[9]
v+=flag[12]
s.add(v == 176)

v=-42
v+=flag[7]
v+=flag[24]
v+=flag[25]
s.add(v == 292)

v=-39
v+=flag[16]
v+=flag[20]
v+=flag[7]
s.add(v == 209)

v=243
v+=flag[15]
v+=flag[23]
v+=flag[17]
v+=flag[17]
s.add(v == 584)

v=-437
v+=flag[8]
v+=flag[4]
v+=flag[24]
v+=flag[2]
s.add(v == 9)

v=284
v+=flag[25]
v+=flag[4]
v+=flag[12]
v+=flag[8]
s.add(v == 710)

v=154
v+=flag[8]
v+=flag[11]
v+=flag[4]
v+=flag[24]
s.add(v == 540)

v=369
v+=flag[23]
v+=flag[21]
v+=flag[2]
v+=flag[21]
s.add(v == 776)

v=221
v+=flag[13]
v+=flag[0]
v+=flag[1]
v+=flag[12]
s.add(v == 573)

v=11
v+=flag[24]
v+=flag[10]
v+=flag[8]
v+=flag[0]
s.add(v == 372)

v=339
v+=flag[18]
v+=flag[3]
v+=flag[18]
s.add(v == 644)

v=434
v+=flag[10]
v+=flag[8]
v+=flag[23]
s.add(v == 716)

v=-331
v+=flag[21]
v+=flag[6]
v+=flag[16]
s.add(v == -46)

v=-84
v+=flag[0]
v+=flag[6]
v+=flag[13]
s.add(v == 179)

v=2
v+=flag[21]
v+=flag[22]
v+=flag[6]
v+=flag[7]
s.add(v == 356)

v=-291
v+=flag[19]
v+=flag[5]
v+=flag[9]
v+=flag[18]
s.add(v == 126)

v=353
v+=flag[9]
v+=flag[14]
v+=flag[9]
s.add(v == 592)

v=-393
v+=flag[11]
v+=flag[23]
v+=flag[3]
v+=flag[9]
s.add(v == -34)

v=-93
v+=flag[7]
v+=flag[16]
v+=flag[18]
v+=flag[6]
s.add(v == 283)

v=162
v+=flag[13]
v+=flag[24]
v+=flag[25]
v+=flag[8]
s.add(v == 627)

v=182
v+=flag[6]
v+=flag[14]
v+=flag[4]
s.add(v == 426)

v=-99
v+=flag[14]
v+=flag[13]
v+=flag[10]
s.add(v == 129)

v=148
v+=flag[14]
v+=flag[3]
v+=flag[23]
v+=flag[6]
s.add(v == 498)

v=-249
v+=flag[25]
v+=flag[22]
v+=flag[22]
v+=flag[2]
s.add(v == 134)

v=60
v+=flag[16]
v+=flag[19]
v+=flag[14]
v+=flag[14]
s.add(v == 363)

v=346
v+=flag[22]
v+=flag[13]
v+=flag[14]
s.add(v == 582)

v=144
v+=flag[3]
v+=flag[16]
v+=flag[16]
v+=flag[18]
s.add(v == 556)

v=-79
v+=flag[4]
v+=flag[15]
v+=flag[9]
s.add(v == 202)

v=-60
v+=flag[17]
v+=flag[15]
v+=flag[11]
s.add(v == 146)

v=-229
v+=flag[21]
v+=flag[8]
v+=flag[10]
s.add(v == 51)

v=472
v+=flag[5]
v+=flag[16]
v+=flag[13]
s.add(v == 808)

v=325
v+=flag[19]
v+=flag[1]
v+=flag[2]
s.add(v == 634)

v=393
v+=flag[19]
v+=flag[2]
v+=flag[20]
v+=flag[0]
s.add(v == 723)

v=158
v+=flag[11]
v+=flag[20]
v+=flag[2]
v+=flag[6]
s.add(v == 451)

v=-389
v+=flag[6]
v+=flag[25]
v+=flag[7]
v+=flag[13]
s.add(v == 28)

v=-289
v+=flag[7]
v+=flag[8]
v+=flag[24]
s.add(v == 34)

v=-290
v+=flag[2]
v+=flag[10]
v+=flag[5]
v+=flag[12]
s.add(v == 85)

v=141
v+=flag[23]
v+=flag[2]
v+=flag[12]
s.add(v == 427)

v=406
v+=flag[6]
v+=flag[0]
v+=flag[4]
s.add(v == 667)

v=-458
v+=flag[8]
v+=flag[20]
v+=flag[19]
s.add(v == -188)

v=244
v+=flag[9]
v+=flag[4]
v+=flag[6]
s.add(v == 534)

v=-228
v+=flag[3]
v+=flag[19]
v+=flag[18]
s.add(v == 86)

v=209
v+=flag[24]
v+=flag[18]
v+=flag[6]
v+=flag[5]
s.add(v == 626)

v=294
v+=flag[4]
v+=flag[21]
v+=flag[25]
s.add(v == 628)

v=-150
v+=flag[17]
v+=flag[10]
v+=flag[15]
v+=flag[21]
s.add(v == 174)

v=-31
v+=flag[2]
v+=flag[13]
v+=flag[5]
v+=flag[2]
s.add(v == 420)

v=-101
v+=flag[10]
v+=flag[17]
v+=flag[23]
v+=flag[5]
s.add(v == 272)

v=-194
v+=flag[0]
v+=flag[7]
v+=flag[0]
s.add(v == 33)

v=-319
v+=flag[12]
v+=flag[7]
v+=flag[17]
s.add(v == -65)

v=7
v+=flag[25]
v+=flag[2]
v+=flag[20]
v+=flag[17]
s.add(v == 374)

v=-341
v+=flag[17]
v+=flag[12]
v+=flag[11]
v+=flag[11]
s.add(v == -86)

v=-383
v+=flag[2]
v+=flag[5]
v+=flag[24]
s.add(v == -38)

res = s.check()
print(res)
m = s.model()
print(bytearray([m[i].as_long() for i in flag]))
# Balsn{U_r_C0Mp1LeR_h4cKer}
