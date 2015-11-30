## 0ldskoo1 - Reverse Engineering 180 Problem

### Description

This challenge is an Xbox iso. You run it via the [xqemu](https://github.com/espes/xqemu) xbox emulator, and it plays a 3D animation of the flag. However, most of the flag is obscured by a giant red rectangle that occasionally appears across the screen.

Also: I just noticed that the author of the emulator is also the author of this challenge. No wonder xqemu plays so nice with IDA. <3

### Solution

To solve the challenge, I first used the [extract-xiso](http://sourceforge.net/projects/extract-xiso/) tool to get a binary that IDA could load. xqemu preserves qemu's remote gdb support, so a normal IDA debugging setup works great here.

Akin to most game-console reversing challenges, the Xbox binary contains a bunch of library code and it's not immediately obvious where the real challenge starts. In effort to find the application code relevant to this CTF challenge, I attempted to find the program's "main loop" by stepping through execution in IDA. There is indeed such a loop, at `loc_DECD4`; it updates the display by one frame each iteration.

I looked at some subroutines called by the loop and decided that this was in fact non-library code: in particular, in `sub_DC130`, there's a `sin((dword_123B0 % 600) * 6.283185307179586 / 600.0)` that I think implements the panning in the animation. So, I decided to stick around this area for both static reversing and some dynamic tampering in the debugger to help figure out what bits of code did what.

Previously, upon first seeing the 3D animation, I'd imagined that a possible way of solving this challenge would be to disable the rendering of the red rectangle. So, I was on the lookout for something like

     1. A graphics subroutine call that defined a rectangle.
     2. Any value specifying the color red, like 0x0000FF or 0xFF0000 or 0xFF0000FF.

Sure enough, inside `sub_DC440` (called from the main loop), there's a `if(...) sub_D3A20(0, 125, 640, 150, 0xFF0000);` statement. This kinda looks like a graphics call that configures a big red rectangle. Additionally, the fact that the call is inside a conditional corresponds with the fact that the obscuring rectangle occasionally disappears. Happily, patching out the function call entirely prevented the rectangle from ever showing up, allowing the flag to be read by just playing the animation.

For people trying this at home: I patched the binary using IDA's editing features, and then fed that binary to extract-xiso to produce an ISO runnable in xqemu.
