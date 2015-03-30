## securecom - Reversing 100 problem - Writeup by Robert Xiao (@nneonneo)

This is a pair of programs, one "client" and one "server". Since there's no network server in the problem, the solution must be entirely in the binary.

The server registers a COM object and provides interfaces which the client calls. There are five relevant functions which are called in order by the client.

The first sets a flag in the server if the client passes a particular string (which you supply) - `SOSIMPLE`. For no apparent reason I couldn't pass this check (even after patching the binary to change the default buffer size), so I opted to just reverse the other four functions.

These functions are actually really simple: they just load the client's buffer with the pieces of the flag, one function at a time. By just comparing the client and the server to figure out which functions are called when, it is straightforward to recover the full flag: `BCTF{gZ4KVRz1lGFLH6kPujwORTe9NG9I3LCa}`
