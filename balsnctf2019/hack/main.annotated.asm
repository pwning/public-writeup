M[esp] = M[esp+1]
esp++
M[ebp+3]=M[ebp+2]
M[ebp+4]=0
esp+=2
M[ebp+7]=0

(Loop)
M[15644]=M[KBD]
CMP M[15644], 0
JEQ SEPFTDLJ
M[15642]=M[15644]
(SEPFTDLJ)
esp++
M[ebp+9]=M[15642]
CMP M[ebp+9], 0
JNE DFXDGDTT
CMP M[ebp+4], 1
JNE QOLRZKAX
M[ebp+4]=0
(QOLRZKAX)
(DFXDGDTT)
CMP M[ebp+9], 0
JEQ RNOBKUHW
CMP M[ebp+4], 0
JNE SWCGUHJY
CMP M[ebp+9], 128
JNE MGCMJPAA

# Output_PrintChar(M[ebp+9])
M[esp] = DGMCQMZB
esp+=2
M[ARG]=esp+1
M[M[ARG]]=M[ebp+9]
jmp Output_PrintChar
(DGMCQMZB)
M[esp] = M[esp+1]

esp--
(TIDECFUP)
esp++
M[ebp+9]=1
esp++
M[ebp+10]=M[ebp+3]
M[ebp+10]-=M[ebp+2]
CMP M[ebp+10], 26
JEQ CRVQYFPF
M[ebp+9]=0

(CRVQYFPF)
esp++
M[ebp+11]=-314
esp+=2
M[ebp+11]+=M[M[ebp+2]+5]
esp+=2
M[ebp+11]+=M[M[ebp+2]+6]
esp+=2
M[ebp+11]+=M[M[ebp+2]+13]
esp+=2
M[ebp+11]+=M[M[ebp+2]+15]
CMP M[ebp+11], 82
JEQ FLMJAMJX
M[ebp+9]=0
(FLMJAMJX)
esp-=9

esp+=1
M[ebp+11]=-243
esp+=2
M[ebp+11]+=M[M[ebp+2]+22]
esp+=2
M[ebp+11]+=M[M[ebp+2]+24]
esp+=2
M[ebp+11]+=M[M[ebp+2]+22]
CMP M[ebp+11], 21
JEQ TVUDBTFV
M[ebp+9]=0
(TVUDBTFV)
esp-=7

esp+=1
M[ebp+11]=-28
esp+=2
M[ebp+11]+=M[M[ebp+2]+1]
esp+=2
M[ebp+11]+=M[M[ebp+2]+11]
esp+=2
M[ebp+11]+=M[M[ebp+2]+17]
esp+=2
M[ebp+11]+=M[M[ebp+2]+3]
CMP M[ebp+11], 314
JEQ BDTYIIIE
M[ebp+9]=0
(BDTYIIIE)
esp-=9

esp+=1
M[ebp+11]=257
esp+=2
M[ebp+11]+=M[M[ebp+2]+20]
esp+=2
M[ebp+11]+=M[M[ebp+2]+7]
esp+=2
M[ebp+11]+=M[M[ebp+2]+10]
esp+=2
M[ebp+11]+=M[M[ebp+2]+24]
CMP M[ebp+11], 585
JEQ TXVRWFRC
M[ebp+9]=0
(TXVRWFRC)
esp-=9

esp+=1
M[ebp+11]=40
esp+=2
M[ebp+11]+=M[M[ebp+2]+4]
esp+=2
M[ebp+11]+=M[M[ebp+2]+25]
esp+=2
M[ebp+11]+=M[M[ebp+2]+21]
CMP M[ebp+11], 374
JEQ QDLKQPID
M[ebp+9]=0
(QDLKQPID)
esp-=7

esp+=1
M[ebp+11]=-151
esp+=2
M[ebp+11]+=M[M[ebp+2]+9]
esp+=2
M[ebp+11]+=M[M[ebp+2]+9]
esp+=2
M[ebp+11]+=M[M[ebp+2]+16]
esp+=2
M[ebp+11]+=M[M[ebp+2]+21]
CMP M[ebp+11], 239
JEQ ECAAQAPM
M[ebp+9]=0
(ECAAQAPM)
esp-=9

esp+=1
M[ebp+11]=-447
esp+=2
M[ebp+11]+=M[M[ebp+2]+1]
esp+=2
M[ebp+11]+=M[M[ebp+2]+21]
esp+=2
M[ebp+11]+=M[M[ebp+2]+8]
esp+=2
M[ebp+11]+=M[M[ebp+2]+8]
CMP M[ebp+11], -23
JEQ DDEFLGEE
M[ebp+9]=0
(DDEFLGEE)
esp-=9

esp+=1
M[ebp+11]=-14
esp+=2
M[ebp+11]+=M[M[ebp+2]+10]
esp+=2
M[ebp+11]+=M[M[ebp+2]+11]
esp+=2
M[ebp+11]+=M[M[ebp+2]+11]
CMP M[ebp+11], 149
JEQ EUPATHWJ
M[ebp+9]=0
(EUPATHWJ)
esp-=7

esp+=1
M[ebp+11]=248
esp+=2
M[ebp+11]+=M[M[ebp+2]+16]
esp+=2
M[ebp+11]+=M[M[ebp+2]+19]
esp+=2
M[ebp+11]+=M[M[ebp+2]+21]
esp+=2
M[ebp+11]+=M[M[ebp+2]+19]
CMP M[ebp+11], 656
JEQ KCOURWXQ
M[ebp+9]=0
(KCOURWXQ)
esp-=9

