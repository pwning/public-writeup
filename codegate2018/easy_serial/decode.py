#! /usr/bin/env python3

import re

case1 = """&& (== $fEqInt (ord (!! s1b7_info (I# 0))) (I# 70)) (&& (== $fEqInt (ord (!! s1b7_info (I# 1))) (I# 108)) (&& (== $fEqInt (ord (!! s1b7_info (I# 2))) (I# 97)) (&& (== $fEqInt (ord (!! s1b7_info (I# 3))) (I# 103)) (&& (== $fEqInt (ord (!! s1b7_info (I# 4))) (I# 123)) (&& (== $fEqInt (ord (!! s1b7_info (I# 5))) (I# 83)) (&& (== $fEqInt (ord (!! s1b7_info (I# 6))) (I# 48)) (&& (== $fEqInt (ord (!! s1b7_info (I# 7))) (I# 109)) (&& (== $fEqInt (ord (!! s1b7_info (I# 8))) (I# 101)) (&& (== $fEqInt (ord (!! s1b7_info (I# 9))) (I# 48)) (&& (== $fEqInt (ord (!! s1b7_info (I# 10))) (I# 102)) (&& (== $fEqInt (ord (!! s1b7_info (I# 11))) (I# 85)) (== $fEqInt (ord (!! s1b7_info (I# 12))) (I# 53)))))))))))))"""

case2 = """== ($fEq[] $fEqChar) (reverse s1b9_info) (: (C# 103) (: (C# 110) (: (C# 105) (: (C# 107) (: (C# 48) (: (C# 48) (: (C# 76) (: (C# 51) (: (C# 114) (: (C# 52) []))))))))))"""

case3 = """&& (== $fEqChar (!! s1bb_info (I# 0)) (!! s1b3_info (I# 0))) (&& (== $fEqChar (!! s1bb_info (I# 1)) (!! s1b4_info (I# 19))) (&& (== $fEqChar (!! s1bb_info (I# 2)) (!! s1b3_info (I# 19))) (&& (== $fEqChar (!! s1bb_info (I# 3)) (!! s1b4_info (I# 7))) (&& (== $fEqChar (!! s1bb_info (I# 4)) (!! s1b2_info (I# 2))) (&& (== $fEqChar (!! s1bb_info (I# 5)) (!! s1b3_info (I# 18))) (&& (== $fEqChar (!! s1bb_info (I# 6)) (!! s1b4_info (I# 19))) (&& (== $fEqChar (!! s1bb_info (I# 7)) (!! s1b2_info (I# 3))) (&& (== $fEqChar (!! s1bb_info (I# 8)) (!! s1b4_info (I# 17))) (== $fEqChar (!! s1bb_info (I# 9)) (!! s1b4_info (I# 18)))))))))))"""

infos = {
    's1b2_info' : "1234567890",
    's1b3_info' : "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    's1b4_info' : "abcdefghijklmnopqrstuvwxyz",
}

# first case statement (first third of the flag)
matches1 = re.findall(r"\(ord \(!! s1b7_info \(I# \d+\)\)\) \(I# (\d+)\)", case1)
flag1 = ''.join(chr(int(m)) for m in matches1)

# second case statement (second third of the flag)
matches2 = re.findall(r"\(C# (\d+)\)", case2)
flag2 = ''.join(reversed([chr(int(m)) for m in matches2]))

# third case statement (last third of the flag)
matches3 = re.findall(r"\(!! s1bb_info \(I# \d+\)\) \(!! (s1b._info) \(I# (\d+)\)\)", case3)
flag3 = ''.join(infos[which_info][int(idx)] for which_info, idx in matches3)

# add the last "}" and show the flag
print("#".join([flag1, flag2, flag3]) + "}") # Flag{S0me0fU5#4r3L00king#AtTh3St4rs}

