#!/usr/bin/python

from sympy.solvers import solve
from sympy import Symbol

def partial_quotiens(x, y):
        pq = []
        while x != 1:
                pq.append(x / y)
                a = y
                b = x % y
                x = a
                y = b
        #print pq
        return pq

def rational(pq):
        i = len(pq) - 1
        num = pq[i]
        denom = 1
        while i > 0:
                i -= 1
                a = (pq[i] * num) + denom
                b = num
                num = a
                denom = b
        #print (num, denom)
        return (num, denom)

def convergents(pq):
        c = []
        for i in range(1, len(pq)):
                c.append(rational(pq[0:i]))
        #print c
        return c

def phiN(e, d, k):
        return ((e * d) - 1) / k

# e = 17993
# n = 90581
# wiener_attack(e, n) --> p =  239, q =  379


e = 0x0285f8d4fe29ce11605edf221868937c1b70ae376e34d67f9bb78c29a2d79ca46a60ea02a70fdb40e805b5d854255968b2b1f043963dcd61714ce4fc5c70ecc4d756ad1685d661db39d15a801d1c382ed97a048f0f85d909c811691d3ffe262eb70ccd1fa7dba1aa79139f21c14b3dfe95340491cff3a5a6ae9604329578db9f5bcc192e16aa62f687a8038e60c01518f8ccaa0befe569dadae8e49310a7a3c3bddcf637fc82e5340bef4105b533b6a531895650b2efa337d94c7a76447767b5129a04bcf3cd95bb60f6bfd1a12658530124ad8c6fd71652b8e0eb482fcc475043b410dfc4fe5fbc6bda08ca61244284a4ab5b311bc669df0c753526a79c1a57
n = 0x02aeb637f6152afd4fb3a2dd165aec9d5b45e70d2b82e78a353f7a1751859d196f56cb6d11700195f1069a73d9e5710950b814229ab4c5549383c2c87e0cd97f904748a1302400dc76b42591da17dabaf946aaaf1640f1327af16be45b8830603947a9c3309ca4d6cc9f1a2bcfdacf285fbc2f730e515ae1d93591ccd98f5c4674ec4a5859264700f700a4f4dcf7c3c35bbc579f6ebf80da33c6c11f68655092bbe670d5225b8e571d596fe426db59a6a05aaf77b3917448b2cfbcb3bd647b46772b13133fc68ffabcb3752372b949a3704b8596df4a44f085393ee2bf80f8f393719ed94ab348852f6a5e0c493efa32da5bf601063a033beaf73ba47d8205db


N= """03:67:19:8d:6b:56:14:e9:58:13:ad:d8:f2:2a:47:    17:bc:72:be:1e:ab:d9:33:d1:b8:69:44:fd:b7:    5b:    8e:d2:30:be:62:d7:d1:b6:9d:22:20:95:c1:28:c8:    6f:82:01:2e:cb:11:61:91:fd:9d:01:8a:6d:02:   f8:    4d:b2:7b:c5:1a:21:30:7d:c8:6f:4b:f7:71:c6:91:    c1:43:e5:ab:e5:49:b5:bd:2d:6e:b1:a2:1f:d6:   27:    0e:7e:1b:48:fe:06:11:fb:b2:e1:b0:b3:52:4e:6f:    4d:e8:b4:e4:a3:45:da:44:a1:3d:e8:25:b7:26:   08:    db:6c:7c:4a:40:b7:82:66:e6:c8:7b:bf:de:f6:b4:    83:81:d4:9c:45:07:a5:8b:cd:47:b7:6d:64:b4:   59:    08:b1:58:bd:7e:bc:4d:ac:b0:b1:cf:d6:c2:c1:95:    74:f4:0e:b2:ef:d0:e9:e1:0d:c7:00:5c:ad:39:   bc:    af:52:b9:ea:c3:87:33:68:d6:90:31:c5:e7:24:68:    4a:44:f0:68:ef:d1:d3:dc:09:6d:9b:5d:64:11:   e5:    8b:de:e4:3e:46:b9:9a:0d:04:94:b9:db:28:19:5a:    f9:01:af:f1:30:d4:a6:e2:03:da:d0:8d:a5:7f:   a7:    e4:02:62:a5:ba:db:2a:32:3e:da:28:b4:46:96:ab:    30:5d"""
N= N.replace(":","").replace('\n','').replace('\t','').replace(' ','')
N= "0x" + N
N= eval(N)

e="""
    00:f3:95:9d:97:8e:02:eb:9f:06:de:f3:f3:35:d8:
    f8:af:d7:60:99:51:dd:ac:60:b7:14:b6:c2:2a:f0:
    fa:91:2f:21:0b:34:20:6b:d2:4a:96:01:c7:8d:f4:
    a0:27:5f:10:7f:d3:ab:55:2d:95:05:7e:b9:34:e7:
    1b:dd:cd:70:45:c2:4b:18:58:7b:8c:8f:cf:5a:dd:
    4c:5d:83:f0:c7:7c:94:dc:9c:50:cb:e4:38:e2:b6:
    7b:af:d3:16:33:b6:aa:f1:78:1d:90:c3:ad:6f:03:
    d0:37:b3:32:18:01:b2:35:46:d4:83:e6:7e:26:06:
    7f:7b:22:34:7d:db:c0:c2:d5:92:ce:81:4c:bf:5d:
    fc:cc:14:14:37:f1:4e:0b:39:90:f8:80:61:e5:f0:
    ba:e5:f0:1e:3f:a7:0d:b0:e9:60:5e:7c:fd:57:5e:
    9c:81:ef:ee:c5:29:c3:3f:d9:03:7a:20:fd:8a:cd:
    51:3a:c9:63:77:68:31:3e:63:f9:83:8a:e3:51:1c:
    dd:0a:9a:2b:51:6f:21:48:c8:d4:75:a3:60:a0:63:
    59:44:97:39:ee:cd:25:1a:bb:42:b0:14:57:3e:43:
    9f:2f:a4:57:35:57:b2:56:99:ff:c1:1e:63:1c:e8:
    ee:97:5a:86:e7:e2:72:bc:f5:f7:6a:93:45:03:48:
    fe:3f"""
e = e.replace(":","").replace('\n','').replace('\t','').replace(' ','')
e = "0x" + e
e = eval(e)

n=N

print e
print '_------_'
print n

#e = 17993
#n = 90581
# wiener_attack(e, n) --> p =  239, q =  379

pq = partial_quotiens(e, n)
c = convergents(pq)
x = Symbol('x')
for (k, d) in c:
        if k != 0:
                y = n - phiN(e, d, k) + 1
                roots = solve(x**2 - y*x + n, x)
                if len(roots) == 2:
                        p = roots[0]
                        q = roots[1]
                        if p * q == n:
                                print 'p = ', p
                                print 'q = ', q
                                break