esp+=1
M[ebp+11]=-346
esp+=2
M[ebp+11]+=M[M[ebp+2]+12]
esp+=2
M[ebp+11]+=M[M[ebp+2]+22]
esp+=2
M[ebp+11]+=M[M[ebp+2]+0]
esp+=2
M[ebp+11]+=M[M[ebp+2]+4]
CMP M[ebp+11], -18
JEQ TYRDSGPV
M[ebp+9]=0
(TYRDSGPV)
esp-=9

esp+=1
M[ebp+11]=-403
esp+=2
M[ebp+11]+=M[M[ebp+2]+24]
esp+=2
M[ebp+11]+=M[M[ebp+2]+9]
esp+=2
M[ebp+11]+=M[M[ebp+2]+1]
CMP M[ebp+11], -97
JEQ DNVOUUNS
M[ebp+9]=0
(DNVOUUNS)
esp-=7

esp+=1
M[ebp+11]=69
esp+=2
M[ebp+11]+=M[M[ebp+2]+1]
esp+=2
M[ebp+11]+=M[M[ebp+2]+5]
esp+=2
M[ebp+11]+=M[M[ebp+2]+21]
esp+=2
M[ebp+11]+=M[M[ebp+2]+12]
CMP M[ebp+11], 465
JEQ JWTCDKMI
M[ebp+9]=0
(JWTCDKMI)
esp-=9

esp+=1
M[ebp+11]=8
esp+=2
M[ebp+11]+=M[M[ebp+2]+0]
esp+=2
M[ebp+11]+=M[M[ebp+2]+12]
esp+=2
M[ebp+11]+=M[M[ebp+2]+7]
CMP M[ebp+11], 246
JEQ MACXRUNE
M[ebp+9]=0
(MACXRUNE)
esp-=7

esp+=1
M[ebp+11]=-197
esp+=2
M[ebp+11]+=M[M[ebp+2]+15]
esp+=2
M[ebp+11]+=M[M[ebp+2]+18]
esp+=2
M[ebp+11]+=M[M[ebp+2]+15]
CMP M[ebp+11], 50
JEQ NYHFZQVD
M[ebp+9]=0
(NYHFZQVD)
esp-=7

esp+=1
M[ebp+11]=-139
esp+=2
M[ebp+11]+=M[M[ebp+2]+13]
esp+=2
M[ebp+11]+=M[M[ebp+2]+25]
esp+=2
M[ebp+11]+=M[M[ebp+2]+0]
CMP M[ebp+11], 164
JEQ ERSSFZKO
M[ebp+9]=0
(ERSSFZKO)
esp-=7

esp+=1
M[ebp+11]=442
esp+=2
M[ebp+11]+=M[M[ebp+2]+23]
esp+=2
M[ebp+11]+=M[M[ebp+2]+1]
esp+=2
M[ebp+11]+=M[M[ebp+2]+20]
CMP M[ebp+11], 692
JEQ WYRUIXCU
M[ebp+9]=0
(WYRUIXCU)
esp-=7

esp+=1
M[ebp+11]=-207
esp+=2
M[ebp+11]+=M[M[ebp+2]+3]
esp+=2
M[ebp+11]+=M[M[ebp+2]+23]
esp+=2
M[ebp+11]+=M[M[ebp+2]+8]
CMP M[ebp+11], 123
JEQ SFRDZZHM
M[ebp+9]=0
(SFRDZZHM)
esp-=7

esp+=1
M[ebp+11]=477
esp+=2
M[ebp+11]+=M[M[ebp+2]+18]
esp+=2
M[ebp+11]+=M[M[ebp+2]+3]
esp+=2
M[ebp+11]+=M[M[ebp+2]+19]
esp+=2
M[ebp+11]+=M[M[ebp+2]+24]
CMP M[ebp+11], 905
JEQ YOSYYHCX
M[ebp+9]=0
(YOSYYHCX)
esp-=9

esp+=1
M[ebp+11]=120
esp+=2
M[ebp+11]+=M[M[ebp+2]+20]
esp+=2
M[ebp+11]+=M[M[ebp+2]+15]
esp+=2
M[ebp+11]+=M[M[ebp+2]+15]
esp+=2
M[ebp+11]+=M[M[ebp+2]+22]
CMP M[ebp+11], 399
JEQ TOPYOUHE
M[ebp+9]=0
(TOPYOUHE)
esp-=9

esp+=1
M[ebp+11]=-368
esp+=2
M[ebp+11]+=M[M[ebp+2]+14]
esp+=2
M[ebp+11]+=M[M[ebp+2]+18]
esp+=2
M[ebp+11]+=M[M[ebp+2]+19]
esp+=2
M[ebp+11]+=M[M[ebp+2]+14]
CMP M[ebp+11], -71
JEQ SYYUQBOI
M[ebp+9]=0
(SYYUQBOI)
esp-=9

esp+=1
M[ebp+11]=436
esp+=2
M[ebp+11]+=M[M[ebp+2]+22]
esp+=2
M[ebp+11]+=M[M[ebp+2]+1]
esp+=2
M[ebp+11]+=M[M[ebp+2]+5]
esp+=2
M[ebp+11]+=M[M[ebp+2]+9]
CMP M[ebp+11], 826
JEQ AALUAMAS
M[ebp+9]=0
(AALUAMAS)
esp-=9

