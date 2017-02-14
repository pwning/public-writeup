## angrybird – Reversing Challenge

angrybird was a traditional keygenme-style reversing challenge. It had some weird exits at the beginning, which the program strings themselves told you to patch out. Not sure what that was about, but it didn't really affect the problem.

We solved this challenge by taking the Hex-Rays output, regex-replacing
```
  if \( ([^\n]*) \)
  {
    puts\("melong"\);
    exit\(1\);
  }
```
to `S.add(Not( $1 ))`, and then cleaning it up into the attached z3py solve script angry.py.

The program did some reading & aserting of the GOT, which is reflected at the top of the solve script, but it didn't really end up mattering too much (i.e. leaving all those bytes as purely symbolic results in the correct flag being generated).

The intended way to solve this problem was, of course, to use angr. But this way was fast too :P
