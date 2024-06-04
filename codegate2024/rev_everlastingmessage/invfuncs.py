import pickle
from itertools import combinations
from tqdm import tqdm

def f1(param_1):
    uvar2 = (param_1 >> 8)
    uvar1 = (param_1 >> 0x10)
    return (((param_1 >> 0x13 ^ param_1 >> 5 ^ param_1 >> 7 ^ param_1 >> 0xf ^ param_1 >> 0x12) & 1) <<
             0x27 | (((param_1 >> 0x13) ^
                            (param_1 >> 2) ^ (param_1 >> 3) ^ (param_1 >> 4) ^
                            (param_1 >> 6) ^ (param_1 >> 7) ^ uvar2 ^ (param_1 >> 0xb)
                            ^ (param_1 >> 0xc) ^ (param_1 >> 0xd) ^ (param_1 >> 0xf) ^
                            uvar1 ^ (param_1 >> 0x11) ^ (param_1 >> 0x12)) & 1 |
                            ((param_1 >> 0x11) ^
                            (param_1 >> 2) ^ param_1 ^ (param_1 >> 4) ^
                            (param_1 >> 5) ^ (param_1 >> 7) ^ uvar2 ^ (param_1 >> 10)
                            ^ (param_1 >> 0xb) ^ (param_1 >> 0xc) ^ (param_1 >> 0xe) ^
                            (param_1 >> 0xf) ^ uvar1) * 2 & 2 |
                            ((param_1 >> 0xe ^
                                   param_1 >> 1 ^ param_1 >> 3 ^ param_1 >> 4 ^ param_1 >> 7 ^
                                   param_1 >> 8 ^ param_1 >> 10) << 2) & 4 |
                            ((param_1 >> 0x13 ^
                                   param_1 >> 1 ^ param_1 >> 3 ^ param_1 >> 5 ^ param_1 >> 6 ^
                                   param_1 >> 7 ^ param_1 >> 8 ^ param_1 >> 0xc ^ param_1 >> 0xd ^
                                   param_1 >> 0xe ^ param_1 >> 0xf ^ param_1 >> 0x12) << 3) & 8 |
                            ((param_1 >> 0x13 ^
                                   param_1 >> 4 ^ param_1 ^ param_1 >> 5 ^ param_1 >> 6 ^ param_1 >> 8 ^
                                   param_1 >> 10 ^ param_1 >> 0xd ^ param_1 >> 0x12) << 4) & 0x10 |
                            ((param_1 >> 0x12 ^
                                   param_1 >> 1 ^ param_1 ^ param_1 >> 2 ^ param_1 >> 3 ^ param_1 >> 6 ^
                                   param_1 >> 8 ^ param_1 >> 9 ^ param_1 >> 10 ^ param_1 >> 0xb ^
                                   param_1 >> 0xc ^ param_1 >> 0xd ^ param_1 >> 0x10 ^ param_1 >> 0x11)
                                  << 5) & 0x20 |
                           ((param_1 >> 0x12 ^
                                  param_1 >> 1 ^ param_1 >> 3 ^ param_1 >> 4 ^ param_1 >> 6 ^
                                  param_1 >> 7 ^ param_1 >> 8 ^ param_1 >> 9 ^ param_1 >> 0xb ^
                                  param_1 >> 0xe ^ param_1 >> 0xf ^ param_1 >> 0x11) << 6) & 0x40) |
                    ((param_1 >> 0x13 ^
                     param_1 >> 1 ^ param_1 ^ param_1 >> 2 ^ param_1 >> 4 ^ param_1 >> 5 ^ param_1 >> 8
                     ^ param_1 >> 9 ^ param_1 >> 10 ^ param_1 >> 0xc ^ param_1 >> 0xf ^ param_1 >> 0x10
                     ^ param_1 >> 0x11 ^ param_1 >> 0x12) & 1) << 7 |
                    (((param_1 >> 0x11 ^
                                   param_1 >> 1 ^ param_1 >> 2 ^ param_1 >> 5 ^ param_1 >> 8 ^
                                   param_1 >> 10 ^ param_1 >> 0xc ^ param_1 >> 0xd ^ param_1 >> 0xe ^
                                   param_1 >> 0xf) << 8) & 0x100) |
                    (((param_1 >> 0x13 ^
                                   param_1 >> 1 ^ param_1 ^ param_1 >> 2 ^ param_1 >> 3 ^ param_1 >> 4 ^
                                   param_1 >> 5 ^ param_1 >> 6 ^ param_1 >> 8 ^ param_1 >> 9 ^
                                   param_1 >> 10 ^ param_1 >> 0xb ^ param_1 >> 0xe ^ param_1 >> 0x11 ^
                                   param_1 >> 0x12) << 9) & 0x200) |
                    (((param_1 >> 0x11 ^
                                   param_1 >> 1 ^ param_1 >> 5 ^ param_1 >> 6 ^ param_1 >> 7 ^
                                   param_1 >> 8 ^ param_1 >> 0xb ^ param_1 >> 0xd ^ param_1 >> 0xf) <<
                                  10) & 0x400) |
                    (((param_1 >> 0x13 ^
                                   param_1 >> 1 ^ param_1 ^ param_1 >> 2 ^ param_1 >> 3 ^ param_1 >> 4 ^
                                   param_1 >> 5 ^ param_1 >> 6 ^ param_1 >> 7 ^ param_1 >> 8 ^
                                   param_1 >> 9 ^ param_1 >> 0xc ^ param_1 >> 0xe ^ param_1 >> 0xf ^
                                   param_1 >> 0x10) << 0xb) & 0x800) |
                    (((param_1 >> 0x11 ^
                                   param_1 >> 2 ^ param_1 >> 3 ^ param_1 >> 4 ^ param_1 >> 5 ^
                                   param_1 >> 8 ^ param_1 >> 9 ^ param_1 >> 0xc ^ param_1 >> 0xd) << 0xc
                                  ) & 0x1000) |
                    (((param_1 >> 0x13 ^
                                   param_1 >> 1 ^ param_1 >> 2 ^ param_1 >> 3 ^ param_1 >> 5 ^
                                   param_1 >> 7 ^ param_1 >> 8 ^ param_1 >> 10 ^ param_1 >> 0xb ^
                                   param_1 >> 0xc ^ param_1 >> 0xd ^ param_1 >> 0xe ^ param_1 >> 0xf ^
                                   param_1 >> 0x10 ^ param_1 >> 0x12) << 0xd) & 0x2000) |
                    (((param_1 >> 0x10 ^
                                   param_1 >> 1 ^ param_1 >> 2 ^ param_1 >> 3 ^ param_1 >> 4 ^
                                   param_1 >> 6 ^ param_1 >> 10 ^ param_1 >> 0xb ^ param_1 >> 0xf) <<
                                  0xe) & 0x4000) |
                    ((param_1 >> 0x12 ^
                     param_1 >> 1 ^ param_1 >> 2 ^ param_1 >> 3 ^ param_1 >> 5 ^ param_1 >> 6 ^
                     param_1 >> 9 ^ param_1 >> 10 ^ param_1 >> 0xc ^ param_1 >> 0xe ^ param_1 >> 0x10 ^
                     param_1 >> 0x11) & 1) << 0xf |
                    (((param_1 >> 0xf ^
                                   param_1 >> 3 ^ param_1 ^ param_1 >> 5 ^ param_1 >> 7 ^ param_1 >> 8 ^
                                   param_1 >> 10 ^ param_1 >> 0xd) << 0x10) & 0x10000) |
                    (((param_1 >> 0x10 ^
                                   param_1 >> 1 ^ param_1 >> 2 ^ param_1 >> 3 ^ param_1 >> 4 ^
                                   param_1 >> 6 ^ param_1 >> 7 ^ param_1 >> 8 ^ param_1 >> 9 ^
                                   param_1 >> 10 ^ param_1 >> 0xd ^ param_1 >> 0xe) << 0x11) & 0x20000)
                    | (((param_1 >> 0x13 ^
                                     param_1 >> 2 ^ param_1 ^ param_1 >> 6 ^ param_1 >> 7 ^ param_1 >> 8
                                     ^ param_1 >> 10 ^ param_1 >> 0xb ^ param_1 >> 0xe ^ param_1 >> 0x11
                                     ) << 0x12) & 0x40000) |
                    (((param_1 >> 0x13 ^
                                   param_1 >> 3 ^ param_1 ^ param_1 >> 9 ^ param_1 >> 0xd ^
                                   param_1 >> 0xf) << 0x13) & 0x80000) |
                    (((param_1 >> 0x12 ^
                                   param_1 >> 1 ^ param_1 ^ param_1 >> 2 ^ param_1 >> 3 ^ param_1 >> 4 ^
                                   param_1 >> 0xb ^ param_1 >> 0xd ^ param_1 >> 0xe ^ param_1 >> 0xf ^
                                   param_1 >> 0x10) << 0x14) & 0x100000) |
                    (((param_1 >> 0x13 ^
                                   param_1 >> 1 ^ param_1 ^ param_1 >> 4 ^ param_1 >> 5 ^ param_1 >> 6 ^
                                   param_1 >> 9 ^ param_1 >> 0xb ^ param_1 >> 0xe ^ param_1 >> 0x10) <<
                                  0x15) & 0x200000) |
                    (((param_1 >> 0x13 ^
                                   param_1 >> 1 ^ param_1 >> 2 ^ param_1 >> 5 ^ param_1 >> 8 ^
                                   param_1 >> 10 ^ param_1 >> 0xb ^ param_1 >> 0xc ^ param_1 >> 0xd ^
                                   param_1 >> 0xe ^ param_1 >> 0x10 ^ param_1 >> 0x11 ^ param_1 >> 0x12)
                                  << 0x16) & 0x400000) |
                    (((param_1 >> 0x12 ^
                                   param_1 >> 3 ^ param_1 ^ param_1 >> 4 ^ param_1 >> 5 ^ param_1 >> 7 ^
                                   param_1 >> 8 ^ param_1 >> 10 ^ param_1 >> 0xe ^ param_1 >> 0x10 ^
                                   param_1 >> 0x11) << 0x17) & 0x800000) |
                    (((param_1 >> 0xe ^
                                   param_1 >> 4 ^ param_1 >> 5 ^ param_1 >> 6 ^ param_1 >> 9) << 0x18) &
                           0x1000000) |
                    (((param_1 >> 0x13 ^
                                   param_1 >> 1 ^ param_1 >> 3 ^ param_1 >> 5 ^ param_1 >> 6 ^
                                   param_1 >> 9 ^ param_1 >> 10 ^ param_1 >> 0xb ^ param_1 >> 0xc ^
                                   param_1 >> 0x11) << 0x19) & 0x2000000) |
                    (((param_1 >> 0x10 ^
                                   param_1 >> 1 ^ param_1 ^ param_1 >> 5 ^ param_1 >> 8 ^ param_1 >> 9 ^
                                   param_1 >> 10 ^ param_1 >> 0xd ^ param_1 >> 0xe) << 0x1a) & 0x4000000
                           ) |
                    (((param_1 >> 0x12 ^
                                   param_1 >> 1 ^ param_1 ^ param_1 >> 2 ^ param_1 >> 3 ^ param_1 >> 9 ^
                                   param_1 >> 0xd ^ param_1 >> 0x10 ^ param_1 >> 0x11) << 0x1b) &
                           0x8000000) |
                    (((param_1 >> 0x13 ^
                                   param_1 >> 4 ^ param_1 ^ param_1 >> 7 ^ param_1 >> 10 ^
                                   param_1 >> 0xb ^ param_1 >> 0xc ^ param_1 >> 0x11) << 0x1c) &
                           0x10000000) |
                    (((param_1 >> 10 ^
                                   param_1 >> 1 ^ param_1 >> 2 ^ param_1 >> 3 ^ param_1 >> 4 ^
                                   param_1 >> 5 ^ param_1 >> 6 ^ param_1 >> 9) << 0x1d) & 0x20000000) |
                    (((param_1 >> 0x12 ^
                                   param_1 >> 4 ^ param_1 ^ param_1 >> 6 ^ param_1 >> 10 ^
                                   param_1 >> 0xb ^ param_1 >> 0xc ^ param_1 >> 0xd ^ param_1 >> 0xe ^
                                   param_1 >> 0xf) << 0x1e) & 0x40000000) |
                    ((param_1 >> 0x12 ^
                     param_1 >> 3 ^ param_1 ^ param_1 >> 5 ^ param_1 >> 6 ^ param_1 >> 0xb ^
                     param_1 >> 0xc ^ param_1 >> 0xd ^ param_1 >> 0xf ^ param_1 >> 0x10) & 1) << 0x1f |
                    ((param_1 >> 0x12 ^
                     param_1 >> 1 ^ param_1 ^ param_1 >> 3 ^ param_1 >> 4 ^ param_1 >> 6 ^ param_1 >> 7
                     ^ param_1 >> 8 ^ param_1 >> 0xc ^ param_1 >> 0xf ^ param_1 >> 0x10 ^
                     param_1 >> 0x11) & 1) << 0x20 |
                    ((param_1 >> 0x12 ^
                     param_1 >> 1 ^ param_1 ^ param_1 >> 2 ^ param_1 >> 5 ^ param_1 >> 7 ^
                     param_1 >> 0xb ^ param_1 >> 0xc) & 1) << 0x21 |
                    ((param_1 >> 0x10 ^
                     param_1 >> 1 ^ param_1 >> 3 ^ param_1 >> 5 ^ param_1 >> 8 ^ param_1 >> 10 ^
                     param_1 >> 0xc ^ param_1 >> 0xe) & 1) << 0x22 |
                    ((param_1 >> 0x12 ^
                     param_1 >> 2 ^ param_1 >> 4 ^ param_1 >> 7 ^ param_1 >> 9 ^ param_1 >> 10 ^
                     param_1 >> 0xb ^ param_1 >> 0xd ^ param_1 >> 0xf ^ param_1 >> 0x10) & 1) << 0x23 |
                    ((param_1 >> 0x11 ^
                     param_1 >> 1 ^ param_1 ^ param_1 >> 2 ^ param_1 >> 3 ^ param_1 >> 10 ^
                     param_1 >> 0xe ^ param_1 >> 0xf ^ param_1 >> 0x10) & 1) << 0x24 |
                    ((param_1 >> 0x11 ^
                     param_1 >> 2 ^ param_1 >> 4 ^ param_1 >> 6 ^ param_1 >> 7 ^ param_1 >> 9 ^
                     param_1 >> 0xc ^ param_1 >> 0xd ^ param_1 >> 0xe ^ param_1 >> 0xf) & 1) << 0x25 |
                    ((param_1 >> 0x13 ^
                     param_1 >> 1 ^ param_1 >> 4 ^ param_1 >> 5 ^ param_1 >> 6 ^ param_1 >> 7 ^
                     param_1 >> 0xd ^ param_1 >> 0xe ^ param_1 >> 0x11) & 1) << 0x26)