esp+=1
M[ebp+11]=-330
esp+=2
M[ebp+11]+=M[M[ebp+2]+12]
esp+=2
M[ebp+11]+=M[M[ebp+2]+17]
esp+=2
M[ebp+11]+=M[M[ebp+2]+3]
esp+=2
M[ebp+11]+=M[M[ebp+2]+18]
CMP M[ebp+11], 39
JEQ UTRTVNKO
M[ebp+9]=0
(UTRTVNKO)
esp-=9

esp+=1
M[ebp+11]=362
esp+=2
M[ebp+11]+=M[M[ebp+2]+11]
esp+=2
M[ebp+11]+=M[M[ebp+2]+12]
esp+=2
M[ebp+11]+=M[M[ebp+2]+3]
CMP M[ebp+11], 602
JEQ BZNJOUOA
M[ebp+9]=0
(BZNJOUOA)
esp-=7

esp+=1
M[ebp+11]=-456
esp+=2
M[ebp+11]+=M[M[ebp+2]+15]
esp+=2
M[ebp+11]+=M[M[ebp+2]+14]
esp+=2
M[ebp+11]+=M[M[ebp+2]+1]
CMP M[ebp+11], -234
JEQ NGVEHJGC
M[ebp+9]=0
(NGVEHJGC)
esp-=7

esp+=1
M[ebp+11]=458
esp+=2
M[ebp+11]+=M[M[ebp+2]+20]
esp+=2
M[ebp+11]+=M[M[ebp+2]+0]
esp+=2
M[ebp+11]+=M[M[ebp+2]+14]
esp+=2
M[ebp+11]+=M[M[ebp+2]+11]
CMP M[ebp+11], 673
JEQ ERWEYXXS
M[ebp+9]=0
(ERWEYXXS)
esp-=9

esp+=1
M[ebp+11]=307
esp+=2
M[ebp+11]+=M[M[ebp+2]+5]
esp+=2
M[ebp+11]+=M[M[ebp+2]+17]
esp+=2
M[ebp+11]+=M[M[ebp+2]+22]
CMP M[ebp+11], 587
JEQ KIGFVQTR
M[ebp+9]=0
(KIGFVQTR)
esp-=7

esp+=1
M[ebp+11]=-91
esp+=2
M[ebp+11]+=M[M[ebp+2]+18]
esp+=2
M[ebp+11]+=M[M[ebp+2]+9]
esp+=2
M[ebp+11]+=M[M[ebp+2]+12]
CMP M[ebp+11], 176
JEQ KBBYVJZD
M[ebp+9]=0
(KBBYVJZD)
esp-=7

esp+=1
M[ebp+11]=-42
esp+=2
M[ebp+11]+=M[M[ebp+2]+7]
esp+=2
M[ebp+11]+=M[M[ebp+2]+24]
esp+=2
M[ebp+11]+=M[M[ebp+2]+25]
CMP M[ebp+11], 292
JEQ QUHSXNUC
M[ebp+9]=0
(QUHSXNUC)
esp-=7

esp+=1
M[ebp+11]=-39
esp+=2
M[ebp+11]+=M[M[ebp+2]+16]
esp+=2
M[ebp+11]+=M[M[ebp+2]+20]
esp+=2
M[ebp+11]+=M[M[ebp+2]+7]
CMP M[ebp+11], 209
JEQ ZQAXHRKS
M[ebp+9]=0
(ZQAXHRKS)
esp-=7

esp+=1
M[ebp+11]=243
esp+=2
M[ebp+11]+=M[M[ebp+2]+15]
esp+=2
M[ebp+11]+=M[M[ebp+2]+23]
esp+=2
M[ebp+11]+=M[M[ebp+2]+17]
esp+=2
M[ebp+11]+=M[M[ebp+2]+17]
CMP M[ebp+11], 584
JEQ UQSPHLHR
M[ebp+9]=0
(UQSPHLHR)
esp-=9

esp+=1
M[ebp+11]=-437
esp+=2
M[ebp+11]+=M[M[ebp+2]+8]
esp+=2
M[ebp+11]+=M[M[ebp+2]+4]
esp+=2
M[ebp+11]+=M[M[ebp+2]+24]
esp+=2
M[ebp+11]+=M[M[ebp+2]+2]
CMP M[ebp+11], 9
JEQ MCQCMJGC
M[ebp+9]=0
(MCQCMJGC)
esp-=9

esp+=1
M[ebp+11]=284
esp+=2
M[ebp+11]+=M[M[ebp+2]+25]
esp+=2
M[ebp+11]+=M[M[ebp+2]+4]
esp+=2
M[ebp+11]+=M[M[ebp+2]+12]
esp+=2
M[ebp+11]+=M[M[ebp+2]+8]
CMP M[ebp+11], 710
JEQ XHUVVIRO
M[ebp+9]=0
(XHUVVIRO)
esp-=9

esp+=1
M[ebp+11]=154
esp+=2
M[ebp+11]+=M[M[ebp+2]+8]
esp+=2
M[ebp+11]+=M[M[ebp+2]+11]
esp+=2
M[ebp+11]+=M[M[ebp+2]+4]
esp+=2
M[ebp+11]+=M[M[ebp+2]+24]
CMP M[ebp+11], 540
JEQ TRGADQNX
M[ebp+9]=0
(TRGADQNX)
esp-=9

