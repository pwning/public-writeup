# algo_auth - misc - Writeup by Corwin de Boor (@strikeskids)

All we are given is a remote endpoint `nc 110.10.147.104 15712`. Upon connection, we
are given the problem statement.

```
==> Hi, I like an algorithm. So, i make a new authentication system.
==> It has a total of 100 stages.
==> Each stage gives a 7 by 7 matrix below sample.
==> Find the smallest path sum in matrix, 
    by starting in any cell in the left column and finishing in any cell in the right column, 
    and only moving up, down, and right.
==> The answer for the sample matrix is 12.
==> If you clear the entire stage, you will be able to authenticate.

[sample]
99 99 99 99 99 99 99 
99 99 99 99 99 99 99 
99 99 99 99 99 99 99 
99 99 99 99 99 99 99 
99  1  1  1 99  1  1 
 1  1 99  1 99  1 99 
99 99 99  1  1  1 99 

If you want to start, type the G key within 10 seconds....>>
```

Because we cannot move left in the maze, we can process the columns one-by-
one. The initial best way to get to any cell within the column is to move
right from the cell in the column before it. There is never a reason to both
move up and move down within the same column (because you will only visit that
column once), so you can first try all of the upward movements and then all of
the downward movements (in the order, so costs propagate). Then, we can just
take the minimum cost of the right column to get the answer to our simple
dynamic program.

Upon solving all of the stages, you are presented with the annoying message

```
@@@@@ Congratz! Your answers are an answer
```

I immediately guessed that the answers were ascii character codes, and
modified the my script to print out the answer as a character. Then, I had to
re-run the entire thing. This printed out a string that looked like all
printable characters, which was a good sign. Unfortunately, the flag was not
accepted.

```
RkxBRyA6IGcwMG9vT09kX2owQiEhIV9fX3VuY29tZm9ydDRibGVfX3MzY3VyaXR5X19pc19fbjB0X180X19zZWN1cml0eSEhISEh
```

What you have to realize is that this string is actually the flag base64-encoded.
Decoding gives you

```
FLAG : g00ooOOd_j0B!!!___uncomfort4ble__s3curity__is__n0t__4__security!!!!!
```
