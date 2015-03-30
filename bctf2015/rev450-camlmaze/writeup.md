## camlmaze - Reversing 450 Problem - Writeup by Robert Xiao (@nneonneo)

camlmaze is a maze client compiled with a somewhat obscure implementation of Caml called CamlFeatherweight. When run with `camlfwrun bytecode`, it connects to a server and loads a maze from that server. You're supposed to send the list of up/down/left/right moves to get out of the maze, but 90% of the maze is masked out so you can't actually solve it.

So at this point the proper solution would be to use `camlfwod` to dump the bytecode, then reverse it, then disable the masking; or figure out how it decodes the string from the server into a maze. But I don't want to do either of these, so I chose instead to skirt the problem by dumping the memory of the process and looking for interesting things.

As it happens (by simply scrolling through the memory), the entire maze is in the heap, stored as three arrays of 1024 small integers each (each integer is either 1 or 3). Printing out the arrays and comparing them to the masked maze shows that the arrays correspond to the vertical walls, horizontal walls, and mask respectively.

So at this point the solution is quite simple: launch the program, go digging in its memory for these arrays, reconstruct the maze, solve it and submit the solution. Simple! You can see the details in `solve.py`.

Once run, we get the flag quite quickly: `BCTF{meowmeowmeowilikeperfectmaze}`