esp+=1
M[ebp+11]=369
esp+=2
M[ebp+11]+=M[M[ebp+2]+23]
esp+=2
M[ebp+11]+=M[M[ebp+2]+21]
esp+=2
M[ebp+11]+=M[M[ebp+2]+2]
esp+=2
M[ebp+11]+=M[M[ebp+2]+21]
CMP M[ebp+11], 776
JEQ HFHORIZY
M[ebp+9]=0
(HFHORIZY)
esp-=9

esp+=1
M[ebp+11]=221
esp+=2
M[ebp+11]+=M[M[ebp+2]+13]
esp+=2
M[ebp+11]+=M[M[ebp+2]+0]
esp+=2
M[ebp+11]+=M[M[ebp+2]+1]
esp+=2
M[ebp+11]+=M[M[ebp+2]+12]
CMP M[ebp+11], 573
JEQ LJUXSATQ
M[ebp+9]=0
(LJUXSATQ)
esp-=9

esp+=1
M[ebp+11]=11
esp+=2
M[ebp+11]+=M[M[ebp+2]+24]
esp+=2
M[ebp+11]+=M[M[ebp+2]+10]
esp+=2
M[ebp+11]+=M[M[ebp+2]+8]
esp+=2
M[ebp+11]+=M[M[ebp+2]+0]
CMP M[ebp+11], 372
JEQ CHFRQXFJ
M[ebp+9]=0
(CHFRQXFJ)
esp-=9

esp+=1
M[ebp+11]=339
esp+=2
M[ebp+11]+=M[M[ebp+2]+18]
esp+=2
M[ebp+11]+=M[M[ebp+2]+3]
esp+=2
M[ebp+11]+=M[M[ebp+2]+18]
CMP M[ebp+11], 644
JEQ IMDGWRDX
M[ebp+9]=0
(IMDGWRDX)
esp-=7

esp+=1
M[ebp+11]=434
esp+=2
M[ebp+11]+=M[M[ebp+2]+10]
esp+=2
M[ebp+11]+=M[M[ebp+2]+8]
esp+=2
M[ebp+11]+=M[M[ebp+2]+23]
CMP M[ebp+11], 716
JEQ WFFHNFZZ
M[ebp+9]=0
(WFFHNFZZ)
esp-=7

esp+=1
M[ebp+11]=-331
esp+=2
M[ebp+11]+=M[M[ebp+2]+21]
esp+=2
M[ebp+11]+=M[M[ebp+2]+6]
esp+=2
M[ebp+11]+=M[M[ebp+2]+16]
CMP M[ebp+11], -46
JEQ OUQBOKRQ
M[ebp+9]=0
(OUQBOKRQ)
esp-=7

esp+=1
M[ebp+11]=-84
esp+=2
M[ebp+11]+=M[M[ebp+2]+0]
esp+=2
M[ebp+11]+=M[M[ebp+2]+6]
esp+=2
M[ebp+11]+=M[M[ebp+2]+13]
CMP M[ebp+11], 179
JEQ LRHBIHEL
M[ebp+9]=0
(LRHBIHEL)
esp-=7

esp+=1
M[ebp+11]=2
esp+=2
M[ebp+11]+=M[M[ebp+2]+21]
esp+=2
M[ebp+11]+=M[M[ebp+2]+22]
esp+=2
M[ebp+11]+=M[M[ebp+2]+6]
esp+=2
M[ebp+11]+=M[M[ebp+2]+7]
CMP M[ebp+11], 356
JEQ NCRKTPIK
M[ebp+9]=0
(NCRKTPIK)
esp-=9

esp+=1
M[ebp+11]=-291
esp+=2
M[ebp+11]+=M[M[ebp+2]+19]
esp+=2
M[ebp+11]+=M[M[ebp+2]+5]
esp+=2
M[ebp+11]+=M[M[ebp+2]+9]
esp+=2
M[ebp+11]+=M[M[ebp+2]+18]
CMP M[ebp+11], 126
JEQ UHLHNFGC
M[ebp+9]=0
(UHLHNFGC)
esp-=9

esp+=1
M[ebp+11]=353
esp+=2
M[ebp+11]+=M[M[ebp+2]+9]
esp+=2
M[ebp+11]+=M[M[ebp+2]+14]
esp+=2
M[ebp+11]+=M[M[ebp+2]+9]
CMP M[ebp+11], 592
JEQ TRXHBJSN
M[ebp+9]=0
(TRXHBJSN)
esp-=7

esp+=1
M[ebp+11]=-393
esp+=2
M[ebp+11]+=M[M[ebp+2]+11]
esp+=2
M[ebp+11]+=M[M[ebp+2]+23]
esp+=2
M[ebp+11]+=M[M[ebp+2]+3]
esp+=2
M[ebp+11]+=M[M[ebp+2]+9]
CMP M[ebp+11], -34
JEQ BUIJCHUJ
M[ebp+9]=0
(BUIJCHUJ)
esp-=9

esp+=1
M[ebp+11]=-93
esp+=2
M[ebp+11]+=M[M[ebp+2]+7]
esp+=2
M[ebp+11]+=M[M[ebp+2]+16]
esp+=2
M[ebp+11]+=M[M[ebp+2]+18]
esp+=2
M[ebp+11]+=M[M[ebp+2]+6]
CMP M[ebp+11], 283
JEQ JGUXVWBJ
M[ebp+9]=0
(JGUXVWBJ)
esp-=9

