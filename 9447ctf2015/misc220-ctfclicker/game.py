#!/usr/bin/env pypy
from collections import namedtuple, Counter

Item = namedtuple('Item', 'name basecost income itemno')
items = (
  Item(name="Art Money", basecost=5, income=4, itemno=0),
  Item(name="Cheat Engine", basecost=50, income=30, itemno=1),
  Item(name="GNU strings", basecost=1000, income=550, itemno=2),
  Item(name="IDA Pro", basecost=30000, income=12000, itemno=3),
  Item(name="Geohot clone", basecost=1234567, income=500000, itemno=4),
  Item(name="The Real Flag", basecost=224064959, income=0, itemno=5),
)

class State(namedtuple('State', 'rseq money owned roundno startedwith')):
  def cost(self, itemno):
    return int(1.2 ** self.owned[itemno] * items[itemno].basecost)
  def canbuy(self, itemno):
    # Also includes does a trivial "should buy"
    return self.money >= self.cost(itemno) < items[itemno].income * (99 - self.roundno)
  def payoffs(self):
    payoffs = []
    for i in range(5):
      if not self.canbuy(i):
        continue
      payoffs.append(((99-self.roundno) * items[i].income - self.cost(i), i))
    payoffs.sort()
    return payoffs
  def purchase_item(self, itemno):
    newowned = self.owned[:]
    newowned[itemno] += 1
    try:
      # We sort the buy sequence since the last tick in order to de-duplicate logically identical states.
      t = self.rseq.index('t')
      rseq = tuple(sorted(self.rseq[:t] + ('b '+str(itemno),))) + self.rseq[t:]
    except ValueError:
      rseq = ('b '+str(itemno),) + self.rseq
    t = State(rseq=rseq, money=self.money-self.cost(itemno), owned=newowned, roundno=self.roundno, startedwith=self.startedwith)
    assert t.money >= 0
    return t
  def perround(self):
    x = 10
    for i in range(5):
      x += self.owned[i] * items[i].income
    self.perround = lambda y=x: y
    return x
  def click(self):
    money = self.money+self.perround()
    return State(rseq=('t',)+self.rseq, money=money, owned=self.owned, roundno=self.roundno+1, startedwith=money)
  def value(self):
    return self.money + (99-self.roundno)*self.perround()
  def is_strictly_worse(self, other):
    if self.money <= other.money and self.perround() <= other.perround() and self.roundno >= other.roundno:
      return self.money != other.money or self.perround() != other.perround() or self.roundno != other.roundno
    return False
  @property
  def seq(self):
    return self.rseq[::-1]
  def strseq(self, numberturns = False):
    s = []
    counter = 1
    for i in self.seq:
      if numberturns and i == 't':
        s.append('t   %d' % counter)
        counter += 1
      else:
        s.append(i)
    return '\n'.join(s)

def eliminate(states, cap=99):
  outstates = []
  for qstate in states:
    if qstate.roundno > cap:
      continue
    for taken_state in outstates:
      if qstate.rseq == taken_state.rseq:
        break
      if qstate.is_strictly_worse(taken_state):
        break
    else:
      # Not strictly worse than something in outstates
      outstates = [i for i in outstates if not i.is_strictly_worse(qstate)]
      outstates.append(qstate)
  return outstates

def chunks(x, n):
  chunksize = (len(x)+n-1)//n
  return [x[i:i+chunksize] for i in xrange(0, len(x), chunksize)]

def stephead(head):
  newheads = []
  newheads.append(head.click())
  payoffs = head.payoffs()
  for value, itemno in payoffs:
    if value <= 0:
      pass
    newheads.append(head.purchase_item(itemno))
  return newheads #eliminate(newheads)

def multistep(heads):
  outheads = []
  for i in range(3):
    for head in heads:
      outheads += stephead(head)
    outheads = eliminate(outheads)
  return outheads


def findbest(startstate, criterion=lambda x: x.money, cap=99):
  from multiprocessing import Pool, cpu_count

  ncpus = cpu_count()
  mypool = Pool(ncpus)

  heads = [startstate]
  best = startstate
  trailing_edge = 0
  while heads:
    print trailing_edge, len(heads)
    x = []
    toconcat = mypool.map(multistep, chunks(heads, ncpus*4), 1)
    for i in toconcat:
      x += i
    heads = eliminate(x, cap=cap)
    minroundno = 999
    for i in heads:
      if i.roundno < minroundno:
        minroundno = i.roundno
      if criterion(i) > criterion(best):
        best = i
    trailing_edge = minroundno
  return best

