## ctfclicker - Misc 220 Problem

### Description

This network service implements a "cookie clicker" style game. The player must earn enough money in 100 rounds of the game to purchase the "flag" item (upon which, the service will send the flag to the player).

### Solution

It appears that you need to find an optimal solution for the game in order to get the flag: we first generated some "decent" action sequences for the game, and never wound up with enough money to purchase the flag. This problem seems amenable to a dynamic programming solution, but DP is for nerds; real hackers brute force. Any allegations that I tried to use DP to solve this problem and miserably failed are unsubstantiated.

The attached `game.py` brute forces an optimal solution to the game via a breadth-first search through the possible game states. The following optimizations are made during the search:

1. We prune out all game states that are strictly worse than another state we've found. We consider state x to be strictly worse than state y iff:
    a. x has less money on hand than y
    b. x has less future earning potential than state y
    c. x is on a round equal to or greater than state y
2. We took the assumption that the optimal solution buys the most expensive item at the earliest possible point in time. This assumption seemed justified by our earlier attempts at computing good action sequences. This assumption allows us to split up the brute force: instead of having to search through one 100-round game, we can search through two consecutive ~50 round games. Thus, we brute force in two stages:
    a. Find the earliest possible state that buys the most expensive item.
    b. Starting from that state, find the state with the most money.

Executing this script with PyPy takes ~2 minutes on my laptop, thanks to some multiprocessing hacks.

Knowing the optimal solution to the ctfclicker game isn't quite enough: to actually play the game, you must solve an scrypt proof-of-work once per round. Because there's an `alarm(40)` at the start of the program, it'd be difficult to solve the proof-of-work challenges live and be able to complete the game. In order to work around this, you must exploit the fact that randomness in these challenges is derived from `srand(time(NULL) >> 4)` to precompute the proof-of-work responses (or get a really fast computer, I guess). This proof-of-work pre-computation is implemented in `seqgen.py`.

The attached `solve.py` connects to the service and plays the game; it contains baked-in results from `game.py`, and requires input from `seqgen.py`. Obviously, this solution was a team effort! ;)
