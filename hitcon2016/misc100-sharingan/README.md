# Sharingan

Sharingan was a cute little puzzle &mdash; a small game that you played against a rudimentary AI. The game itself is written in Ruby, so after a bit of ruby reversing, we can figure out how the game works. Firstly, the game takes place on an 18x18 size grid. The AI will play first, and it will always start at (9,9). From there forward, you may play on any unoccupied tile (x,y), and the AI will play its piece on the corresponding tile (18-x, 18-y). Furthermore, if at any time during the game, any number of your pieces completely surround a contiguous group of the opponents, all of the opponents pieces are removed from the game. The objective then, is to get more of your pieces on the board than your opponent. 

With this current construction, the problem is very difficult. However, they add another litle gotcha to spice things up. Whenever the player is about to capture one or more of the AIs pieces, upon playing that piece, it gets turned into one of the opponents pieces and the original action is cancelled. While this seems like it should make the game more difficult, it actually improves things considerably. Consider this construction and its reflection, where `X` are the player's pieces, and `O` are the opponents.

```
 XXX           OOO
XO OX   ...   OX XO
 XXX           OOO
```

Now, where we to play a piece in the center of this construct, normally, both teams would lose two of their pieces. Instead, however, when the piece change occurs, we now have a larger block of contiguous opponent pieces, all which get removed concurrently so this becomes

```
 XXX
XOOOX
 XXX
```
and then

```
 XXX
X   X
 XXX
```

At which point we have more than the opponent, and we win. To test, run `cat soln.txt | ruby sharingan.rb`
