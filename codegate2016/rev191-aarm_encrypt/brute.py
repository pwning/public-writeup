import subprocess
import re
import collections

target = 'bcqai83,/0h`vvh_monqu"kglgh_soh13dhr/'

rmap = collections.defaultdict(list)
for c in map(chr, range(32, 127)):
    print "progress: %d" % ord(c)
    t = subprocess.check_output(['qemu-aarch64-static', './f0c2d56c85544b0788e5cb266b2c8be8', '1406730800', c * len(target)])
    out = re.findall(r'BLuKJ([\w\W]+)duquu', t)[0]

    for i, n in enumerate(out):
        rmap[i, n].append(c)

final = []
for i, n in enumerate(target):
    final.append(rmap[i, n])

print final

# aarch64... but almost like arm 32bit.
