## watermelon - Pwnable 210 Problem

We are given some sort of menu-based playlist management service. An
array of 100 playlists is initialized on the stack. Each playlist entry
contains and id and two buffers of size 20 for the music and artist
names. The function for modifying a playlist had a trivial buffer
overflow that writes up to 0xc8 bytes to the 20 byte artist name buffer.
None of the read functions null terminate.

The exploit creates 100 playlists. This is incredibly slow due to the
connection to Korea being poor, and the readuntil function reading a
single byte at a time. I should really write a better readuntil
function, as it would have saved several minutes of time. Anyway, the
exploit then uses the buffer overflow to leak the stack canary and the
return address of main (inside of `__libc_start_main`), by writing As up
to the start of the leak target and printing the playlists.

The exploit then uses the overflow to smash the stack. It sends the
command to exit the service, which causes the program to return to libc
calling `system("/bin/sh")`.
