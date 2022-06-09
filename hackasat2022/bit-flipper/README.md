# Bit Flipper

For this problem, we were given a [binary](./bitflipper) that had a complicated routine for flipping bits in a variable based on user input that involved shifting and xor'ing.  While some of my teammates statically reversed the binary, I worked on black-boxing the entire process and making observations about how the program worked purely from observation.

When connecting to the server, the user would basically get to play a game consisting of a number of rounds.  Every round the user would submit a number, and receive back a number from the server.  Pretty quickly, I had the following observations:

1. Observation: If you submit 0 to the initial round, the server will return 16.
2. Observation: If you submit 1 to the initial round, the server will return some number less than 16.
3. Observation: If the server outputs `X` and then you submit any number `Y` twice in a row, then the server will output `X` again.

Since we know it's doing something with XOR from the limited static reversing, observation (3) makes a lot of sense; you're simply doing and then ondoing an operation.  Next I decided to do a basic search by submitting the pattern `1, 2, 1, 4, 1, 2, 1, 8, ...`; note that after each step of this pattern, the cumulative XOR of the values submitted so far is always unique.  This gave rise to the following observations:

4. Observation: When submitting this pattern, every other value returned by the server would be 16.
5. Observation: By comparing results across multiple runs, it appeared that lower numbers were less frequent, and each value `X` appeared approximately half as often as `X+1`.

Let's reformulate the game slightly: you start at some hidden value `I`, and over time build up some value `X` (which starts at 0), and the server gives you some value derived from `I ^ X`.  With this terminology and the observations so far, we can derive the following:

6. Deduction from (1), (2), and (4): the server will return 16 if and only if `X` has an even number of 1s.
7. Hypothesis from (5): the goal is to get the server to return 0.

The next step I took was to dump the server's response alongside the cumulative value of `X` at every step across several runs of the program.  (I would provide some sample data, but the problem unfortunately is no longer online at the time of writing. [Sidenote by teammate who did static reversing: despite having access to the binary, the `hardest_rotations.nums` is not provided and only exists on the server, thus re-creating sample data is non trivial])  I then spent a very long time looking for patterns, before noticing the following:

8. Observation: If the last number the server returned was 13 and you submit 15, then the server will return some number less than 13, and vice versa.

This observation seemed to hold across multiple tests, so I accepted it as a fact.  This seemed to give a good direction of how to build up to a solution: we know that we can "escape" 16 by submitting 1, and that we can "escape" 15 by submitting 3, so if we can find these "magic" number for each value greater than 0, we should be able to reduce all the way to 0 in at most 16 steps.

After staring at output for a while longer (guided by observation (6) to only check masks with an even number of 1 bits), I came to two more observations about magic numbers:

9. Observation: 3 is a magic number for 15.
10. Observation: 5 is a magic number for 14.
11. Observation: 9 IS NOT a magic number for 13.
12. Observation: 17 is a magic number for 12.

I got stuck at this point for quite a long time.  The biggest issue was that the limit of 100 rounds per connection meant that only one or two sub-12 values would generally appear per run, but I was also just simply stumped at trying to find the pattern.

However, after writing out what I knew on the whiteboard a few times, inspiration struck.  At one point I had written the magic numbers like this:

```
16: 00001
15: 00011
14: 00101
13: 01111
12: 10001
```

Something about this pattern looked really _familiar_.  After a while I erased the leading zeros and shifted around how I was writing it:

```
16:     1
15:    1 1
14:   1 0 1
13:  1 1 1 1
12: 1 0 0 0 1
```

Wait, that's a Sierpinski triangle in binary!  This led me to what I described to my teammates as "the conspiracy theory":

13. Conspiracy Theory from (2), (8), (9), (10), (12): the `16-X`'th row of the binary Sierpinski triangle is a magic number for `X`.

I tried it on a couple more runs by hand, and lo and behold, it seemed to be working.  Ultimately I reorganized my testing script a little to simply always submit the magic number from (13); see `solve.py`.  To my extreme surprise, out popped a flag!

To this day I still have no idea what the intended path in this problem was.  My understaning from my teammates' limited static reversing is that the variable that you're trying to clear is being used as an index into some array, and that's the source of the numbers we're getting back.  However, this array is read from a file we weren't given (`hardest_rotations.nums`), so I'm not sure how we were supposed to use that info.  Additionally, you had to play the game three times with slightly different rules to get the flag, but this solution somehow solves all of them, which I also don't understand.  Given that we know that it has something to do with bit shifts and XORing the fact that Sierpinski triangles could be relevant _kind of_ makes sense (since `row(X)` can be expressed as `row(X-1) ^ (row(X-1) << 1))`) I guess?

Definitely the weirdest first blood I've ever gotten in a CTF; it's not often you can solve a reversing problem without opening the binary or running it locally even one time.