esp+=1
M[ebp+11]=162
esp+=2
M[ebp+11]+=M[M[ebp+2]+13]
esp+=2
M[ebp+11]+=M[M[ebp+2]+24]
esp+=2
M[ebp+11]+=M[M[ebp+2]+25]
esp+=2
M[ebp+11]+=M[M[ebp+2]+8]
CMP M[ebp+11], 627
JEQ DGRLLRHZ
M[ebp+9]=0
(DGRLLRHZ)
esp-=9

esp+=1
M[ebp+11]=182
esp+=2
M[ebp+11]+=M[M[ebp+2]+6]
esp+=2
M[ebp+11]+=M[M[ebp+2]+14]
esp+=2
M[ebp+11]+=M[M[ebp+2]+4]
CMP M[ebp+11], 426
JEQ JFAEOTLJ
M[ebp+9]=0
(JFAEOTLJ)
esp-=7

esp+=1
M[ebp+11]=-99
esp+=2
M[ebp+11]+=M[M[ebp+2]+14]
esp+=2
M[ebp+11]+=M[M[ebp+2]+13]
esp+=2
M[ebp+11]+=M[M[ebp+2]+10]
CMP M[ebp+11], 129
JEQ IOTKVITZ
M[ebp+9]=0
(IOTKVITZ)
esp-=7

esp+=1
M[ebp+11]=148
esp+=2
M[ebp+11]+=M[M[ebp+2]+14]
esp+=2
M[ebp+11]+=M[M[ebp+2]+3]
esp+=2
M[ebp+11]+=M[M[ebp+2]+23]
esp+=2
M[ebp+11]+=M[M[ebp+2]+6]
CMP M[ebp+11], 498
JEQ IHQDXMHV
M[ebp+9]=0
(IHQDXMHV)
esp-=9

esp+=1
M[ebp+11]=-249
esp+=2
M[ebp+11]+=M[M[ebp+2]+25]
esp+=2
M[ebp+11]+=M[M[ebp+2]+22]
esp+=2
M[ebp+11]+=M[M[ebp+2]+22]
esp+=2
M[ebp+11]+=M[M[ebp+2]+2]
CMP M[ebp+11], 134
JEQ MYASJIRN
M[ebp+9]=0
(MYASJIRN)
esp-=9

esp+=1
M[ebp+11]=60
esp+=2
M[ebp+11]+=M[M[ebp+2]+16]
esp+=2
M[ebp+11]+=M[M[ebp+2]+19]
esp+=2
M[ebp+11]+=M[M[ebp+2]+14]
esp+=2
M[ebp+11]+=M[M[ebp+2]+14]
CMP M[ebp+11], 363
JEQ HSRVGXFO
M[ebp+9]=0
(HSRVGXFO)
esp-=9

esp+=1
M[ebp+11]=346
esp+=2
M[ebp+11]+=M[M[ebp+2]+22]
esp+=2
M[ebp+11]+=M[M[ebp+2]+13]
esp+=2
M[ebp+11]+=M[M[ebp+2]+14]
CMP M[ebp+11], 582
JEQ LSSBVGAD
M[ebp+9]=0
(LSSBVGAD)
esp-=7

esp+=1
M[ebp+11]=144
esp+=2
M[ebp+11]+=M[M[ebp+2]+3]
esp+=2
M[ebp+11]+=M[M[ebp+2]+16]
esp+=2
M[ebp+11]+=M[M[ebp+2]+16]
esp+=2
M[ebp+11]+=M[M[ebp+2]+18]
CMP M[ebp+11], 556
JEQ ILBFRIVD
M[ebp+9]=0
(ILBFRIVD)
esp-=9

esp+=1
M[ebp+11]=-79
esp+=2
M[ebp+11]+=M[M[ebp+2]+4]
esp+=2
M[ebp+11]+=M[M[ebp+2]+15]
esp+=2
M[ebp+11]+=M[M[ebp+2]+9]
CMP M[ebp+11], 202
JEQ AQWKYOXF
M[ebp+9]=0
(AQWKYOXF)
esp-=7

esp+=1
M[ebp+11]=-60
esp+=2
M[ebp+11]+=M[M[ebp+2]+17]
esp+=2
M[ebp+11]+=M[M[ebp+2]+15]
esp+=2
M[ebp+11]+=M[M[ebp+2]+11]
CMP M[ebp+11], 146
JEQ HJVHGVVS
M[ebp+9]=0
(HJVHGVVS)
esp-=7

esp+=1
M[ebp+11]=-229
esp+=2
M[ebp+11]+=M[M[ebp+2]+21]
esp+=2
M[ebp+11]+=M[M[ebp+2]+8]
esp+=2
M[ebp+11]+=M[M[ebp+2]+10]
CMP M[ebp+11], 51
JEQ HNTDTNAB
M[ebp+9]=0
(HNTDTNAB)
esp-=7

esp+=1
M[ebp+11]=472
esp+=2
M[ebp+11]+=M[M[ebp+2]+5]
esp+=2
M[ebp+11]+=M[M[ebp+2]+16]
esp+=2
M[ebp+11]+=M[M[ebp+2]+13]
CMP M[ebp+11], 808
JEQ SCBJERNE
M[ebp+9]=0
(SCBJERNE)
esp-=7

