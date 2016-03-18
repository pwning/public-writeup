#
# The first half of this script is the code that was provided
# as part of the CTF challenge.
#

import md5
def encode(input_string):
    #print input_string
    h = md5.md5(input_string[:4]).hexdigest()
    table = {
        'a': 1,
        'b': 2,
        'c': 3,
        'd': 4,
        'e': 5,
        'f': 6,
        'g': 7,
        'h': 8,
        'i': 9,
        'j': 0
    }
    out = ""
    prev = ""
    stage1 = []
    stage2 = []
    stage3 = ""
    passbyte = -1
    for ch in input_string:
        if ch in table.keys():
            stage1.append(table[ch])
        else:
            stage1.append(ch)

    for index, ch in enumerate(stage1):
        if len(stage1) <= index+1:
            if index != passbyte:
                stage2.append(ch)
            break

        if passbyte != -1 and passbyte == index:
            continue

        if type(ch) == int and type(stage1[index+1])==int:
            tmp = ch << 4
            tmp |= stage1[index+1]
            stage2.append(tmp)
            passbyte = index+1
        else:
            stage2.append(ch)

    for ch in stage2:
        if type(ch) == int:
            stage3 += chr(ch)
        else:
            stage3 += ch
    
    for index, ch in enumerate(stage3):
        if index >= len(h):
            choice = 0
        else:
            choice = index

        out += chr(ord(ch) ^ ord(h[choice]))

    return out

encoded = "~u/\x15mK\x11N`[^\x13E2JKj0K;3^D3\x18\x15g\xbc\\Gb\x14T\x19E"

#
# Solution:
#

charset = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890_ '
niter = len('qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890_')**4
block = niter / 100 + 1

import sys
def find_base():
  from itertools import product
  for i, x in enumerate(product(charset, repeat=4)):
    if i % block == 0:
      print str(100*i/niter)+"%",
      sys.stdout.flush()
    if encoded.startswith(encode(''.join(x))):
      print
      print ''.join(x)

# Step 1: Brute force the first 4 chars, the ones that
# determine the md5 hash that affect the whole output.
# There are 5 possibilities, but "FLag" is the right one
# (and the obvious chice).
#find_base()
base = "FLag"


# Step 2: The first thing I tried, just brute-forcing
# char by char, works for most of the flag
while encode(base) != encoded:
  choice = None
  for x in range(32, 127):
    x = chr(x)
    if encoded.startswith(encode(base+x)):
      print '>', x
      if choice is None:
        choice = x
  if choice is None:
    break
  base += choice
  print base

# base = "FLag is {compress_is_always_"

# Step 3: Step 2 stops working for some reason (probably due
# to the 2-character `table` translation done in `encode`).
# So I tried brute-forcing every 2 characters from there,
# and that did the job.
while encode(base) != encoded:
  choice = None
  for x1 in range(32, 127):
    for y1 in range(32, 127):
      x = chr(x1)+chr(y1)
      if encoded.startswith(encode(base+x)):
        print '>', x
        if choice is None:
          choice = x
        else:
          print '^^^ Alternate possibility!'
  if choice is None:
    break
  base += choice
  print base

# base = "FLag is {compress_is_always_helpful!"
base += '}'  # The above process isn't perfect, but whatever.
print base
