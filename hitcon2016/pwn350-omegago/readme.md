## OmegaGo - Pwn 350 Problem

### Description

Want to fight with AlphaGo? Beat OmegaGo first.
nc 52.198.232.90 31337

Note: The game rule has been simplified to make life easier.

(link to binary and libc)

### Overview

OmegaGo is a x86-64 ELF (NX, partial RELRO, no PIE) implementing a
simplified go game where you can play multiple games against a computer
opponent. The computer goes first and plays
[mirror go](http://senseis.xmp.net/?MirrorGo).  If the mirror move is
not legal, it places a stone at the first legal position on the board.

The program keeps a full history of the game and allows taking back moves (via
the `regret` command).

The game continues until no legal moves are possible or the player
resigns (via the `surrender` command). At the end of each game, the
player can optionally print the full history of the game, then choose
whether or not to play again.

### Reversing

Reversing the Go implementation, we see that it creates computer and
human player objects that implement a virtual `Play` method.

```
class Player {
 public:
  virtual void Play(GameState *state, int player_number, uint32_t *row, uint32_t *col) {};
};

class Human : public Player { ... };
class Computer : public Player { ... };
```

The computer's `Play` method implements the mirror go strategy and the
human's `Play` method reads 10 bytes into a global buffer, `g_input` and
interprets them as board coordinates or commands (`regret`,
`surrender`).

The program represents boards using a bitmap. Each position on the 19x19
board has three possible states, empty (`.` - 0), computer (`O` - 1), or
human (`X` - 2). Each of the 19x19 positions is represented by two
adjacent bits (a half-nibble) in the bitmap (with the 0b11 value never
occurring).

```
struct GameState {
  uint64_t board_bitmap[12];
  uint32_t move_row;
  uint32_t move_row;
  uint32_t player;
  uint32_t pad0;
  double player1_time_remaining;
  double player2_time_remaining;
};
```

The program keeps track of the history of the game with a static global
array of `GameState` pointers. The array occurs immediately before a
global variable containing the current game state.

```
GameState *g_history[364];
GameState g_current_state;
```

Each move, the program allocates a new `GameState` and copies the
current game state into it. 

```
GameState *state = new Gamestate;
*state = g_current_state;
g_history[g_history_size] = state;
```

Taking a move back is implemented by the following logic:

```
delete_last_move() {
  ...
  delete g_history[--g_history_size];
  ...
}

take_back_move() {
	delete_last_move(); // roll back computer's last move
	delete_last_move(); // roll back player's last move
	g_current_state = *g_history[g_history_size - 1];
}
```

In addition to the history, the game maintains a set of hashes of the
board, `g_board_set`. If a board position is ever repeated, the program
exits immediately.

At the beginning of each game, the program frees each element of
`g_history`, clears `g_position_set`, and reallocates new `Computer` and
`Human` objects. The program never frees these objects - a fact which we
take advantage of in the exploit.

### Bug

Writes to `g_history` are not bounds checked. If the game consists of
more than 364 moves, the program will continue to write `GameState`
pointers past the end of `g_history`.

### Exploit

In order to trigger teh bug, we need to construct a game which takes
>394 moves, taking into account that repeat positions are not allowed,
and the board only has 19x19, or 361 points.

To do this, we use the concept of [ko](http://senseis.xmp.net/?ko).

```
  ABCDEFGHIJ
1 
2  XO    XO
3 XO O  X XO
4  XO    XO
5
```

Here, we show a mirrored ko situation on a smaller board. By making a
formation like the above, X (the human) can capture at C3. The computer
will make the corresponding mirrored move at H3, leading to:

```
  ABCDEFGHIJ
1 
2  XO    XO
3 X XO  XO O
4  XO    XO
5 
```

Next, X moves elsewhere, say A1, and O mirrors accordingly:

```
  ABCDEFGHIJ
1 X
2  XO    XO
3 X XO  XO O
4  XO    XO
5          O
```

Now, X can recapture the ko without repeating the position by playing
I4:

```
  ABCDEFGHIJ
1 X
2  XO    XO
3 XO O  X XO
4  XO    XO
5          O
```

For every subsequent move, we can waste another move by recapturing the
ko. This allows us to spend moves without filling up more of the board.
In the exploit, we loop through 4 kos (8 counting mirrors) to let us
waste 4 additional moves for each move that fills up an additional point
on the board.

Now, we can use this bug to overlap `g_history[364]` with the current
position and corrupt `g_history[364]` by making moves affecting the
first 8 bytes of the bitmap. One complication is that, we are only able
to place either an O or an X on a point that is currently empty. In
terms of the bitmap, we can change a 0b00 half-nibble to either 0b01 or
0b10.

Luckily, the bottom 12 bits of heap addresses were fully consistent
across runs. To nudge the address into a value where our primitive is
useful, we start by surrendering 3 games immediately to influence heap
address via the leaked `Player` objects.

Next, we use the ko strategy to grow the history to make 365 moves (the
last one being the last computer move). Now, the `GameState` pointer at
`g_history[364]` is written over the first 8 bytes of the bitmap in
`g_current_state`.

Now we place a piece to increment the `GameState` pointer by 0x80. This
points `g_history[364]` to a location containing some zeros, followed by
a libc address. At this point, we have:

```
g_history[364] = computer_move + 0x80
g_history[365] = move_we_just_made
g_history[366] = computer_response
```

by taking back our move, we execute the `take_back_move`, which ends
with:

```
// g_history_size = 365
*g_current_state = g_history[g_history_size - 1];

```

This writes a libc address to the current board, and also sets
`g_history[364]` to 0 which is critical, since this pointer will be
freed later when we start the next game. By reading out the board, we
leak a libc address.

Now, we surrender the game and repeat the process. This time, we also
construct a fake fastbin chunk of size 0x20 on the game board (matching
the chunk size for `Player` objects):

Once again, we make moves until `g_history[364]` overlaps with the
bottom 8 bytes of the `g_current_state`'s bitmap. We make additional
moves to change the bottom 12 bits of this pointer from 0x410 to 0x550,
which points it the fake fastbin chunk inside one of the `GameState`
objects.

Finally, we surrender this game, freeing the fake fastbin chunk. We play
one final game. This time, the `Computer` object is allocated at our
fake fastbin chunk. We setup the board to place a fake vtable address in
the bitmap (we used `g_input + 4`, which contains no 0b11 half-nibbles).
We then made moves until a `GameState` overlapped our fake fastbin
chunk on that final move, we add the address of our desired rip 4 bytes
into the input buffer. After the move, the `Computer` object's vtable is
overwritten with the fake vtable we placed in the bitmap. On the next
computer move, the program jumps an addres of our choosing.

Since the program is an xinetd service, we were able to use a gadget in libc which does:

```
execve("/bin/sh", rsp + 0x70, environ);
```

to get a shell.

For unknown reasons, despite having a reliable local exploit, the
exploit was unreliable against the remote server (in Japan) when sent
from a machine in the US.
