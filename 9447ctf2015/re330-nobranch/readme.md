## nobranch - Reverse Engineering 330 Problem

### Description

Challenge text:

```
$ ./nobranch `cat flag.txt`
HMQhQLi6VqgeOj78AbiaqquK3noeJt
```

This challenge is a binary that mangles a text input into a text output; we're supplied the mangled flag, and are supposed to find the input that produced that. The conceit of this challenge is that the main() function is a single giant basic block, without any branch instructions nor conditional instructions.

### Solution

I decided to try throwing Z3 at this challenge and hope for the best. Simultaneously, my teammates attempted to transform the program into something more reversible, so we had all the angles covered!

I wrote some python that would parse the dumped asm of the main() function into solver constraints. Both the script and the dumped asm---which I edited manually for easier parsing, especially around the mem reads from the text input and the mem writes to the output buffer---are included alongside this writeup.

Educational aside: there are several great libraries for lifting x86 code to solver constraints out there. You don't need to roll your own. (But in a CTF, sometimes I'd rather wrestle with my own shitty python than someone else's library :P).

I didn't have any luck with the Z3 solver (although I heard later that it worked great for other teams), so I ported my code to use [Boolector](http://fmv.jku.at/boolector/). Boolector worked fine for me---~30 min solve time on my laptop. SMT solving is a capricious beast.