zerostate = State(rseq=(), money=50, owned=[0]*6, roundno=0, startedwith=0)

# findbest(zerostate) would take a long time to run. So, we assume that the best state
# will be the one that purchased the most expensive item soonest. The magic "47" is there
# because we knew a round-47 buy was possible from previous efforts at finding good states

partial = findbest(zerostate, lambda x: (x.owned[4], x.value()), 47)

print partial
# State(rseq=('b 4', 't', 't', 't', 't', 't', 't', 't', 't', 't', 'b 3', 't', 't', 'b 3', 't', 'b 3', 't', 'b 3', 't', 'b 0', 'b 1', 'b 1', 'b 1', 'b 1', 'b 2', 'b 2', 't', 'b 3', 't', 'b 3', 't', 'b 3', 't', 'b 0', 'b 0', 'b 2', 'b 2', 'b 2', 't', 'b 3', 't', 'b 3', 't', 't', 'b 1', 't', 'b 3', 't', 't', 't', 't', 't', 't', 'b 2', 't', 'b 0', 'b 1', 'b 2', 't', 'b 1', 'b 1', 'b 2', 't', 'b 0', 'b 0', 'b 1', 'b 2', 't', 'b 1', 'b 2', 't', 'b 2', 't', 'b 2', 't', 'b 0', 'b 0', 'b 1', 'b 1', 't', 'b 2', 't', 't', 't', 't', 'b 1', 't', 'b 0', 'b 0', 'b 0', 'b 1', 't', 'b 0', 'b 0', 'b 1', 't', 'b 0', 'b 1', 't', 'b 1', 't', 'b 0', 'b 0', 'b 0', 'b 0', 'b 0', 't', 'b 1'), money=71, owned=[19, 18, 13, 10, 1, 0], roundno=47, startedwith=1234638)

best = findbest(partial)
print best
# State(rseq=('t', 't', 't', 't', 't', 't', 't', 't', 't', 't', 't', 't', 't', 't', 't', 't', 't', 't', 't', 't', 't', 't', 't', 't', 't', 't', 't', 't', 't', 't', 't', 'b 4', 't', 't', 'b 4', 't', 'b 3', 't', 'b 4', 't', 'b 4', 't', 't', 'b 4', 't', 'b 4', 't', 'b 3', 'b 3', 't', 'b 4', 't', 'b 4', 't', 'b 4', 't', 'b 4', 't', 't', 'b 4', 't', 'b 4', 't', 'b 2', 'b 2', 't', 'b 4', 't', 't', 'b 0', 'b 0', 'b 1', 'b 2', 'b 2', 'b 2', 'b 3', 'b 3', 't', 'b 4', 't', 't', 't', 't', 't', 't', 't', 't', 't', 'b 3', 't', 't', 'b 3', 't', 'b 3', 't', 'b 3', 't', 'b 0', 'b 1', 'b 1', 'b 1', 'b 1', 'b 2', 'b 2', 't', 'b 3', 't', 'b 3', 't', 'b 3', 't', 'b 0', 'b 0', 'b 2', 'b 2', 'b 2', 't', 'b 3', 't', 'b 3', 't', 't', 'b 1', 't', 'b 3', 't', 't', 't', 't', 't', 't', 'b 2', 't', 'b 0', 'b 1', 'b 2', 't', 'b 1', 'b 1', 'b 2', 't', 'b 0', 'b 0', 'b 1', 'b 2', 't', 'b 1', 'b 2', 't', 'b 2', 't', 'b 2', 't', 'b 0', 'b 0', 'b 1', 'b 1', 't', 'b 2', 't', 't', 't', 't', 'b 1', 't', 'b 0', 'b 0', 'b 0', 'b 1', 't', 'b 0', 'b 0', 'b 1', 't', 'b 0', 'b 1', 't', 'b 1', 't', 'b 0', 'b 0', 'b 0', 'b 0', 'b 0', 't', 'b 1'), money=224064959, owned=[21, 19, 18, 15, 14, 0], roundno=99, startedwith=224064959)

assert best.money >= items[5].basecost
print best.purchase_item(5).strseq()
