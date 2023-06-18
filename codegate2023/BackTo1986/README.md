# BackTo1986

We're given a breakout game where each level spells out one character of the flag.

We can start by extracting the given `initramfs.cpio.gz`. In it, we find that it runs the program `main`.

The game uses `tfblib` for drawing to the framebuffer. Identifying the library functions lets us track
down where stuff is being drawn. (For example, brick drawing uses `tfb_fill_rect` and `tfb_draw_rect`.)

We patched the following:
- Immediately win each level (`0x4024f7: cmp eax, 1 -> cmp eax, 2`)
- Make the block outlines 1x1 so they're less distracting (`0x401a0c`, `0x401a11`)
- Change the block colors so the flag character is more visible (`0x403f7f`~`0x403fc2`)
- Move the status text below the blocks (`0x401bf8`)

![Screenshot of patched game](screenshot.png)

We then repacked `initramfs.cpio.gz` then played through the game to read all 255 (WTF?) characters of the flag.
