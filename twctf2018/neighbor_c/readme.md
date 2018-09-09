## Neighbor C - Pwn - Writeup by Benjamin Lim (@jarsp)

### Description

Neighbor C is a simple amd64 binary that repeatedly copies the user input into a BSS array, and then `fprintfs` the user input to stderr. However, only the output of stdout is visible over the connection.

### Solution

The `fprintf` gives us an obvious blind printf vulnerability. We exploit this is two parts.

The first step is to redirect stderr to stdout to get output from the printf. This is possible as the `stream` argument (`stderr`) to `fprintf` is being stored on the stack. The plan is to do a partial overwrite of a single byte (using `%hhn`) through the saved `rbp` to make the next `rbp` point to the saved `stderr` on the stack. After that we do another partial overwrite of 2 bytes through the next saved `rbp` to modify the `stderr` pointer to `stdout` (which is possible as they are close together in `libc`).

It turns out that because of the layout of the stack the address of `stderr` on the stack is always 8 `mod` 16, while the saved `rbp` pointers are at 0 `mod` 16. This means that we can guess the last byte of the address of the saved `stderr` from 0xf8 downwards without crashing the program. This means that per run we only have to guess 1 nibble of aslr to redirect the IO, roughly 1 in 16 runs. The script also has some optimization to minimize time wasted due to the `sleep` calls in the program.

The second step is then to get a shell. The calling function doesn't return so this is a bit troublesome. We leak libc and stack address. We then use the same trick to write the address of a libc gadget just below the saved return address of the `fprintf` call on the stack. We also zero out another 8 bytes on the stack to make the libc gadget work. Finally we overwrite the last two bytes of the `fprintf` return address to point to a `ret` instruction in the program. The second `ret` triggers the shell.

    TWCTF{You_understand_FILE_structure_well!1!1}

(so it seems like the intended solution for the second part was to exploit the IO file structures... :p)
