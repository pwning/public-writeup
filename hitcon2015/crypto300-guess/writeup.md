# guess (crypto 300)

Guess is a math challenge wherein a service gives you a limited number of questions to determine the value of 32 random bytes (and grants you the flag if you beat this game).

### Step 1: Reverse it!

The main logic of the service is written in a series of mmx instructions, which takes some care to reverse. Here's what the service does:

1. Proof of work

2. Takes 32 bytes from /dev/urandom, treated as a vector of 32 signed 8-bit integers.

3. Takes 32 bytes of user input, xors it with with the random vector.

4. Gets the 32-bit signed sum of the elements (i.e. addition does NOT wrap modulo 256).

5. Returns to the user whether or not that sum is zero.

6. Steps 3,5,6 repeat for a total of 256 times, and then the service asks you to provide the original random vector.


In pseudocode:

    # proof of work omitted
    randvec = [randint(0, 255) for i in range(32)]
    for _ in range(256):
      xoredvec = [ord(c) ^ i for i, c in zip(randvec,raw_input())]
      x = sum((i if i < 128 else i-256) for i in xoredvec)
      print "Yep" if x == 0 else "Nope"
    if all(ord(c) == i for i, c in zip(randvec,raw_input())):
      print open("./flag").read()

### Step 2: Get flag.

Our strategy for playing this game is described below, and implemented in `guess.py`.

0. Definitions.
    * "Yes": A response from the server that the computed sum was zero.
    * "No": A response from the server that the computed sum was nonzero.
    * X thru Y: Integers from X to Y, inclusive.
    * `V`: The random vector we are trying to determine.
    * `V[n][m]`: The `m`th bit (0 thru 7) of the `n`th (0 thru 31) element of `V`. `m=0` is the LSB, `m=7` is the sign bit.
    * `G(x/y, z/w, ...)`: Play the game, submitting a query vector that is zeros aside from: bit `y` of byte `x`, bit `w` of byte `z`, .... These bits are set high.
    * `X`: The xored vector, between `V` and some user-supplied vector. (This is what gets summed element-wise to determine "Yes" or "No").

1. Repeatedly re-connect to the service, and wait until sending 32 null bytes gives us a "Yes". This happens with probability ~1/1000, so we don't have to wait too long.

2. We assume that `V[0][0] == 0` (we'll be right with 50% probability), and then use the following facts to determine `V[0 thru 31][0 thru 6]` (everything but the sign bits). This takes a total of 31 * 7 + 6 = 223 queries (31 * 7 applications of the first fact to test bit equality for a particular bit position across all bytes, and 6 applications of the second to test bit equality between different bit positions across any bytes).
    * For `0 <= m <= 6`, `G(x/m, y/m)` is "No" iff `V[x][m] == V[y][m]`.
    * For `0 <= m <= 5` and `V[x][m] == V[y][m]` and distinct `x, y, z`, `G(x/m, y/m, z/(m+1))` is "Yes" iff `V[z][m+1] == V[y][m]`.

3. We assume that `V[0][7] == 0` (the sign bit), and then test bit equality between all the signbits in 32 queries using the following technique to test if the signbits `V[x][7]` and `V[y][7]` are equal:
    1. Use our knowledge of all the non-sign bits to prepare a query such that `X[x][0 thru 6] == 0` and `X[y][0 thru 6] == 0x7F`, while simultaneously maintaining that the query will certainly be a "Yes" (by effectively doing adds or subtracts to other elements of `X` to balance out the mentioned changes; see the code for more detail). This means that `X[x]` is either 0 or -128, and `X[y]` is either 127 or -1.
    2. We run a `G(x/7, y/7, <the prepared query from above>)`. Based on the way "(0 or -128) plus (127 or -1)" does or doesn't add up to zero, we see that `V[x][7] == V[y][7]` iff the query is "No".

4. In total, we've determined all the bytes 25% probability using 255 guesses. Since due to step 1. this method applies only ~1/1000 connections, it takes an expected 4000 connections to win the game and recover the flag (for us, it took ~5000 connections).

### Caveats

1. The challenge allows for multiple attempts per proof-of-work, which you could use to be more efficient with connections.

2. The challenge doesn't allow submitting all null bytes as a query (even though the method described above uses this). We worked around this by xoring the last byte of every query with 0xFF, which should usually make things happy.