def f2(param_1):
    uVar2 = (param_1 >> 8)
    uVar1 = (param_1 >> 0x10)
    return (((param_1 >> 0x13 ^
          param_1 >> 1 ^ param_1 ^ param_1 >> 2 ^ param_1 >> 3 ^ param_1 >> 4 ^ param_1 >> 0xb ^
          param_1 >> 0xd ^ param_1 >> 0xf ^ param_1 >> 0x10 ^ param_1 >> 0x11) & 1) << 0x27 |
         (((param_1 >> 0x13) ^
                 (param_1 >> 1) ^ param_1 ^ (param_1 >> 2) ^ (param_1 >> 5)
                 ^ (param_1 >> 7) ^ uVar2 ^ (param_1 >> 0xc) ^ (param_1 >> 0xd) ^
                 uVar1 ^ (param_1 >> 0x12)) & 1 |
                 ((param_1 >> 0x12) ^
                 (param_1 >> 4) ^ (param_1 >> 5) ^ (param_1 >> 6) ^
                 (param_1 >> 7) ^ uVar2 ^ (param_1 >> 9) ^ (param_1 >> 10) ^
                 (param_1 >> 0xb) ^ (param_1 >> 0xf) ^ uVar1) * 2 & 2 |
                 ((param_1 >> 0x13 ^
                        param_1 >> 1 ^ param_1 ^ param_1 >> 2 ^ param_1 >> 6 ^ param_1 >> 7 ^
                        param_1 >> 0x10) << 2) & 4 |
                 ((param_1 >> 0x12 ^
                        param_1 >> 1 ^ param_1 >> 7 ^ param_1 >> 9 ^ param_1 >> 0xb ^ param_1 >> 0xc
                        ^ param_1 >> 0xd ^ param_1 >> 0x10) << 3) & 8 |
                 ((param_1 >> 0x11 ^
                        param_1 >> 3 ^ param_1 ^ param_1 >> 4 ^ param_1 >> 5 ^ param_1 >> 8 ^
                        param_1 >> 9 ^ param_1 >> 0xc ^ param_1 >> 0xe ^ param_1 >> 0xf) << 4) &
                 0x10 | ((param_1 >> 0x13 ^
                               param_1 >> 1 ^ param_1 >> 3 ^ param_1 >> 4 ^ param_1 >> 6 ^
                               param_1 >> 7 ^ param_1 >> 8 ^ param_1 >> 9 ^ param_1 >> 10 ^
                               param_1 >> 0xc ^ param_1 >> 0x11) << 5) & 0x20 |
                ((param_1 >> 0x13 ^
                       param_1 >> 2 ^ param_1 >> 3 ^ param_1 >> 5 ^ param_1 >> 7 ^ param_1 >> 10 ^
                       param_1 >> 0xd ^ param_1 >> 0xe ^ param_1 >> 0xf) << 6) & 0x40) |
         ((param_1 >> 0x13 ^
          param_1 >> 2 ^ param_1 ^ param_1 >> 5 ^ param_1 >> 8 ^ param_1 >> 10 ^ param_1 >> 0xb ^
          param_1 >> 0xc ^ param_1 >> 0xd ^ param_1 >> 0xe ^ param_1 >> 0xf ^ param_1 >> 0x12) & 1)
         << 7 | (((param_1 >> 0x12 ^
                               param_1 >> 2 ^ param_1 ^ param_1 >> 4 ^ param_1 >> 5 ^ param_1 >> 8 ^
                               param_1 >> 10 ^ param_1 >> 0xc ^ param_1 >> 0xe ^ param_1 >> 0x11) <<
                              8) & 0x100) |
         (((param_1 >> 0x13 ^
                        param_1 >> 3 ^ param_1 ^ param_1 >> 4 ^ param_1 >> 5 ^ param_1 >> 0xb ^
                        param_1 >> 0xc) << 9) & 0x200) |
         (((param_1 >> 0x13 ^
                        param_1 >> 1 ^ param_1 >> 5 ^ param_1 >> 6 ^ param_1 >> 7 ^ param_1 >> 8 ^
                        param_1 >> 9 ^ param_1 >> 10 ^ param_1 >> 0xb ^ param_1 >> 0xc ^
                        param_1 >> 0xe ^ param_1 >> 0xf ^ param_1 >> 0x11) << 10) & 0x400) |
         (((param_1 >> 0x13 ^
                        param_1 >> 5 ^ param_1 >> 7 ^ param_1 >> 0xc ^ param_1 >> 0xe ^
                        param_1 >> 0x11 ^ param_1 >> 0x12) << 0xb) & 0x800) |
         (((param_1 >> 0x12 ^
                        param_1 >> 4 ^ param_1 ^ param_1 >> 5 ^ param_1 >> 6 ^ param_1 >> 9 ^
                        param_1 >> 10 ^ param_1 >> 0xd ^ param_1 >> 0x10 ^ param_1 >> 0x11) << 0xc)
                & 0x1000) |
         (((param_1 >> 0x12 ^
                        param_1 >> 4 ^ param_1 >> 6 ^ param_1 >> 10 ^ param_1 >> 0xb ^
                        param_1 >> 0xc ^ param_1 >> 0xe ^ param_1 >> 0xf ^ param_1 >> 0x10) << 0xd)
                & 0x2000) |
         (((param_1 >> 0x13 ^
                        param_1 >> 1 ^ param_1 >> 2 ^ param_1 >> 5 ^ param_1 >> 6 ^ param_1 >> 8 ^
                        param_1 >> 9 ^ param_1 >> 0xb ^ param_1 >> 0xc ^ param_1 >> 0xe) << 0xe) &
                0x4000) |
         ((param_1 >> 0x11 ^
          param_1 >> 1 ^ param_1 >> 2 ^ param_1 >> 5 ^ param_1 >> 9 ^ param_1 >> 10 ^ param_1 >> 0xd
          ) & 1) << 0xf |
         (((param_1 >> 0x12 ^
                        param_1 >> 3 ^ param_1 >> 4 ^ param_1 >> 6 ^ param_1 >> 7 ^ param_1 >> 8 ^
                        param_1 >> 0xb ^ param_1 >> 0xc) << 0x10) & 0x10000) |
         (((param_1 >> 0x13 ^
                        param_1 >> 3 ^ param_1 ^ param_1 >> 8 ^ param_1 >> 10 ^ param_1 >> 0xd ^
                        param_1 >> 0xe ^ param_1 >> 0xf ^ param_1 >> 0x10) << 0x11) & 0x20000) |
         (((param_1 >> 0x13 ^
                        param_1 >> 2 ^ param_1 >> 3 ^ param_1 >> 4 ^ param_1 >> 6 ^ param_1 >> 7 ^
                        param_1 >> 8 ^ param_1 >> 9 ^ param_1 >> 10 ^ param_1 >> 0xb ^
                        param_1 >> 0xd ^ param_1 >> 0xe ^ param_1 >> 0x10 ^ param_1 >> 0x11 ^
                        param_1 >> 0x12) << 0x12) & 0x40000) |
         (((param_1 >> 0x13 ^
                        param_1 >> 1 ^ param_1 ^ param_1 >> 2 ^ param_1 >> 5 ^ param_1 >> 8 ^
                        param_1 >> 9 ^ param_1 >> 10 ^ param_1 >> 0xc ^ param_1 >> 0xe ^
                        param_1 >> 0xf ^ param_1 >> 0x11 ^ param_1 >> 0x12) << 0x13) & 0x80000) |
         (((param_1 >> 0x13 ^
                        param_1 >> 2 ^ param_1 >> 5 ^ param_1 >> 6 ^ param_1 >> 0xc ^ param_1 >> 0xd
                        ^ param_1 >> 0x10 ^ param_1 >> 0x11 ^ param_1 >> 0x12) << 0x14) & 0x100000)
         | (((param_1 >> 0x12 ^
                          param_1 >> 1 ^ param_1 ^ param_1 >> 3 ^ param_1 >> 4 ^ param_1 >> 6 ^
                          param_1 >> 9 ^ param_1 >> 10 ^ param_1 >> 0xd ^ param_1 >> 0xe ^
                          param_1 >> 0x10) << 0x15) & 0x200000) |
         (((param_1 >> 0x12 ^
                        param_1 >> 1 ^ param_1 ^ param_1 >> 2 ^ param_1 >> 3 ^ param_1 >> 5 ^
                        param_1 >> 10 ^ param_1 >> 0xb ^ param_1 >> 0xf ^ param_1 >> 0x10 ^
                        param_1 >> 0x11) << 0x16) & 0x400000) |
         (((param_1 >> 0x12 ^
                        param_1 >> 1 ^ param_1 >> 2 ^ param_1 >> 3 ^ param_1 >> 5 ^ param_1 >> 7 ^
                        param_1 >> 8 ^ param_1 >> 0xd ^ param_1 >> 0xe) << 0x17) & 0x800000) |
         (((param_1 >> 0x12 ^
                        param_1 >> 1 ^ param_1 >> 3 ^ param_1 >> 5 ^ param_1 >> 10 ^ param_1 >> 0xb
                        ^ param_1 >> 0xc ^ param_1 >> 0xe ^ param_1 >> 0x10) << 0x18) & 0x1000000) |
         (((param_1 >> 0x12 ^
                        param_1 >> 2 ^ param_1 ^ param_1 >> 3 ^ param_1 >> 6 ^ param_1 >> 7 ^
                        param_1 >> 0xc ^ param_1 >> 0xd ^ param_1 >> 0xe ^ param_1 >> 0xf ^
                        param_1 >> 0x10 ^ param_1 >> 0x11) << 0x19) & 0x2000000) |
         (((param_1 >> 0x12 ^
                        param_1 >> 1 ^ param_1 >> 3 ^ param_1 >> 6 ^ param_1 >> 7 ^ param_1 >> 8 ^
                        param_1 >> 0xb ^ param_1 >> 0xe ^ param_1 >> 0xf ^ param_1 >> 0x10 ^
                        param_1 >> 0x11) << 0x1a) & 0x4000000) |
         (((param_1 >> 0x10 ^
                        param_1 >> 1 ^ param_1 >> 4 ^ param_1 >> 5 ^ param_1 >> 0xb ^ param_1 >> 0xc
                        ^ param_1 >> 0xd ^ param_1 >> 0xf) << 0x1b) & 0x8000000) |
         (((param_1 >> 0xd ^
                        param_1 >> 1 ^ param_1 ^ param_1 >> 3 ^ param_1 >> 4 ^ param_1 >> 5 ^
                        param_1 >> 10 ^ param_1 >> 0xb ^ param_1 >> 0xc) << 0x1c) & 0x10000000) |
         (((param_1 >> 0x10 ^
                        param_1 >> 2 ^ param_1 ^ param_1 >> 3 ^ param_1 >> 6 ^ param_1 >> 7 ^
                        param_1 >> 8 ^ param_1 >> 9 ^ param_1 >> 10 ^ param_1 >> 0xb ^
                        param_1 >> 0xe) << 0x1d) & 0x20000000) |
         (((param_1 >> 0x13 ^
                        param_1 >> 1 ^ param_1 >> 2 ^ param_1 >> 3 ^ param_1 >> 7 ^ param_1 >> 8 ^
                        param_1 >> 10 ^ param_1 >> 0xe ^ param_1 >> 0x10 ^ param_1 >> 0x11 ^
                        param_1 >> 0x12) << 0x1e) & 0x40000000) |
         ((param_1 >> 0x13 ^
          param_1 >> 1 ^ param_1 >> 3 ^ param_1 >> 4 ^ param_1 >> 5 ^ param_1 >> 8 ^ param_1 >> 9 ^
          param_1 >> 0xb ^ param_1 >> 0xe ^ param_1 >> 0xf ^ param_1 >> 0x10 ^ param_1 >> 0x11 ^
          param_1 >> 0x12) & 1) << 0x1f |
         ((param_1 >> 0x10 ^
          param_1 >> 2 ^ param_1 >> 4 ^ param_1 >> 5 ^ param_1 >> 6 ^ param_1 >> 7 ^ param_1 >> 10 ^
          param_1 >> 0xd ^ param_1 >> 0xe ^ param_1 >> 0xf) & 1) << 0x20 |
         ((param_1 >> 0x13 ^
          param_1 >> 2 ^ param_1 >> 4 ^ param_1 >> 5 ^ param_1 >> 7 ^ param_1 >> 9 ^ param_1 >> 0xb
          ^ param_1 >> 0xe ^ param_1 >> 0xf ^ param_1 >> 0x10 ^ param_1 >> 0x12) & 1) << 0x21 |
         ((param_1 >> 0x13 ^
          param_1 >> 1 ^ param_1 ^ param_1 >> 4 ^ param_1 >> 5 ^ param_1 >> 6 ^ param_1 >> 7 ^
          param_1 >> 8 ^ param_1 >> 0xb ^ param_1 >> 0xd ^ param_1 >> 0xe ^ param_1 >> 0x12) & 1) <<
         0x22 | ((param_1 >> 0x12 ^
                 param_1 >> 1 ^ param_1 >> 4 ^ param_1 >> 6 ^ param_1 >> 9 ^ param_1 >> 0xc ^
                 param_1 >> 0xf) & 1) << 0x23 |
         ((param_1 >> 0x13 ^
          param_1 >> 1 ^ param_1 >> 3 ^ param_1 >> 5 ^ param_1 >> 0xb ^ param_1 >> 0xf ^
          param_1 >> 0x10 ^ param_1 >> 0x11) & 1) << 0x24 |
         ((param_1 >> 0x13 ^
          param_1 >> 1 ^ param_1 >> 3 ^ param_1 >> 4 ^ param_1 >> 5 ^ param_1 >> 6 ^ param_1 >> 8 ^
          param_1 >> 9 ^ param_1 >> 0xc ^ param_1 >> 0xd ^ param_1 >> 0xf ^ param_1 >> 0x10) & 1) <<
         0x25 | ((param_1 >> 0x11 ^
                 param_1 >> 1 ^ param_1 >> 4 ^ param_1 >> 5 ^ param_1 >> 7 ^ param_1 >> 8 ^
                 param_1 >> 0xb ^ param_1 >> 0xc ^ param_1 >> 0xe ^ param_1 >> 0x10) & 1) << 0x26)

