import subprocess
import re
import os
import mmap
import sys
import pexpect

p = pexpect.spawn('./camlfwrun -s 104.197.7.111 -p 1212 bytecode')
p.logfile_read = sys.stdout
p.expect('Path?')

maps = open('/proc/%d/maps' % p.pid, 'r')
for line in maps:
    if '[heap]' in line:
        addrs, prot, offs, dev, ino, name = line.split()
        start, end = [int(x, 16) for x in addrs.split('-')]
        heapbase = start
        heapsize = end - start

memf = open('/proc/%d/mem' % p.pid, 'rb')
memf.seek(heapbase)
heap = memf.read(heapsize)

chunks = re.findall('\0\0\0\0((?:[\1\3]\0\0\0){1024})', heap)
vwalls, hwalls, mask = chunks

maze = [['|']+[' ']*49+['|'] for _ in xrange(26)]
maze[0] = '.@' + '._'*24 + '|'
for y in xrange(25):
    for x in xrange(25):
        idx = (y*25+x)*4
        if hwalls[idx] == '\x01':
            maze[y+1][x*2+1:x*2+3] = '_.'
        if vwalls[idx] == '\x01':
            maze[y+1][(x+1)*2] = '|'
for row in maze:
    print ''.join(row)

seen = set()
def solve(x, y):
    if x == 24 and y == 25:
        return 'd'
    if (x,y) in seen:
        return

    print x, y
    possible = []
    if maze[y][x*2+1] != '_':
        possible.append(('d', x, y+1))
    if x > 0 and maze[y][x*2] != '|':
        possible.append(('l', x-1, y))
    if maze[y][x*2+2] != '|':
        possible.append(('r', x+1, y))
    if y > 0 and maze[y-1][x*2+1] != '_':
        possible.append(('u', x, y-1))

    seen.add((x, y))
    for d, xx, yy in possible:
        res = solve(xx, yy)
        if res:
            maze[y][x*2+1] = '#'
            return d + res

    return None

soln = 'd' + solve(0, 1)
print soln
for row in maze:
    print ''.join(row)

p.send(soln + '\n')
p.interact()

# flag = BCTF{meowmeowmeowilikeperfectmaze}