esp+=1
M[ebp+11]=325
esp+=2
M[ebp+11]+=M[M[ebp+2]+19]
esp+=2
M[ebp+11]+=M[M[ebp+2]+1]
esp+=2
M[ebp+11]+=M[M[ebp+2]+2]
CMP M[ebp+11], 634
JEQ HEJASAAT
M[ebp+9]=0
(HEJASAAT)
esp-=7

esp+=1
M[ebp+11]=393
esp+=2
M[ebp+11]+=M[M[ebp+2]+19]
esp+=2
M[ebp+11]+=M[M[ebp+2]+2]
esp+=2
M[ebp+11]+=M[M[ebp+2]+20]
esp+=2
M[ebp+11]+=M[M[ebp+2]+0]
CMP M[ebp+11], 723
JEQ JVAKKPCS
M[ebp+9]=0
(JVAKKPCS)
esp-=9

esp+=1
M[ebp+11]=158
esp+=2
M[ebp+11]+=M[M[ebp+2]+11]
esp+=2
M[ebp+11]+=M[M[ebp+2]+20]
esp+=2
M[ebp+11]+=M[M[ebp+2]+2]
esp+=2
M[ebp+11]+=M[M[ebp+2]+6]
CMP M[ebp+11], 451
JEQ DPPXXQSP
M[ebp+9]=0
(DPPXXQSP)
esp-=9

esp+=1
M[ebp+11]=-389
esp+=2
M[ebp+11]+=M[M[ebp+2]+6]
esp+=2
M[ebp+11]+=M[M[ebp+2]+25]
esp+=2
M[ebp+11]+=M[M[ebp+2]+7]
esp+=2
M[ebp+11]+=M[M[ebp+2]+13]
CMP M[ebp+11], 28
JEQ SUTQFAVM
M[ebp+9]=0
(SUTQFAVM)
esp-=9

esp+=1
M[ebp+11]=-289
esp+=2
M[ebp+11]+=M[M[ebp+2]+7]
esp+=2
M[ebp+11]+=M[M[ebp+2]+8]
esp+=2
M[ebp+11]+=M[M[ebp+2]+24]
CMP M[ebp+11], 34
JEQ EENRENKI
M[ebp+9]=0
(EENRENKI)
esp-=7

esp+=1
M[ebp+11]=-290
esp+=2
M[ebp+11]+=M[M[ebp+2]+2]
esp+=2
M[ebp+11]+=M[M[ebp+2]+10]
esp+=2
M[ebp+11]+=M[M[ebp+2]+5]
esp+=2
M[ebp+11]+=M[M[ebp+2]+12]
CMP M[ebp+11], 85
JEQ CFSNVOZY
M[ebp+9]=0
(CFSNVOZY)
esp-=9

esp+=1
M[ebp+11]=141
esp+=2
M[ebp+11]+=M[M[ebp+2]+23]
esp+=2
M[ebp+11]+=M[M[ebp+2]+2]
esp+=2
M[ebp+11]+=M[M[ebp+2]+12]
CMP M[ebp+11], 427
JEQ DOPUECEQ
M[ebp+9]=0
(DOPUECEQ)
esp-=7

esp+=1
M[ebp+11]=406
esp+=2
M[ebp+11]+=M[M[ebp+2]+6]
esp+=2
M[ebp+11]+=M[M[ebp+2]+0]
esp+=2
M[ebp+11]+=M[M[ebp+2]+4]
CMP M[ebp+11], 667
JEQ QXHVYWCX
M[ebp+9]=0
(QXHVYWCX)
esp-=7

esp+=1
M[ebp+11]=-458
esp+=2
M[ebp+11]+=M[M[ebp+2]+8]
esp+=2
M[ebp+11]+=M[M[ebp+2]+20]
esp+=2
M[ebp+11]+=M[M[ebp+2]+19]
CMP M[ebp+11], -188
JEQ UPOTWTBT
M[ebp+9]=0
(UPOTWTBT)
esp-=7

esp+=1
M[ebp+11]=244
esp+=2
M[ebp+11]+=M[M[ebp+2]+9]
esp+=2
M[ebp+11]+=M[M[ebp+2]+4]
esp+=2
M[ebp+11]+=M[M[ebp+2]+6]
CMP M[ebp+11], 534
JEQ YNGUBAMY
M[ebp+9]=0
(YNGUBAMY)
esp-=7

esp+=1
M[ebp+11]=-228
esp+=2
M[ebp+11]+=M[M[ebp+2]+3]
esp+=2
M[ebp+11]+=M[M[ebp+2]+19]
esp+=2
M[ebp+11]+=M[M[ebp+2]+18]
CMP M[ebp+11], 86
JEQ PWTNTXYJ
M[ebp+9]=0
(PWTNTXYJ)
esp-=7

esp+=1
M[ebp+11]=209
esp+=2
M[ebp+11]+=M[M[ebp+2]+24]
esp+=2
M[ebp+11]+=M[M[ebp+2]+18]
esp+=2
M[ebp+11]+=M[M[ebp+2]+6]
esp+=2
M[ebp+11]+=M[M[ebp+2]+5]
CMP M[ebp+11], 626
JEQ OGZGWBDQ
M[ebp+9]=0
(OGZGWBDQ)
esp-=9

esp+=1
M[ebp+11]=294
esp+=2
M[ebp+11]+=M[M[ebp+2]+4]
esp+=2
M[ebp+11]+=M[M[ebp+2]+21]
esp+=2
M[ebp+11]+=M[M[ebp+2]+25]
CMP M[ebp+11], 628
JEQ LSJCLEWE
M[ebp+9]=0
(LSJCLEWE)
esp-=7