def f3(param_1):
    return (((param_1 >> 0x10 ^
          param_1 >> 1 ^ param_1 >> 2 ^ param_1 >> 3 ^ param_1 >> 5 ^ param_1 >> 7 ^ param_1 >> 8 ^
          param_1 >> 9 ^ param_1 >> 10 ^ param_1 >> 0xc ^ param_1 >> 0xe ^ param_1 >> 0xf) & 1) <<
         0x27 | (((param_1 >> 0x10) ^
                        (param_1 >> 2) ^ param_1 ^ (param_1 >> 3) ^
                        (param_1 >> 5) ^ (param_1 >> 0xc) ^ (param_1 >> 0xd)) & 1
                        | ((param_1 >> 0x13) ^
                          (param_1 >> 2) ^ (param_1 >> 3) ^ (param_1 >> 5) ^
                          (param_1 >> 9) ^ (param_1 >> 0xc) ^ (param_1 >> 0xd) ^
                          (param_1 >> 0xf)) * 2 & 2 |
                        ((param_1 >> 0x13 ^
                               param_1 >> 2 ^ param_1 ^ param_1 >> 3 ^ param_1 >> 4 ^ param_1 >> 6 ^
                               param_1 >> 7 ^ param_1 >> 9 ^ param_1 >> 0xb ^ param_1 >> 0xc ^
                               param_1 >> 0xe ^ param_1 >> 0xf ^ param_1 >> 0x10 ^ param_1 >> 0x12)
                              << 2) & 4 |
                        ((param_1 >> 0x10 ^ param_1 >> 4 ^ param_1 >> 0xb ^ param_1 >> 0xd) <<
                              3) & 8 |
                        ((param_1 >> 0x12 ^
                               param_1 >> 3 ^ param_1 ^ param_1 >> 6 ^ param_1 >> 8 ^ param_1 >> 10
                               ^ param_1 >> 0xc ^ param_1 >> 0xd ^ param_1 >> 0xe ^ param_1 >> 0x11)
                              << 4) & 0x10 |
                        ((param_1 >> 0x13 ^
                               param_1 >> 1 ^ param_1 >> 2 ^ param_1 >> 3 ^ param_1 >> 5 ^
                               param_1 >> 6 ^ param_1 >> 9 ^ param_1 >> 0xb ^ param_1 >> 0xd ^
                               param_1 >> 0xf) << 5) & 0x20 |
                       ((param_1 >> 0x12 ^
                              param_1 >> 2 ^ param_1 >> 6 ^ param_1 >> 0xb ^ param_1 >> 0xc ^
                              param_1 >> 0xd ^ param_1 >> 0xe ^ param_1 >> 0x10 ^ param_1 >> 0x11)
                             << 6) & 0x40) |
                ((param_1 >> 0x11 ^
                 param_1 >> 4 ^ param_1 >> 5 ^ param_1 >> 7 ^ param_1 >> 9 ^ param_1 >> 0xe) & 1) <<
                7 | (((param_1 >> 0x11 ^
                                   param_1 >> 2 ^ param_1 ^ param_1 >> 3 ^ param_1 >> 4 ^
                                   param_1 >> 6 ^ param_1 >> 7 ^ param_1 >> 8 ^ param_1 >> 9 ^
                                   param_1 >> 10 ^ param_1 >> 0xb ^ param_1 >> 0x10) << 8) & 0x100)
                | (((param_1 >> 0xf ^
                                 param_1 >> 5 ^ param_1 ^ param_1 >> 6 ^ param_1 >> 8 ^
                                 param_1 >> 10 ^ param_1 >> 0xb) << 9) & 0x200) |
                (((param_1 >> 0x12 ^
                               param_1 >> 1 ^ param_1 ^ param_1 >> 4 ^ param_1 >> 5 ^ param_1 >> 6 ^
                               param_1 >> 9 ^ param_1 >> 10 ^ param_1 >> 0xb ^ param_1 >> 0xc ^
                               param_1 >> 0xd ^ param_1 >> 0x10 ^ param_1 >> 0x11) << 10) & 0x400) |
                (((param_1 >> 0x13 ^
                               param_1 >> 3 ^ param_1 >> 4 ^ param_1 >> 6 ^ param_1 >> 8 ^
                               param_1 >> 9 ^ param_1 >> 0xd ^ param_1 >> 0x11) << 0xb) & 0x800) |
                (((param_1 >> 0x13 ^
                               param_1 >> 3 ^ param_1 >> 4 ^ param_1 >> 5 ^ param_1 >> 9 ^
                               param_1 >> 10 ^ param_1 >> 0xd ^ param_1 >> 0xf ^ param_1 >> 0x10 ^
                               param_1 >> 0x12) << 0xc) & 0x1000) |
                (((param_1 >> 0x12 ^
                               param_1 >> 2 ^ param_1 ^ param_1 >> 4 ^ param_1 >> 6 ^ param_1 >> 8 ^
                               param_1 >> 0xc) << 0xd) & 0x2000) |
                (((param_1 >> 0x13 ^
                               param_1 >> 2 ^ param_1 >> 3 ^ param_1 >> 5 ^ param_1 >> 8 ^
                               param_1 >> 0xd ^ param_1 >> 0x12) << 0xe) & 0x4000) |
                ((param_1 >> 0x13 ^
                 param_1 >> 2 ^ param_1 >> 4 ^ param_1 >> 8 ^ param_1 >> 0xb ^ param_1 >> 0xf ^
                 param_1 >> 0x10 ^ param_1 >> 0x11) & 1) << 0xf |
                (((param_1 >> 0xe ^
                               param_1 >> 2 ^ param_1 ^ param_1 >> 3 ^ param_1 >> 8 ^ param_1 >> 9 ^
                               param_1 >> 0xb ^ param_1 >> 0xc ^ param_1 >> 0xd) << 0x10) & 0x10000)
                | (((param_1 >> 0x12 ^
                                 param_1 >> 1 ^ param_1 >> 2 ^ param_1 >> 5 ^ param_1 >> 7 ^
                                 param_1 >> 8 ^ param_1 >> 0xc ^ param_1 >> 0x11) << 0x11) & 0x20000
                         ) |
                (((param_1 >> 0x13 ^
                               param_1 >> 3 ^ param_1 >> 7 ^ param_1 >> 8 ^ param_1 >> 10 ^
                               param_1 >> 0xb ^ param_1 >> 0xc ^ param_1 >> 0xd ^ param_1 >> 0xf ^
                               param_1 >> 0x11 ^ param_1 >> 0x12) << 0x12) & 0x40000) |
                (((param_1 >> 0x12 ^
                               param_1 >> 1 ^ param_1 >> 2 ^ param_1 >> 3 ^ param_1 >> 4 ^
                               param_1 >> 5 ^ param_1 >> 7 ^ param_1 >> 10 ^ param_1 >> 0xf ^
                               param_1 >> 0x11) << 0x13) & 0x80000) |
                (((param_1 >> 0x10 ^
                               param_1 >> 4 ^ param_1 >> 5 ^ param_1 >> 6 ^ param_1 >> 0xc ^
                               param_1 >> 0xe) << 0x14) & 0x100000) |
                (((param_1 >> 0x11 ^
                               param_1 >> 2 ^ param_1 ^ param_1 >> 3 ^ param_1 >> 4 ^ param_1 >> 8 ^
                               param_1 >> 0xb ^ param_1 >> 0xc ^ param_1 >> 0xe) << 0x15) & 0x200000
                       ) |
                (((param_1 >> 0x13 ^
                               param_1 >> 1 ^ param_1 ^ param_1 >> 2 ^ param_1 >> 4 ^ param_1 >> 5 ^
                               param_1 >> 6 ^ param_1 >> 7 ^ param_1 >> 9 ^ param_1 >> 0xd ^
                               param_1 >> 0xe ^ param_1 >> 0xf ^ param_1 >> 0x10 ^ param_1 >> 0x11 ^
                               param_1 >> 0x12) << 0x16) & 0x400000) |
                (((param_1 >> 0x13 ^
                               param_1 >> 1 ^ param_1 ^ param_1 >> 2 ^ param_1 >> 4 ^ param_1 >> 5 ^
                               param_1 >> 8 ^ param_1 >> 10 ^ param_1 >> 0xb ^ param_1 >> 0xc ^
                               param_1 >> 0xe ^ param_1 >> 0x10 ^ param_1 >> 0x11) << 0x17) &
                       0x800000) |
                (((param_1 >> 0x10 ^
                               param_1 >> 3 ^ param_1 ^ param_1 >> 4 ^ param_1 >> 7 ^ param_1 >> 0xd
                               ^ param_1 >> 0xf) << 0x18) & 0x1000000) |
                (((param_1 >> 0x12 ^
                               param_1 >> 2 ^ param_1 ^ param_1 >> 4 ^ param_1 >> 6 ^ param_1 >> 8 ^
                               param_1 >> 9 ^ param_1 >> 10 ^ param_1 >> 0xc ^ param_1 >> 0x10) <<
                              0x19) & 0x2000000) |
                (((param_1 >> 0x13 ^
                               param_1 >> 1 ^ param_1 ^ param_1 >> 2 ^ param_1 >> 3 ^ param_1 >> 4 ^
                               param_1 >> 5 ^ param_1 >> 6 ^ param_1 >> 7 ^ param_1 >> 0xb ^
                               param_1 >> 0xc ^ param_1 >> 0xe ^ param_1 >> 0x10) << 0x1a) &
                       0x4000000) |
                (((param_1 >> 0x11 ^
                               param_1 >> 2 ^ param_1 ^ param_1 >> 3 ^ param_1 >> 4 ^ param_1 >> 6 ^
                               param_1 >> 9 ^ param_1 >> 0xc ^ param_1 >> 0xd ^ param_1 >> 0xf) <<
                              0x1b) & 0x8000000) |
                (((param_1 >> 0x11 ^
                               param_1 >> 8 ^ param_1 ^ param_1 >> 0xc ^ param_1 >> 0xd ^
                               param_1 >> 0xe ^ param_1 >> 0xf ^ param_1 >> 0x10) << 0x1c) &
                       0x10000000) |
                (((param_1 >> 0x13 ^
                               param_1 >> 1 ^ param_1 >> 2 ^ param_1 >> 4 ^ param_1 >> 6 ^
                               param_1 >> 7 ^ param_1 >> 8 ^ param_1 >> 10 ^ param_1 >> 0xd ^
                               param_1 >> 0x10) << 0x1d) & 0x20000000) |
                (((param_1 >> 0x12 ^
                               param_1 >> 1 ^ param_1 >> 3 ^ param_1 >> 5 ^ param_1 >> 7 ^
                               param_1 >> 8 ^ param_1 >> 9 ^ param_1 >> 0xb ^ param_1 >> 0xd ^
                               param_1 >> 0xe ^ param_1 >> 0xf ^ param_1 >> 0x10) << 0x1e) &
                       0x40000000) |
                ((param_1 >> 0x13 ^
                 param_1 >> 1 ^ param_1 ^ param_1 >> 2 ^ param_1 >> 3 ^ param_1 >> 4 ^ param_1 >> 5
                 ^ param_1 >> 6 ^ param_1 >> 9 ^ param_1 >> 10 ^ param_1 >> 0xc ^ param_1 >> 0xd ^
                 param_1 >> 0xe ^ param_1 >> 0xf) & 1) << 0x1f |
                ((param_1 >> 0x13 ^
                 param_1 >> 2 ^ param_1 >> 3 ^ param_1 >> 5 ^ param_1 >> 8 ^ param_1 >> 10 ^
                 param_1 >> 0xb ^ param_1 >> 0xd ^ param_1 >> 0xe ^ param_1 >> 0x11 ^
                 param_1 >> 0x12) & 1) << 0x20 |
                ((param_1 >> 0x13 ^
                 param_1 >> 1 ^ param_1 ^ param_1 >> 4 ^ param_1 >> 7 ^ param_1 >> 9 ^ param_1 >> 10
                 ^ param_1 >> 0xb ^ param_1 >> 0xe ^ param_1 >> 0xf ^ param_1 >> 0x10 ^
                 param_1 >> 0x12) & 1) << 0x21 |
                ((param_1 >> 0x13 ^
                 param_1 >> 2 ^ param_1 ^ param_1 >> 5 ^ param_1 >> 6 ^ param_1 >> 7 ^ param_1 >> 9
                 ^ param_1 >> 10 ^ param_1 >> 0xb ^ param_1 >> 0xc ^ param_1 >> 0xd ^ param_1 >> 0xe
                 ^ param_1 >> 0xf) & 1) << 0x22 |
                ((param_1 >> 0x13 ^
                 param_1 >> 3 ^ param_1 >> 5 ^ param_1 >> 8 ^ param_1 >> 9 ^ param_1 >> 0xc ^
                 param_1 >> 0xd) & 1) << 0x23 |
                ((param_1 >> 0x13 ^
                 param_1 >> 2 ^ param_1 >> 5 ^ param_1 >> 7 ^ param_1 >> 8 ^ param_1 >> 9 ^
                 param_1 >> 0xb ^ param_1 >> 0xd) & 1) << 0x24 |
                ((param_1 >> 0x12 ^
                 param_1 >> 1 ^ param_1 >> 2 ^ param_1 >> 4 ^ param_1 >> 5 ^ param_1 >> 7 ^
                 param_1 >> 8 ^ param_1 >> 10 ^ param_1 >> 0xb ^ param_1 >> 0xc ^ param_1 >> 0xd ^
                 param_1 >> 0xe ^ param_1 >> 0xf) & 1) << 0x25 |
                ((param_1 >> 0x12 ^
                 param_1 >> 2 ^ param_1 >> 3 ^ param_1 >> 4 ^ param_1 >> 7 ^ param_1 >> 10 ^
                 param_1 >> 0xb ^ param_1 >> 0xe ^ param_1 >> 0xf ^ param_1 >> 0x10) & 1) << 0x26)

