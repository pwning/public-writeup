# Printf

We are given a binary that contains a custom `printf` implementation. It asks for a string, calls `printf` on it, asks for another string, calls `printf` on it, and then exits. This custom printf implementation does not have the `%n` modifier, so we need to work a bit harder to exploit this.

The custom `printf` function first computes the expected size of the output string, uses `alloca` to allocate a stack buffer for it based on the computed size, and then does another pass to populate the stack buffer with the output string. Finally, it calls `puts` on the allocated buffer. There are some checks to check for the allocated length being negative, but is otherwise unbounded. Therefore, by controlling the length of the string, we can force `rsp` to point over some interesting region of memory and then write to it.

We can control the size of the output string using the width sub-specifier (e.g. `%100x`), which accepts any postive `int64`. However, if we do so, the `printf` will eventually write over unmapped memory and crash. Fortunately, the handling of invalid specifiers like `%y` differs between the first pass (length computation) and the second pass (filling in the string). The first pass simply ignores invalid format specifiers, which the second pass immediately returns -1 from `printf` upon reaching said specifier. Therefore, we can use a format string like `ABCD%y%1000000x` to write a small number of bytes to a controlled location.

Finally, we use trial and error to figure out the correct libc and stack offsets on the server. We then leak the stack and libc addresses, write magic to the `AT_EXIT` hook, (which happens to still be present in 2.29), and get shell.

`TWCTF{Pudding_Pudding_Pudding_purintoehu}`