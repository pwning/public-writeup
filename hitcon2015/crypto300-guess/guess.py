import sys

def recvuntil(s):
  dat = bytearray()
  while not dat.endswith(s):
    cc = rfile.read(1)
    dat.append(cc[0])
  dat = bytes(dat)
  sys.stdout.write(dat)
  return dat[:-len(s)]

def recvn(n):
  dat = bytearray()
  while len(dat) < n:
    cc = rfile.read(1)
    dat.append(cc[0])
  dat = bytes(dat)
  sys.stdout.write(dat)
  return dat

def recvs(s):
  for c in s:
    cc = rfile.read(1)
    sys.stdout.write(cc)
    assert c == cc[0]

import select
def recvany():
  dat = bytearray()
  while select.select([rfile], [], [], 0.1)[0]:
    cc = rfile.read(1)
    if len(cc) != 1:
      break
    dat.append(cc[0])
  dat = bytes(dat)
  sys.stdout.write(dat)
  sys.stdout.flush()
  return dat

def send(s):
  sys.stdout.write('\033[92m'+s.encode('hex')+'\033[0m'+'\n')
  wfile.write(s)

fixed_guesses = []
for bitpos in range(7):
  for char in range(1, 32):
    s = bytearray(32)
    s[0] = 1<<bitpos
    s[char] = 1<<bitpos
    fixed_guesses.append((bitpos, char, str(s)))

import socket, subprocess
while True:
  sock = socket.create_connection(('52.69.244.164', 9355))
  # sock = socket.create_connection(('127.0.0.1', 9355))
  sys.stdout.flush()
  wfile = sock.makefile('wb', 0)
  rfile = sock.makefile('rb', 0)

  recvuntil("begins with ")
  b1 = int(recvuntil(" "), 0)
  b2 = int(recvuntil(" "), 0)
  b3 = int(recvuntil(" "), 0)
  b4 = int(recvuntil(", "), 0)

  recvuntil("? ")
  # ./sha.sh solves the proof-of-work.
  send(chr(b1)+chr(b2)+chr(b3)+chr(b4)+subprocess.check_output(("./sha.sh", str((b1 + (b2<<8) + (b3<<16) + (b4<<24))))).strip().decode('hex'))
  recvuntil("Try to guess the secret!\n")
  guesses_left = 256
  def guess(ss):
    global guesses_left
    guesses = [ss] if isinstance(ss, (bytes, bytearray)) else ss
    for s in ss:
      assert guesses_left > 0
      guesses_left -= 1
      # We're not allowed to guess "\x00"*32, so just always
      # invert the last guessed char.
      send(s[:-1] + chr(ord(s[-1])^0xFF))
    results = [recvuntil("\n") != "Nope." for s in guesses]
    return results[0] if isinstance(ss, (bytes, bytearray)) else results

  # Wait until we get delt bytes that naturally add up to zero. This seems
  # to happen with roughly 1/1000 probability.
  if not guess("\x00"*32):
    sock.close()
    continue
  print "Found a natural 0 sum."

  equiv = [[0]*8 for i in range(32)]
  def eq2i(b):
    return sum(x << i for i, x in enumerate(b))

  # We need the fixed_guesses trick to send a bunch of stuff all at once,
  # otherwise the service times out.
  for (bitpos, char, s), res in zip(fixed_guesses, guess([i[2] for i in fixed_guesses])):
    equiv[char][bitpos] = 1 if res else 0

  for bitpos in range(6):
    # Find two chars with a matching bitpos
    for c1, c2 in [(1,2), (1,3), (2,3)]:
      if equiv[c1][bitpos] == equiv[c2][bitpos]:
        break
    else:
      assert False
    s = bytearray(32)
    s[c1] = 1<<bitpos
    s[c2] = 1<<bitpos
    s[0] = 1<<(bitpos+1)

    #if (levels are considered the same) == (levels should be different)
    if ( equiv[0][bitpos+1] == equiv[c1][bitpos] ) == guess(str(s)):
      # flip level bitpos+1 (doesn't break anything because we iterate from bottom to top)
      for i in range(32):
        equiv[i][bitpos+1] = 1 - equiv[i][bitpos+1]

  # There's a 50% chance we've got these all inverted, but whatever.
  # for i in range(32):
  #   for j in range(7):
  #     equiv[i][j] = 1 - equiv[i][j]

  # Now for the sign bits
  for char in range(1, 32):
    s = bytearray(32)

    low0 = eq2i(equiv[0][:7])
    lowc = eq2i(equiv[char][:7])

    s[0] = low0 ^ 0 ^ 0x80
    s[char] = lowc ^ 0x7f ^ 0x80

    # add the difference elsewhere
    diff = (low0 - 0) + (lowc - 0x7F)

    for c2 in range(1, 32):
      if diff == 0:
        break
      if char == c2:
        continue
      c2v = eq2i(equiv[c2][:7])
      if diff > 0:
        change = min(diff, 0x7f-c2v)
        diff -= change
        c2n = c2v + change
      else:
        change = min(-diff, c2v)
        diff += change
        c2n = c2v - change
      s[c2] = c2v ^ c2n

    equiv[char][7] = 1 if guess(str(s)) else 0

  # There's a separate 50% chance that we got the sign bits inverted. Whatever.
  # for i in range(32):
  #   equiv[i][7] = 1 - equiv[i][7]

  # Burn extra guesses
  while guesses_left > 0:
    guess("\x00"*32)

  recvuntil("Now tell me what the secret is.\n")

  secret = ''.join(chr(eq2i(b)) for b in equiv)
  send(secret[:-1]+chr(ord(secret[-1])^0xff)) # Account for the flip guess() does.

  try:
    s = ''
    cc = rfile.read(1)
    while len(cc) > 0:
      s += cc
      sys.stdout.write(cc)
      sys.stdout.flush()
      cc = rfile.read(1)
    if "zzz too slooooooow..." not in s:
      print "FLAG FLAG FLAG FLAG FLAG"
      subprocess.check_output(("sh", "-c", "echo '%s' | xxd -r -ps | wall" % s.encode('hex')))
      break
  except socket.error:
    pass
  print "Damn, guessed wrong."
  sock.close()
