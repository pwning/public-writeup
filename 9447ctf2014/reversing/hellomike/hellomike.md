hellomike

hellomike.beam is an Erlang bytecode file. A quick `escript hellomike.beam` will run it and reveal this to be a find-the-serial style challenge.

It doesn't look like any Erlang bytecode decompilers exist (except for debug .beam files, which hellomike.beam is not), but we'd at least like to disassemble this into mnemonic form. Some googling reveals that Erlang has a built-in disassembler:

```
$ erl
Erlang/OTP 17 [erts-6.2] [source] [64-bit] [smp:8:8] [async-threads:10] [hipe] [kernel-poll:false]

Eshell V6.2  (abort with ^G)
1> io:format("~p~n",[beam_disasm:file("hellomike.beam")]).
{beam_file,hellomike,
           [{main,1,318},{module_info,0,342},{module_info,1,344}],
           [{vsn,[175001235647749787802935055027724804216]}],
           [{options,[{outdir,"/tmp"}]},
           ...
           {test,is_nonempty_list,{f,340},[{x,0}]},
           {get_list,{x,0},{x,1},{x,2}},
           {test,is_nil,{f,317},[{...}]},
           {allocate_zero,6,2},
           {move,{literal,...},{...}},
           ...
```

The `io:format` bit removes the pretty-priniting limits; otherwise, the actual output would contain ellipses similar to the above.

Niche languages always suffer from a lack of documentation, but I found an only slightly out-of-date writeup of how the BEAM VM works and its opcodes.
http://synrc.com/publications/cat/Functional%20Languages/Erlang/beam.txt
(Note that, compared to the beam_disasm output, argument order is somtimes different and there are missing opcodes.)

Other documentation I used was http://www.erlang.org/doc/man/erlang.html, which describes the {extfunc,erlang,\<func name\>,\<arity\>} calls.

There are 6 functions defined in hellomike.beam: nfa_0, nfa_1, nfa_2, nfa_3, nfa_4, and main (and also a handful stubs which just forward to these or whatever). An NFA is http://en.wikipedia.org/wiki/Nondeterministic_finite_automaton, so presumably main uses a couple finite state machines to decide whether to accept the input or not. This means that trying to solve this challenge dynamically using methods like instruction counting are probably not going to work; we need to extract the state machines and solve for a satisfying input (specifically, we're told in the problem text that the flag is the lexically-first shortest satisfying input).

Let's start with these nfa_x functions. Sure, there's 4K lines of disasm worth of them; but if you diff, say, nfa_0 and nfa_1, you'll realize that they all have exactly the same structure.

Every nfa_x function contains several statements like
```
                       {select_val,{x,3},
                                   {f,56},
                                   {list,[{integer,51},
                                          {f,7},
                                          {integer,65},
                                          {f,8},
                                          {integer,70},
                                          {f,9},
                                          {integer,49},
                                          {f,10},
                                          {integer,67},
                                          {f,11},
                                          {integer,54},
                                          {f,12}]}},
```
The `{f,7}` thingies are code-label references, so what we're looking at is basically a switch statement over ASCII characters! Looking at the other such switch statements, all the ASCII codes used in the bytecode are for characters from [0-9A-F].

Furthermore, besides a preamble and those switch statements each nfa_x function is pretty much *entirely* comprised of chunks that all look like
```
                       {label,7}, %% A target of one of the switch statements
                       remove_message,
                       {test_heap,3,5},
                       {bif,self,nofail,[],{x,0}}, %% Sets the message target to "self"
                       {put_tuple,2,{x,1}},
                       {put,{integer,2}},
                       {put,{x,4}},
                       {line,3},
                       send, %% Sends the message (2, {x,4}). For every chunk, this is (<NFA vertex>, string[1:])
                       {move,{y,1},{x,0}},
                       {call_last,1,{hellomike,nfa_0,1},2}, %% A recursive tail-call to the begining of the function.
```

So, modulo some details, these nfa_x functions are all just recursive loops that repeatedly case on characters. Presumably, they're doing something like iterating over a string, and repeatedly matching its characters.
Some of these chunks `send` several different tuples before recursing with `call_last`; the effect is, multiple choices are enqueued in the message queue for future exploration. This is nicely in line with the theory that these functions are NFAs.
Lastly, some of the chunks end with
```
                       {put,{atom,success}},
                       {move,{y,1},{x,0}},
                       {line,66},
                       send,
                       {deallocate,2},
                       return,
```
instead of recusing via `call_last`. These probably represent accept states.

At this point, I dove into the details of the Erlang BEAM and just hand-reversed the program. Even though the disassembler initially spit out 4000 lines, thanks to the repetitive structure noted above there were only about 100 unique lines to reverse.
After reversing, I knew each nfa_x function to be equivalent to:
```
table_x = { # Example table; real tables have more entries.
  0: {'A' : [0], 'B' : [1], 'C' : [0,1,2]},
  1: {'1' : [2,3], '2' : [0]},
  2: {'8' : [0]}
}
table_x_accept = {1, 2} # If the string becomes empty on these vertices, the NFA accepts the string.
def nfa_x():
  queue = [(0, argv[1])] # The first item is inserted by the Erlang `main`
  while queue:
    vertex, input = queue.pop(0)
    if len(input) == 0:
      return SUCCESS if vertex in table_x_accept else None
    t = table_x[vertex].get(input[0])
    if t is not None:
      queue.extend((i,input[1:]) for i in t)
  return None
```

This is very recognizably an NFA implementation ^_^

A reading of `main` reveals that it sequentially goes through nfa_0 thru nfa_4, providing the initial tuple `(0, argv[1])` to each nfa, and waiting for the nfa to send back `{atom,success}`. As you'd expect, it requires each of the five nfa_x functions to have reached an `{atom,success}` before printing out `"This matches, but is this the lexicographically smallest shortest string? ;)"`.

At this point, I used regex-fu to lift the NFAs to Python data structures as dictinaries of `(vertex, edge-charcter): [target vertices]`. (This isn't as nice as the Python representation I gave above, but hey, I was in the middle of a CTF!)
```
success = 9999 # Vertices to represent accept state or fail state.
failure = 1234

nfa_0 = {
  ...
  (1, '9'): [2],
  (1, '1'): [2],
  (1, '8'): [2],
  (2, '\x00'): [failure], # I use '\x00' to represent the last edge to success or failure.
  (2, 'A'): [3],
  (2, '3'): [1],
  (2, '1'): [0],
  (2, 'C'): [1, 3],
  (2, 'F'): [1, 3],
  (2, 'E'): [0, 3],
  ...
}
```

We can view the space to expore as a big directed graph, who's vertices are the cartesian product of each NFA's vertices. With NFAs represented as above, the neighbors of any vertex can be found via:
```
nfas = [nfa_0, nfa_1, nfa_2, nfa_3, nfa_4]
from itertools import product
def neighs(v):
  ret = []
  for c in '0123456789ABCDEF\x00':
    try: ret.extend(product(*[nfas[i][(v[i], c)] for i in range(5)]))
    except: pass
  return ret
```

A Dijksta search from `(0,)*5` (the start state visible in the `main` function) to `(success,)*5` yields "5136418B11816E". This indeed passes the `escript hellomike.beam 5136418B11816E` check, so we're close! We know the shortest accepting string is len("5136418B11816E") == 14, so to get the lexically first shortest string, we just switch from Dijkstra search to a lexically-ordered depth-first search which truncates at a depth of 14. This doesn't take long to find the flag, even in python :)
