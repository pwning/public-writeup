## Online Nonogram

### Bug
While adding a new puzzle, the program would read the puzzle first into a global array without check the size of input, and then copy expected number of bytes (not the actual number of bytes given as input) to the dynamically allocated memory. Since the global array was of 1024 bytes, which wass immediate

### Solution

We first make a new puzzle of size n = 96, such that `(n*n << 3) > 1024`, and give 1024 bytes as input (all null except for the last 12 bytes - which are 0xff). This will copy more than 1024 bytes into the allocated memory, thus copying the heap address where the vector is pointing to. While playing the newly added puzzle, it first prints the board in the column-major order (print number of consecutive 1's) and here our input basically makes it easy for us to recover the vector pointer addresses from just the column-major order, and we can go back to the menu by giving bad input so `scanf("%d %d",...)` fails.

Once we have a heap leak, we forge our vector by overflowing the global buffer again and create some fake Puzzle structures (make the name string point to the location we know libc address will be written to) all while adding a single new puzzle. Now, on freeing a large chunk, we can get the libc address in the heap - where we had puzzle string pointer pointing to, and on doing show puzzle, we can leak the libc address.

Once we have heap leak and libc leak, we try to corrupt the tcache free list to get allocation on top of `__free_hook`, to get the `system("/bin/sh");` by first freeing 2 (or more) 0x30 size chunks (size chosen randomly such that it is not commonly used) under our control (since we control the Puzzle structure and the pointers in it), and then overwriting the entire 0x30 size chunk (while they are in the freed state). For this, we had faked some 0x30 size chunks (that we freed) inside a large chunk (so it can be freed and reallocated to overwrite over the freed 0x30 size chunks). While overwriting the tcache free list, we write the free hook address as the next pointer to get allocation on top of the free hook and write the system address over there. This works because 2.31 libc assumes that the tcache free list isn't corrupted while allocating, it only does the check while doing free. After overwriting the free hook address, freeing any memory with `/bin/sh\x00` at the start will give the shell.

