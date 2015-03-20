The supplied file was a Minecraft "region" file; having no 1337 Minecraft h4xx0rz with us, the easiest way we found to view it was to replace a similarly named file from the official Minecraft client's world-state, and simply run the client.

Contained in this region file was a [Redstone circuit](http://minecraft.gamepedia.com/Redstone_circuit), which would begin mutating a logical state of 343 bits upon pressing an in-game big red button.  There was also a friendly signpost indicating that the state bits would be an ASCII encoding of the flag after allowing the circuit operate on the state for 10^18 time-ticks.

Extracting the initial state became a matter of copying the relevant section of the game data into a .schematic file using an external editor such as [MC Edit](http://www.mcedit.net), and then extracting the relevant bits of the state using python and [NBT](https://github.com/twoolie/NBT) to avoid the lengthy process of manually copying the bits out of the game.

The killer observation was that there were 343 identical redstone "mechanisms" each containing one bit of state. Upon deconstructing the mechanisms and testing out their components in-game, one sees that they are [T flip-flops](http://en.wikipedia.org/wiki/Flip-flop_%28electronics%29#T_flip-flop) hooked up in a circular arrangement such that the output of the nth flip flop was connected to the input of the (n+1)th (mod 343). It follows that after each tick, bit n of the state is replace by its XOR with the (n-1)th bit in the state (mod 343).

From this, we arrived at a Python representation of how this circuit would act on the initial state:
```python
def rol343(x, n):
  n = n % 343
  return ((x << n) | (x >> (343-n))) & ((1<<343)-1)

state = 0b...343 bits of initial state...
for i in xrange(10**18):
  state ^= rol343(state, 1)
print bin(state)
```

An astute observer will notice two things about this program:

1. 10^18 is a big number, and Python is slow.

2. An optimized version that doesn't need 10^18 iterations to produce the same output state could be written as
```python
state = 0b...343 bits of initial state...
for i, b in enumerate(bin(10**18)[2:][::-1]):
  if b == '1': state ^= rol343(state, 2**i)
print bin(state)
```

Said astute observer would then quickly arrive at the flag (modulo sorting out the ASCII endianness, possbile off-by-one-errors on that 10^18 constant, and correctly transcribing the 343 bits of state).