esp+=1
M[ebp+11]=-150
esp+=2
M[ebp+11]+=M[M[ebp+2]+17]
esp+=2
M[ebp+11]+=M[M[ebp+2]+10]
esp+=2
M[ebp+11]+=M[M[ebp+2]+15]
esp+=2
M[ebp+11]+=M[M[ebp+2]+21]
CMP M[ebp+11], 174
JEQ RWSNWFLL
M[ebp+9]=0
(RWSNWFLL)
esp-=9

esp+=1
M[ebp+11]=-31
esp+=2
M[ebp+11]+=M[M[ebp+2]+2]
esp+=2
M[ebp+11]+=M[M[ebp+2]+13]
esp+=2
M[ebp+11]+=M[M[ebp+2]+5]
esp+=2
M[ebp+11]+=M[M[ebp+2]+2]
CMP M[ebp+11], 420
JEQ VYTOQSSY
M[ebp+9]=0
(VYTOQSSY)
esp-=9

esp+=1
M[ebp+11]=-101
esp+=2
M[ebp+11]+=M[M[ebp+2]+10]
esp+=2
M[ebp+11]+=M[M[ebp+2]+17]
esp+=2
M[ebp+11]+=M[M[ebp+2]+23]
esp+=2
M[ebp+11]+=M[M[ebp+2]+5]
CMP M[ebp+11], 272
JEQ SRFOTJZZ
M[ebp+9]=0
(SRFOTJZZ)
esp-=9

esp+=1
M[ebp+11]=-194
esp+=2
M[ebp+11]+=M[M[ebp+2]+0]
esp+=2
M[ebp+11]+=M[M[ebp+2]+7]
esp+=2
M[ebp+11]+=M[M[ebp+2]+0]
CMP M[ebp+11], 33
JEQ VJBAIXYU
M[ebp+9]=0
(VJBAIXYU)
esp-=7

esp+=1
M[ebp+11]=-319
esp+=2
M[ebp+11]+=M[M[ebp+2]+12]
esp+=2
M[ebp+11]+=M[M[ebp+2]+7]
esp+=2
M[ebp+11]+=M[M[ebp+2]+17]
CMP M[ebp+11], -65
JEQ URHQQMWF
M[ebp+9]=0
(URHQQMWF)
esp-=7

esp+=1
M[ebp+11]=7
esp+=2
M[ebp+11]+=M[M[ebp+2]+25]
esp+=2
M[ebp+11]+=M[M[ebp+2]+2]
esp+=2
M[ebp+11]+=M[M[ebp+2]+20]
esp+=2
M[ebp+11]+=M[M[ebp+2]+17]
CMP M[ebp+11], 374
JEQ FQUVCMOV
M[ebp+9]=0
(FQUVCMOV)
esp-=9

esp+=1
M[ebp+11]=-341
esp+=2
M[ebp+11]+=M[M[ebp+2]+17]
esp+=2
M[ebp+11]+=M[M[ebp+2]+12]
esp+=2
M[ebp+11]+=M[M[ebp+2]+11]
esp+=2
M[ebp+11]+=M[M[ebp+2]+11]
CMP M[ebp+11], -86
JEQ YTJRWJQM
M[ebp+9]=0
(YTJRWJQM)
esp-=9

esp+=1
M[ebp+11]=-383
esp+=2
M[ebp+11]+=M[M[ebp+2]+2]
esp+=2
M[ebp+11]+=M[M[ebp+2]+5]
esp+=2
M[ebp+11]+=M[M[ebp+2]+24]
CMP M[ebp+11], -38
JEQ MSGVJFPD
M[ebp+9]=0
(MSGVJFPD)
esp-=7

esp+=1
M[esp] = WQUGDLMD
esp+=2
M[ARG]=esp+1
M[M[ARG]] = 10
jmp Array_Alloc
(WQUGDLMD)
M[esp] = M[esp+1]
esp++
M[ebp+11]=M[ebp+12]
M[15633]=ebp
@9
D=A
@15633
AM=M+D
D=M
@15620
AMD=D-1
JNE BBSEHHTG

# "Success!"
M[15634]=ebp+11
M[15643]=M[M[15634]]
M[M[15643]] = 83
M[15643]++
M[M[15643]] = 117
M[15643]++
M[M[15643]] = 99
M[15643]++
M[M[15643]] = 99
M[15643]++
M[M[15643]] = 101
M[15643]++
M[M[15643]] = 115
M[15643]++
M[M[15643]] = 115
M[15643]++
M[M[15643]] = 33
@15643
AM=M+1
M=0
(BBSEHHTG)
M[15635]=ebp
@9
D=A
@15635
AM=M+D
D=M
@15620
AM=D
JNE ADSRGCDN

# "Fail!"
M[15636]=ebp+11
M[15643]=M[M[15636]]
M[M[15643]] = 70
M[15643]++
M[M[15643]] = 97
M[15643]++
M[M[15643]] = 105
M[15643]++
M[M[15643]] = 108
M[15643]++
M[M[15643]] = 33
@15643
AM=M+1
M=0

(ADSRGCDN)
M[esp] = PKCYPMCF
esp+=2
M[ARG]=esp+1
M[15633]=ebp
@11
D=A
@15633
AM=M+D
D=M
@ARG
A=M
M=D
jmp Output_PrintString
(PKCYPMCF)
M[esp] = M[esp+1]
esp++
(CRMACYDY)
jmp CRMACYDY
(MGCMJPAA)
CMP M[ebp+9], 10
JNE ZQWHXPHY

