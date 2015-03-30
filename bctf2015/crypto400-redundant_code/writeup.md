redundant_code is a reversing + crypto challenge, that comes with a binary `redundant_code` and a 30MB text blob `code.pub`.

Reversing the binary is fairly straightforward: the `redundant_code` binary takes argv[1], uses it to construct an array of linked lists, applies some transformation to that data structure twice, and pretty prints the result. A python implementation of the binary, `redundant.py`, is included with this writeup.

The 30MB text blob `code.pub` supplied with the problem is an output from the program. So, we have received the output of `./redundant_code $FLAG`, and must recover that input argument. 

After reflecting on the algorithm, it's clearly best interpreted as graph manipulation. The input is encoded as a graph: for each character `c` of the input, there's a star graph of degree `ord(c)-ord('0')`, and the roots of these star graphs are joined into a path in the order that the characters appear in the string (plus one additional 'head' vertex). Then, the [line graph](http://en.wikipedia.org/wiki/Line_graph) of that graph is taken twice. So, you've been given `L(L(<star graphs>))`, and you want to recover the original star graphs.

According to the Wikipedia page, there are linear-time algorithms for recovering the original graph from line graphs, but during the CTF I didn't realize that "line graphs" were a standard thing. So, after spending a few hours trying and failing to come up with these algorithms on my own, eventually I discovered that a simple brute-force approach could solve the challenge. The brute forcer is included, `lolgraph.sh`. Running it in the same directory as the challenge files will produce the flag.

This brute-forcer is literally just running `./redundant_code ${FLAGPREFIX}[A-Za-z0-9_{}]` and choosing the character with output that best matches `code.pub`. Cute, right? I'd been working on a more sophisticated brute-forcer that did subgraph-hunting, when I noticed that this would probably work due to the way vertices are given ids when pretty-printed by the `redundant_code` binary.
