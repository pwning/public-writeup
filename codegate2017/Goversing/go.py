#!/usr/bin/env python2.7
import re
from subprocess import Popen, PIPE

#
# prev_max isn't that necessary, it was just left over from when I
# still didn't have this script right and it would make false
# progress with wrong characters.
#

username = ''
prev_max = 0
while True:
  found = []
  for i in range(33, 127):
    c = chr(i)
    with open('/tmp/mytmpfile', 'w') as f:
      f.write('''1
%s
password
2
3
3
3
3
''' % (username+c).ljust(8, 'q'))  # username length is 8
    p = Popen(('gdb','./Goversing'), stdin=PIPE, stderr=PIPE, stdout=PIPE)
    out, err = p.communicate('''break *0x40207B if $dl != $cl
commands
print $rdi
set confirm off
quit
end
run < /tmp/mytmpfile
''')
    if 'Wrong Input.' in out:
      continue
    try:
      # Extract $rdi from the gdb output, which is the loop counter.
      found.append((int(re.search(r'\n\$1 = ([0-9]+)\n', out).group(1)), c))
    except:
      # Was never true that $dl != $cl, great!
      found.append((999, c))
      continue
  n, c = max(found)
  if n > prev_max:
    prev_max = n
    username += c
  else:
    break
  print n, sorted(found)[-2][0],
  print username

print '-------'
print username

password = ""
prev_max = 0
while True:
  found = []
  for i in range(33, 127):
    c = chr(i)
    with open('/tmp/mytmpfile', 'w') as f:
      f.write('''1
'''+username+'''
%s
2
3
3
3
3
''' % (password+c).ljust(0x1d, 'x'))  # password length is 29
    p = Popen(('gdb','./Goversing'), stdin=PIPE, stderr=PIPE, stdout=PIPE)
    out, err = p.communicate('''break *0x40214C if $dl != $r8l
commands
print $rdi
set confirm off
quit
end
run < /tmp/mytmpfile
''')
    if 'Wrong Input.' in out:
      continue
    try:
      found.append((int(re.search(r'\n\$1 = ([0-9]+)\n', out).group(1)), c))
    except:
      found.append((999, c))
      continue
  n, c = max(found)
  if n > prev_max:
    prev_max = n
    password += c
  else:
    break
  print n, sorted(found)[-2][0],
  print password

print '-------'
print username # Admin@G0
print password # S2Cr2t-m2Mb2r's_P4sSw0rd~!@.@

p = Popen(('./Goversing',), stdin=PIPE)
p.communicate('''1
'''+username+'''
'''+password+'''
2
3
''')

# FLAG{39e1316661e80847b12dae96789a13e4a3d3b496}
