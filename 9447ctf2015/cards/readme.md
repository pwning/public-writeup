## cards - Exploitation 140 Problem - Writeup by Tim Becker (@tjbecker)

### Description

We're given the binary and the source code. The game starts by asking you to enter up to 52 cards, where
cards are 64-bit nonzero integers. It then performs some unnecessary shuffling to the cards, and starts the
game. The game consists of many rounds of both you and the opponent choosing a card. Whoever chooses the larger
card wins. The game continues until you have chosen every card exactly once.
If you win more rounds than the opponent, you get the flag.

However, the game appears to be impossible to win, since the opponent will always choose the card above yours
in sorted order (modulo the number of cards).

We'll either need to find a bug that allows us to win the game, or control RIP and point it to `giveFlag`.

The binary has mostly all modern protections enabled.

```
cards: ELF 64-bit LSB  shared object, x86-64, version 1 (SYSV), dynamically linked (uses shared libs), for GNU/Linux 2.6.24, BuildID[sha1]=7bce28e26cfcb1a331fae514e91b54a855e610e1, not stripped

CANARY    : ENABLED
FORTIFY   : ENABLED
NX        : ENABLED
PIE       : ENABLED
RELRO     : FULL
```

### Solution

After failing to find an off-by-one or an uninitialized value in the `playGame` function, I redirected my
attention to the pointless shuffle function:

```c
void shuffle(long long *deck, int size) {
  int i;
  for (i = 0; i < size; i++) {
    long long val = deck[i];
    if (val < 0ll) {
      val = -val;
    }

    long long temp = deck[val % size];
    deck[val % size] = deck[(i + 1) % size];
    deck[(i + 1) % size] = temp;
  }
}
```

Since `val % size` can be negative if `val` is negative, the code attempts to ensure that the value is always
positive before doing the swap. However, there is exactly one negative number that remains negative after inverting
its sign, namely `0x8000000000000000`, since two's complement negation ensures `-val == (~val) + 1`. Therefore,
we can swap `deck[val % size]` with an arbitrary value, where `val = 0x8000000000000000`
(`-9223372036854775808`) and `size` is a controlled integer between 1 and 52. This swapped value will become
one of our cards and will be printed to us in `playGame`.

By controlling the size, we can set deck to be any small, odd negative nummber.

By analyzing the stack, we see that `deck[-1]` is the return address for `shuffle`. However, we cannot
swap that value until we have a leak. Conveniently, if `playGame` has not yet been called, then
`deck[-3]` has a leftover pointer to `_start`, which is fine to corrupt. We can use this leak to compute
the address of `printFlag`, and then swap this value onto `deck[-1]`.

See `solve.py` for the finished exploit.
