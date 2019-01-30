## 20000

We are given a tarball containing a binary and 20000 numbered so files.

The main binary prompts for a number, dlopens the corresponding so file,
then calls it's `test()` function.

The point of the challenge was apparently to search for an so that gives
us a shell.

First, we cluster the so files by piping them to objdump, cutting off
the first few lines, and hashing them.

Examining some of the clusters by hand, there appeared to be three types
of libraries. One category implements `filter1` functions, another
category implements `filter2` functions, and the last category reads
user input, passes it through filter functions from two other hardcoded
so files, and passes the user input to `system()` in various ways.

Hand-examining some of the filter functions, we saw some that were
missing shell escape characters. Choosing one of those and grepping for
it led us to number 17394, which passes user input to `system()`. The
filters for this one allowed `sh`.

```
$ nc 110.10.147.106 15959

   /$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$
  /$$__  $$ /$$$_  $$ /$$$_  $$ /$$$_  $$ /$$$_  $$
 |__/  \ $$| $$$$\ $$| $$$$\ $$| $$$$\ $$| $$$$\ $$
   /$$$$$$/| $$ $$ $$| $$ $$ $$| $$ $$ $$| $$ $$ $$
  /$$____/ | $$\ $$$$| $$\ $$$$| $$\ $$$$| $$\ $$$$
 | $$      | $$ \ $$$| $$ \ $$$| $$ \ $$$| $$ \ $$$
 | $$$$$$$$|  $$$$$$/|  $$$$$$/|  $$$$$$/|  $$$$$$/
 |________/ \______/  \______/  \______/  \______/

INPUT : 17394
This is lib_17394 file.
How do you find vulnerable file?
sh
cat flag
flag{Are_y0u_A_h@cker_in_real-word?}
```

