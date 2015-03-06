## Alewife - Pwning 400 Problem - Writeup by Robert Xiao (@nneonneo)

This problem took a little while to reverse. Basically, it implements a variety of array operations on three kinds of arrays: `string` arrays, `int` arrays and `mixed` arrays (arrays whose elements can be either `string` or `int`). 32 instances of each type of array are preallocated in BSS, each with capacity for 256 elements.

On the `string` and `int` arrays, it is possible to append elements, pop elements off the end, print the array, and sort the array. In order to create a `string` or `int` array, you have to first create a `mixed` array with only one type of data, then use the copy operation to copy the `mixed` array out into a new `string` or `int` array.

One major bug lies in the sorting routine. The same bug is in both the `string` and `int` sorting routines, but the `int` sorting routine is easier to exploit. Basically, the sort contains an off-by-one error and will include the element one past the end of the array in the sort. In each of the array objects, the QWORD immediately after the preallocated 256-element array is a pointer to the start of the array, so by including this QWORD in the sort, you can push an almost arbitrary element into this pointer position. This can be triggered simply by inserting 256 elements into any array (the maximum size permissible), then sorting the array.

Overwriting the array pointer enables almost arbitrary writes (by pointing that pointer somewhere interesting, like the PLT table, then triggering an array insertion). The catch is that the value used to overwrite the start of the array has to be bigger than the pointer itself. In my case, I used the address of the second word in the array (the element at index `1`) -- this has the effect of simply shifting the array over by one place. This places the array pointer at array index 255, which makes it possible to overwrite the array pointer with a truly arbitrary value via simple array insertion.

We can then point the array pointer at the PLT. Printing out the array lets us obtain useful `libc` addresses. Then we can just overwrite any PLT entry with an array insertion. We choose to overwrite the PLT entry for `strlen` with the address of `system`, then trigger an operation that involves a string entry (in our case, a previously-inserted string entry of `"/bin/sh"`). Voila: a shell, and shortly thereafter a flag.

For full details see `pwn.py`.