def f4(param_1):
    uVar2 = (param_1 >> 8)
    uVar1 = (param_1 >> 0x10)
    return (((param_1 >> 0x12 ^
          param_1 >> 2 ^ param_1 ^ param_1 >> 3 ^ param_1 >> 4 ^ param_1 >> 6 ^ param_1 >> 7 ^
          param_1 >> 8 ^ param_1 >> 9 ^ param_1 >> 0xb ^ param_1 >> 0xc) & 1) << 0x27 |
         ((uVar1 ^ (param_1 >> 7) ^ uVar2 ^ (param_1 >> 0xc) ^
                          (param_1 >> 0xd) ^ (param_1 >> 0xe)) & 1 |
                 ((param_1 >> 0x13) ^
                 (param_1 >> 1) ^ param_1 ^ (param_1 >> 3) ^ (param_1 >> 4)
                 ^ (param_1 >> 5) ^ (param_1 >> 6) ^ (param_1 >> 7) ^ uVar2 ^
                 (param_1 >> 9) ^ (param_1 >> 10) ^ (param_1 >> 0xc) ^
                 (param_1 >> 0xf) ^ uVar1) * 2 & 2 |
                 ((param_1 >> 0x12 ^
                        param_1 >> 3 ^ param_1 ^ param_1 >> 5 ^ param_1 >> 8 ^ param_1 >> 0xb) << 2)
                 & 4 | ((param_1 >> 0x12 ^
                              param_1 >> 1 ^ param_1 ^ param_1 >> 2 ^ param_1 >> 4 ^ param_1 >> 5 ^
                              param_1 >> 7 ^ param_1 >> 9 ^ param_1 >> 10 ^ param_1 >> 0xd) << 3) &
                       8 | ((param_1 >> 0x13 ^
                                  param_1 >> 1 ^ param_1 ^ param_1 >> 2 ^ param_1 >> 4 ^
                                  param_1 >> 6 ^ param_1 >> 9 ^ param_1 >> 0xb ^ param_1 >> 0xc ^
                                  param_1 >> 0xd ^ param_1 >> 0xf ^ param_1 >> 0x10) << 4) & 0x10 |
                 ((param_1 >> 0x12 ^
                        param_1 >> 4 ^ param_1 >> 5 ^ param_1 >> 8 ^ param_1 >> 9 ^ param_1 >> 10 ^
                        param_1 >> 0xc ^ param_1 >> 0xf) << 5) & 0x20 |
                ((param_1 >> 0xe ^
                       param_1 >> 1 ^ param_1 >> 2 ^ param_1 >> 4 ^ param_1 >> 5 ^ param_1 >> 6 ^
                       param_1 >> 7 ^ param_1 >> 8 ^ param_1 >> 0xc) << 6) & 0x40) |
         ((param_1 >> 0x13 ^
          param_1 >> 2 ^ param_1 ^ param_1 >> 3 ^ param_1 >> 4 ^ param_1 >> 5 ^ param_1 >> 10 ^
          param_1 >> 0xc ^ param_1 >> 0xd ^ param_1 >> 0xf ^ param_1 >> 0x10 ^ param_1 >> 0x12) & 1)
         << 7 | (((param_1 >> 0x13 ^
                               param_1 >> 2 ^ param_1 ^ param_1 >> 3 ^ param_1 >> 5 ^ param_1 >> 9 ^
                               param_1 >> 0xd ^ param_1 >> 0xe ^ param_1 >> 0x11 ^ param_1 >> 0x12)
                              << 8) & 0x100) |
         (((param_1 >> 0xd ^
                        param_1 >> 6 ^ param_1 ^ param_1 >> 7 ^ param_1 >> 9 ^ param_1 >> 0xb) << 9)
                & 0x200) |
         (((param_1 >> 0x13 ^
                        param_1 >> 1 ^ param_1 >> 2 ^ param_1 >> 6 ^ param_1 >> 7 ^ param_1 >> 9 ^
                        param_1 >> 10 ^ param_1 >> 0xb ^ param_1 >> 0xc ^ param_1 >> 0xe ^
                        param_1 >> 0x10) << 10) & 0x400) |
         (((param_1 >> 0x12 ^
                        param_1 >> 1 ^ param_1 ^ param_1 >> 5 ^ param_1 >> 6 ^ param_1 >> 9 ^
                        param_1 >> 0xb ^ param_1 >> 0xf ^ param_1 >> 0x10) << 0xb) & 0x800) |
         (((param_1 >> 0x10 ^
                        param_1 >> 2 ^ param_1 ^ param_1 >> 4 ^ param_1 >> 8 ^ param_1 >> 10 ^
                        param_1 >> 0xb) << 0xc) & 0x1000) |
         (((param_1 >> 0x11 ^
                        param_1 >> 1 ^ param_1 ^ param_1 >> 2 ^ param_1 >> 3 ^ param_1 >> 5 ^
                        param_1 >> 8 ^ param_1 >> 10 ^ param_1 >> 0xb ^ param_1 >> 0xd) << 0xd) &
                0x2000) |
         (((param_1 >> 0x13 ^
                        param_1 >> 1 ^ param_1 >> 2 ^ param_1 >> 3 ^ param_1 >> 4 ^ param_1 >> 5 ^
                        param_1 >> 9 ^ param_1 >> 10 ^ param_1 >> 0xb ^ param_1 >> 0xc ^
                        param_1 >> 0xd ^ param_1 >> 0xe ^ param_1 >> 0xf ^ param_1 >> 0x12) << 0xe)
                & 0x4000) |
         ((param_1 >> 0x10 ^
          param_1 >> 1 ^ param_1 ^ param_1 >> 2 ^ param_1 >> 3 ^ param_1 >> 4 ^ param_1 >> 5 ^
          param_1 >> 6 ^ param_1 >> 9 ^ param_1 >> 0xb ^ param_1 >> 0xe) & 1) << 0xf |
         (((param_1 >> 0x13 ^
                        param_1 >> 3 ^ param_1 ^ param_1 >> 4 ^ param_1 >> 7 ^ param_1 >> 8 ^
                        param_1 >> 9 ^ param_1 >> 0xb ^ param_1 >> 0xc ^ param_1 >> 0xf ^
                        param_1 >> 0x10 ^ param_1 >> 0x12) << 0x10) & 0x10000) |
         (((param_1 >> 0x13 ^
                        param_1 >> 2 ^ param_1 ^ param_1 >> 3 ^ param_1 >> 5 ^ param_1 >> 6 ^
                        param_1 >> 7 ^ param_1 >> 9 ^ param_1 >> 0xb ^ param_1 >> 0xc ^
                        param_1 >> 0xd ^ param_1 >> 0xf ^ param_1 >> 0x12) << 0x11) & 0x20000) |
         (((param_1 >> 0xf ^
                        param_1 >> 1 ^ param_1 ^ param_1 >> 2 ^ param_1 >> 3 ^ param_1 >> 4 ^
                        param_1 >> 7 ^ param_1 >> 9 ^ param_1 >> 10 ^ param_1 >> 0xb ^
                        param_1 >> 0xd ^ param_1 >> 0xe) << 0x12) & 0x40000) |
         (((param_1 >> 0x13 ^
                        param_1 >> 4 ^ param_1 >> 5 ^ param_1 >> 6 ^ param_1 >> 8 ^ param_1 >> 10 ^
                        param_1 >> 0xf ^ param_1 >> 0x11) << 0x13) & 0x80000) |
         (((param_1 >> 0x12 ^
                        param_1 >> 2 ^ param_1 ^ param_1 >> 3 ^ param_1 >> 5 ^ param_1 >> 10 ^
                        param_1 >> 0xc ^ param_1 >> 0xe ^ param_1 >> 0xf ^ param_1 >> 0x10 ^
                        param_1 >> 0x11) << 0x14) & 0x100000) |
         (((param_1 >> 0x13 ^
                        param_1 >> 2 ^ param_1 >> 4 ^ param_1 >> 6 ^ param_1 >> 9 ^ param_1 >> 10 ^
                        param_1 >> 0xb ^ param_1 >> 0xd ^ param_1 >> 0xf ^ param_1 >> 0x10 ^
                        param_1 >> 0x12) << 0x15) & 0x200000) |
         (((param_1 >> 0x13 ^
                        param_1 >> 1 ^ param_1 ^ param_1 >> 3 ^ param_1 >> 4 ^ param_1 >> 5 ^
                        param_1 >> 6 ^ param_1 >> 8 ^ param_1 >> 10 ^ param_1 >> 0xc ^
                        param_1 >> 0xd ^ param_1 >> 0xe ^ param_1 >> 0xf ^ param_1 >> 0x11 ^
                        param_1 >> 0x12) << 0x16) & 0x400000) |
         (((param_1 >> 0x13 ^
                        param_1 >> 1 ^ param_1 ^ param_1 >> 2 ^ param_1 >> 3 ^ param_1 >> 4 ^
                        param_1 >> 6 ^ param_1 >> 8 ^ param_1 >> 9 ^ param_1 >> 10 ^ param_1 >> 0xc
                        ^ param_1 >> 0xd ^ param_1 >> 0x10 ^ param_1 >> 0x11 ^ param_1 >> 0x12) <<
                       0x17) & 0x800000) |
         (((param_1 >> 0x13 ^
                        param_1 >> 4 ^ param_1 >> 5 ^ param_1 >> 8 ^ param_1 >> 9 ^ param_1 >> 0xd ^
                        param_1 >> 0xe ^ param_1 >> 0xf ^ param_1 >> 0x10) << 0x18) & 0x1000000) |
         (((param_1 >> 0x13 ^
                        param_1 >> 1 ^ param_1 >> 4 ^ param_1 >> 5 ^ param_1 >> 0xb ^ param_1 >> 0xc
                        ^ param_1 >> 0x10 ^ param_1 >> 0x11 ^ param_1 >> 0x12) << 0x19) & 0x2000000)
         | (((param_1 >> 0x12 ^
                          param_1 >> 1 ^ param_1 >> 3 ^ param_1 >> 4 ^ param_1 >> 5 ^ param_1 >> 6 ^
                          param_1 >> 8 ^ param_1 >> 9 ^ param_1 >> 10 ^ param_1 >> 0xb ^
                          param_1 >> 0xd ^ param_1 >> 0xf ^ param_1 >> 0x10 ^ param_1 >> 0x11) <<
                         0x1a) & 0x4000000) |
         (((param_1 >> 0x12 ^
                        param_1 >> 1 ^ param_1 >> 3 ^ param_1 >> 4 ^ param_1 >> 5 ^ param_1 >> 6 ^
                        param_1 >> 7 ^ param_1 >> 9 ^ param_1 >> 10 ^ param_1 >> 0xb ^
                        param_1 >> 0x10 ^ param_1 >> 0x11) << 0x1b) & 0x8000000) |
         (((param_1 >> 0x12 ^
                        param_1 >> 2 ^ param_1 ^ param_1 >> 3 ^ param_1 >> 4 ^ param_1 >> 5 ^
                        param_1 >> 6 ^ param_1 >> 7 ^ param_1 >> 0xc ^ param_1 >> 0xd ^
                        param_1 >> 0xf ^ param_1 >> 0x11) << 0x1c) & 0x10000000) |
         (((param_1 >> 0x11 ^
                        param_1 >> 1 ^ param_1 >> 5 ^ param_1 >> 10 ^ param_1 >> 0xc) << 0x1d) &
                0x20000000) |
         (((param_1 >> 0x13 ^
                        param_1 >> 4 ^ param_1 >> 7 ^ param_1 >> 8 ^ param_1 >> 9 ^ param_1 >> 0xb ^
                        param_1 >> 0xc ^ param_1 >> 0x10 ^ param_1 >> 0x11) << 0x1e) & 0x40000000) |
         ((param_1 >> 0x13 ^
          param_1 >> 1 ^ param_1 ^ param_1 >> 3 ^ param_1 >> 5 ^ param_1 >> 6 ^ param_1 >> 7 ^
          param_1 >> 10 ^ param_1 >> 0xb ^ param_1 >> 0xd ^ param_1 >> 0xe ^ param_1 >> 0x10 ^
          param_1 >> 0x12) & 1) << 0x1f |
         ((param_1 >> 0x12 ^
          param_1 >> 1 ^ param_1 ^ param_1 >> 2 ^ param_1 >> 10 ^ param_1 >> 0xd ^ param_1 >> 0xe ^
          param_1 >> 0xf ^ param_1 >> 0x11) & 1) << 0x20 |
         ((param_1 >> 0x10 ^
          param_1 >> 3 ^ param_1 ^ param_1 >> 4 ^ param_1 >> 5 ^ param_1 >> 6 ^ param_1 >> 9 ^
          param_1 >> 10 ^ param_1 >> 0xb ^ param_1 >> 0xc ^ param_1 >> 0xd) & 1) << 0x21 |
         ((param_1 >> 0x12 ^
          param_1 >> 1 ^ param_1 >> 2 ^ param_1 >> 4 ^ param_1 >> 8 ^ param_1 >> 9 ^ param_1 >> 10 ^
          param_1 >> 0xc ^ param_1 >> 0xd ^ param_1 >> 0xf ^ param_1 >> 0x10 ^ param_1 >> 0x11) & 1)
         << 0x22 | ((param_1 >> 0x10 ^
                    param_1 >> 1 ^ param_1 >> 2 ^ param_1 >> 3 ^ param_1 >> 5 ^ param_1 >> 8 ^
                    param_1 >> 0xc ^ param_1 >> 0xd) & 1) << 0x23 |
         ((param_1 >> 0x11 ^
          param_1 >> 1 ^ param_1 ^ param_1 >> 2 ^ param_1 >> 3 ^ param_1 >> 5 ^ param_1 >> 6 ^
          param_1 >> 7 ^ param_1 >> 9 ^ param_1 >> 0xb ^ param_1 >> 0xf) & 1) << 0x24 |
         ((param_1 >> 0x11 ^
          param_1 >> 3 ^ param_1 ^ param_1 >> 4 ^ param_1 >> 5 ^ param_1 >> 6 ^ param_1 >> 9 ^
          param_1 >> 0xb ^ param_1 >> 0xc ^ param_1 >> 0xd ^ param_1 >> 0xe ^ param_1 >> 0xf) & 1)
         << 0x25 | ((param_1 >> 0x13 ^
                    param_1 >> 1 ^ param_1 ^ param_1 >> 2 ^ param_1 >> 3 ^ param_1 >> 4 ^
                    param_1 >> 6 ^ param_1 >> 7 ^ param_1 >> 10 ^ param_1 >> 0xb ^ param_1 >> 0xf ^
                    param_1 >> 0x10 ^ param_1 >> 0x12) & 1) << 0x26)

ds = []
fs = [f1,f2,f3,f4]
for _ in range(4):
    ds.append(dict())

for i in tqdm(range(0x100000)):
    for j in range(4):
        x = fs[j](i)
        ds[j][x] = i

with open("invfuncs", "wb") as f:
    pickle.dump(ds, f)