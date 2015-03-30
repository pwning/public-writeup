## pattern - Reversing 600 Problem - Writeup by Robert Xiao (@nneonneo)

`pattern` lets you manipulate a square, tiled pattern (consisting of 4 different tiles `||`, `--`, `**`, and `  `), representing the tiles internally as packed bytes (2 bits per tile, 4 tiles per byte). The pattern is stored in a static buffer of size 576 (exactly enough for a 48x48 pattern). You can upload a custom pattern, generate a random one, "beautify" the pattern and print it out. Beautifying the pattern mirrors and duplicates the pattern to make a new double-size one with symmetry:

            XYYX
    XY  =>  ZWWZ
    ZW      ZWWZ
            XYYX

The bug in the program is that the beautify function doesn't check that the size is less than 24 before doubling the dimensions. This can cause the size of the resulting pattern to be larger than 576 bytes, overflowing the pattern buffer (by up to 1728 bytes, a huge amount). Since you can upload custom patterns, you can write almost anything you want to memory.

So what's after the pattern buffer? There's a few program values (the pattern author's name, the pattern generator type, and the pattern size), and there's the `.dynamic` section which controls dynamic linking.

First off, we can use the overflow to overflow the pattern size. This is useful to make the pattern bigger without actually writing to it; we can use this to print out the contents of memory (interpreted as a pattern). In particular, we can read the `.dynamic` section, which contains a `DT_DEBUG` pointer that points at `_r_debug` from `ld-linux` - this gives us the base address of `ld-linux`. Note that in order to make the print function properly output the pattern, we also need to write a valid type to the pattern generator type (otherwise the print function will generate a new pattern before printing it, modifying it "by god").

We now want to overwrite `.dynamic` to exploit the program. `.dynamic` is only read at program startup and exit, so we'll need to exit the program in order to trigger the exploit.

It's worth noting that I solved this problem in a substantially easier way than was intended. The intended solution involves overwriting the relocations table of `.dynamic`, causing the linker to make bad relocations at exit (in `_dl_fixup`). However, I found another way.

After performing fixup relocations, the linker calls the function specified in the `DT_FINI` entry of `.dynamic`. With `gdb` we can see that the `DT_FINI` function is called with `edx` set to the address of the `DT_FINI` entry. With a rop gadget finder we find this gem in libc:

     0x000db7b1: push eax ; push 0x00000001 ; push dword [esp+0x34] ; push dword [edx+0x0C] ; call dword [edx+0x24]

This calls the function at `[edx+0x24]` with the value from `[edx+0x0c]` as the first argument, so if we can make `DT_FINI+0x24 = system` and `DT_FINI+0x0c = "/bin/sh"` then we win!

The only thing we need to do now is to make sure `_dl_fixup` doesn't crash before the fini function runs. This is a simple matter of figuring out which entries of `.dynamic` it cares about (which I did just by trial-and-error), and then carefully arranging our pattern so that we overwrite them with the same values they had before. There's some annoying parts where the mirroring of beautify gets in the way, but by adjusting the pattern size it is possible to find a size where everything aligns properly. (Had this not been possible, we would probably have had to figure out how to exploit `_dl_fixup`).

We also don't know the address of libc, only ld. This means we still have to bruteforce to beat the ASLR of libc (well, I was told afterwards that ld and libc differ by a constant, which would have been helpful here :) ).

The final exploit code is in `pwn.py`.

Once we have successfully manipulated the `.dynamic` section into the shape we need, we just ask to exit the program, triggering the finalization process and calling `DT_FINI`. If we guessed the libc address, we get dropped into a shell, and we `cat flag` to get `BCTF{ev3n_g0d_is_n0t_a_s3curity_eXp3rt}`.