# newline - print it, and then process flag
M[esp] = SZPTCNAR
esp+=2
M[ARG]=esp+1
M[M[ARG]]=M[ebp+9]
jmp Output_PrintChar
(SZPTCNAR)
M[esp] = M[esp+1]
esp--
jmp TIDECFUP

# not newline - check character
(ZQWHXPHY)
M[ebp+4]=1
CMP M[ebp+9], 140
JNE XDQHPNML
    # 140 = esc - toggle shift state
    M[ebp+8]=1
    M[ebp+8]-=M[ebp+7]
    M[ebp+7]=M[ebp+8]
(XDQHPNML)
CMP M[ebp+9], 140
JEQ ETGBSDZL

CMP M[ebp+7], 1
JNE UWNRMVKY
    # Handle shifted keys
    M[ebp+8]=M[ebp+9]
    CMP M[ebp+9], 65
    JLT VUMRHMJZ
    CMP M[ebp+9], 90
    JGT PTGYGSEF
    M[ebp+8]+=32
    (PTGYGSEF)
    (VUMRHMJZ)
    CMP M[ebp+9], 97
    JLT MEGYIFDW
    CMP M[ebp+9], 122
    JGT VRIHGSAV
    M[ebp+8]-=32
    (VRIHGSAV)
    (MEGYIFDW)
    CMP M[ebp+9], 91
    JNE GMNOZQHJ
    M[ebp+8] = 123
    (GMNOZQHJ)
    M[15635]=ebp+9
    CMP M[M[15635]], 93
    JNE ENBLAAKG
    M[15636]=ebp+8
    M[M[15636]] = 125
    (ENBLAAKG)
    M[15633]=ebp+9
    CMP M[M[15633]], 49
    JNE EQEGQCXG
    M[15634]=ebp+8
    M[M[15634]] = 33
    (EQEGQCXG)
    M[15635]=ebp+9
    CMP M[M[15635]], 50
    JNE NFOUSIJZ
    M[15636]=ebp+8
    M[M[15636]] = 64
    (NFOUSIJZ)
    M[15633]=ebp+9
    CMP M[M[15633]], 51
    JNE VRHPBOSG
    M[15634]=ebp+8
    M[M[15634]] = 35
    (VRHPBOSG)
    M[15635]=ebp+9
    CMP M[M[15635]], 52
    JNE VULWOVCM
    M[15636]=ebp+8
    M[M[15636]] = 36
    (VULWOVCM)
    M[15633]=ebp+9
    CMP M[M[15633]], 53
    JNE GATQWLXK
    M[15634]=ebp+8
    M[M[15634]] = 37
    (GATQWLXK)
    M[15635]=ebp+9
    CMP M[M[15635]], 54
    JNE QFYJOCCD
    M[15636]=ebp+8
    M[M[15636]] = 94
    (QFYJOCCD)
    M[15633]=ebp+9
    CMP M[M[15633]], 55
    JNE TJTUSLBO
    M[15634]=ebp+8
    M[M[15634]] = 38
    (TJTUSLBO)
    M[15635]=ebp+9
    CMP M[M[15635]], 56
    JNE ZMENCGAI
    M[15636]=ebp+8
    M[M[15636]] = 42
    (ZMENCGAI)
    M[15633]=ebp+9
    CMP M[M[15633]], 57
    JNE BOTYZQCQ
    M[15634]=ebp+8
    M[M[15634]] = 40
    (BOTYZQCQ)
    M[15635]=ebp+9
    CMP M[M[15635]], 48
    JNE QUTEWWCP
    M[15636]=ebp+8
    M[M[15636]] = 41
    (QUTEWWCP)
    M[15633]=ebp+9
    CMP M[M[15633]], 45
    JNE ZVESGFAG
    M[15634]=ebp+8
    M[M[15634]] = 95
    (ZVESGFAG)
    M[15635]=ebp+9
    CMP M[M[15635]], 61
    JNE MEUOFPRA
    M[15636]=ebp+8
    M[M[15636]] = 43
    (MEUOFPRA)
    M[15633]=ebp+8
    M[15634]=ebp+9
    M[M[15634]]=M[M[15633]]
(UWNRMVKY)
CMP M[ebp+9], 129
JNE DLSDVUNG
    CMP M[ebp+3], M[ebp+2]
    JLE JHEGXGWX
    M[15639]-=8
    M[esp] = BUJCAKIG
    esp+=2
    M[ARG]=esp+1
    M[M[ARG]] = 32
    jmp Output_PrintChar
    (BUJCAKIG)
    M[esp] = M[esp+1]
    esp++
    M[15639]-=8
    M[ebp+3]--
    esp--
    (JHEGXGWX)
(DLSDVUNG)
CMP M[ebp+9], 129
JEQ IXOOGFIJ
    M[esp] = KAGAPUGZ
    esp+=2
    M[ARG]=esp+1
    M[M[ARG]]=ebp+9
    jmp Output_PrintChar
    (KAGAPUGZ)
    M[esp] = M[esp+1]
    esp++

    M[M[ebp+3]]=M[ebp+9]
    M[ebp+3]++
    esp--
(IXOOGFIJ)
(ETGBSDZL)
(SWCGUHJY)
(RNOBKUHW)
M[15642] = 0
esp--
jmp Loop
