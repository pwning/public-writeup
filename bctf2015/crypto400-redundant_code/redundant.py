#!/usr/bin/python
# Implementation of the redundant_code binary in python.
# All the names have nothing to do with graphs, because I only
# realized the program was representing graphs after reversing.

class Arr(object):
  def __init__(self, nslots = 0, counter = 0):
    self.counter = counter # Edge counter.
    self.slots = [[] for i in range(nslots)] # Adjacency lists for each vertex.

  def insert(self, x, y): # Adds an edge between vertex number x and y
    assert x != y
    self.slots[x].append((y, self.counter))
    self.slots[y].append((x, self.counter))
    self.counter += 1

  def printme(self): # The pretty print from the redundant_code binary
    print len(self.slots), self.counter
    for i in range(len(self.slots)):
      for ref, cc in reversed(self.slots[i]):
        if ref > i:
          print i+1, ref+1

def around(inarr): # Performs the line graph transform.
  outarr = Arr(nslots = inarr.counter)
  for slot in inarr.slots:
    # for each vertex
    for i in range(len(slot)):
      for e in range(i+1, len(slot)):
        # for each pair of its edges, make an edge between them.
        outarr.insert(slot[-i-1][1], slot[-e-1][1])
  return outarr

# This function loads a string input into the star graph representation
def fromstr(s):
  arr = Arr(len(s) + 2 + sum(ord(c)-ord('0') for c in s))
  for i in range(len(s)+1):
    arr.insert(i, i+1)

  xxx = len(s) + 2
  for i in range(len(s)):
    for _ in range(ord(s[i])-ord('0')):
      arr.insert(i+1, xxx)
      xxx += 1
  return arr

if __name__ == '__main__':
  import sys
  # Like the redundant_code binary, print the iterated line graph of the encoded input.
  around(around(fromstr(sys.argv[1]))).printme()
