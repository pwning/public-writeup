import sys
from socket import *
import re
import ast
import math

TARGET = ('104.197.7.111', 13135)

s = socket()
s.connect(TARGET)

def rd(*suffixes):
    out = ''
    while 1:
        x = s.recv(1)
        if not x:
            raise EOFError()
        sys.stdout.write(x)
        sys.stdout.flush()
        out += x

        for suffix in suffixes:
            if out.endswith(suffix):
                break
        else:
            continue
        break
    return out

def pr(x):
    s.send(x+'\n')
    print "<%s" % x

# Integers
for i in xrange(10):
    qs = re.findall(r'Is ([\d\.+/*()-]+) an integer or not', rd(': '))
    if qs:    
        val = eval(qs[0], {'__builtins__': None})
        pr('yes' if val == math.floor(val) else 'no')
    else:
        pr('no')

def read_problem():
    txt = rd('Answer: ')
    desc = re.findall(r'Description: (.+)\n', txt)[0]
    start = re.findall(r'The sequence starts with: (.+)\n', txt)
    if start:
        start = start[0]
    else:
        start = ''
    n = int(re.findall(r'n = (\d+),', txt)[0])
    return desc, start, n

# Primes (A000040)
desc, start, n = read_problem()
primes = open('primes.txt').read().strip().split()
pr(primes[n-1])

# Fibonacci numbers (A000045)
desc, start, n = read_problem()
a,b = 0, 1
for i in xrange(n):
    a,b = b,a+b
pr(str(a))

# Number of unlabeled trees (A000055)
desc, start, n = read_problem()
from A000055 import A000055
pr(str(A000055[n]))

# Miscellaneous OEIS sequences
import gzip
import collections
names = collections.defaultdict(list)
with gzip.open('names.gz') as f:
    for row in f:
        row = row.strip()
        if not row or row.startswith('#'):
            continue
        num, name = row.split(' ', 1)
        names[name].append(num)

seqs = {}
with gzip.open('stripped.gz') as f:
    for row in f:
        row = row.strip()
        if not row or row.startswith('#'):
            continue
        num, seq = row.split(' ', 1)
        seqs[num] = seq.strip(',')

import urllib2

def solve_oeis():
    desc, start, n = read_problem()
    desc = desc.strip()
    Anums = names[desc]
    if len(Anums) > 1:
        for num in Anums:
            if seqs[num].startswith(start):
                Anum = num
                print "<Disambiguated to %s>" % Anum
                break
        else:
            print "Can't disambiguate..."
    else:
        Anum = Anums[0]
        print "<Sequence %s>" % Anum
    answer = None
    try:
        biglist = urllib2.urlopen('https://oeis.org/%s/b%s.txt' % (Anum, Anum[1:]))
        for row in biglist:
            row = row.strip()
            if row.startswith('#') or not row:
                continue
            a,b = row.split()
            if int(a) == n:
                answer = b
                break
    except urllib2.URLError as e:
        print "<Failed to obtain full list: %s>" % e

    pr(answer)

for i in xrange(32):
    solve_oeis()

# "The Prime Numbers Revenge"
desc, start, n = read_problem()
conn = urllib2.urlopen('https://primes.utm.edu/nthprime/index.php', data='n=%s' % n)
n_fmt = '{0:,}'.format(n)
answer = re.findall(r'The %s.. prime is ([\d,]+)\.' % n_fmt, conn.read())
pr(answer[0].replace(',', ''))

# Catalan numbers
desc, start, n = read_problem()
import catalan
sys.setrecursionlimit(100000)
pr(str(catalan.catR2(n)))

# Number of sets of rooted connected graphs where every block is a complete graph (A035052)
desc, start, n = read_problem()
from A035052 import A035052
pr(str(A035052[n]))

# Shapes of height-balanced AVL trees with n nodes (A006265)
desc, start, n = read_problem()
from A006265 import A006265_1000
pr(str(A006265_1000[n-1000]))

# Partition numbers modulo 1000000007
desc, start, n = read_problem()
# We're just going to ask you to run Mod[PartitionsP[n], 1000000007] in Mathematica and paste the result here.
s.settimeout(0.3)
while 1:
    while 1:
        try:
            bit = s.recv(4096)
            sys.stdout.write(bit)
        except timeout:
            break

    pr(raw_input()+'\n')

# flag = BCTF{Y0u_h4ve_m0ar_7ermz_than_205}
