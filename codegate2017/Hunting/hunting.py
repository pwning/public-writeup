import pty
import subprocess
import os
import time
import select
import sys
import ctypes


master, slave = pty.openpty()
p = subprocess.Popen(["/home/hunting/hunting"], stdin=slave, stdout=slave, stderr=slave)

LIBC = ctypes.cdll.LoadLibrary("libc.so.6")
LIBC.srand(LIBC.time(0))

def readuntil(target):
  s = ''
  while not s.endswith(target):
    c = os.read(master, 1)
    sys.stdout.write(c)
    s += c
  return s

def readall(timeout=1):
  s = ''
  while select.select([master], [], [], timeout)[0]:
    c = os.read(master, 2048)
    sys.stdout.write(c)
    s += c
  return s

def write(s):
  #sys.stdout.write(s)
  os.write(master, s)


# ice ball:
#   sleep(0)
#   dmg = (rand()&0xFFFF) % 1000
# It's just a high-damage move that can quickly get us to the final boss.
readuntil("choice:")
write('3\n')
readuntil("choice:")
write('3\n')

# Lookup the defensive move that will prevent any damange to us.
def getdef():
  return [1,3,2,1][LIBC.rand() % 4]

# Beat the easy bosses.
for health in [100, 1000, 3000]:
  while health > 0:
    dmg = (LIBC.rand() & 0xFFFF) % 1000
    readuntil("1. How to play")
    write('2\n')
    readuntil("=====================================")
    readuntil("=====================================")
    readuntil("=====================================")
    write('%d\n' % getdef())
    health -= dmg

# Final boss time.
readuntil("choice:")
for i in range(2):
  # fireball
  #   dmg = (rand() % 1000 << 16) % 100
  #   sleep(1)
  write('3\n')
  readuntil("choice:")
  write('2\n')

  write('2\n')
  LIBC.rand() # Happens in the attack thread...
  time.sleep(0.1) # ...so make sure it applies before issuing our defense.
  write('%d\n' % getdef())

  # ice sword:
  #   rand(); rand(); rand();
  #   dmg = (1<<32) - 1
  #   sleep(1)
  readuntil("choice:")
  write('3\n')
  readuntil("choice:")
  write('7\n')
  time.sleep(0.4)

  write('2\n')
  LIBC.rand(); LIBC.rand(); LIBC.rand() # Same deal...
  time.sleep(0.1) # ...gotta wait until the above rands apply.
  write('%d\n' % getdef())

  # We've issued the ice sword attack half a second after,
  # so the fireball attack happens with the ice sword's -1 dmg.

  # Wait until everything finishes, then go again.
  time.sleep(0.9)
  readall()

readall(5) # should print flag
