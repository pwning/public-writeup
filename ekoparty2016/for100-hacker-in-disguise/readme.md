## Hacker in Disguise - Forensics 100 Problem

### Description
We have captured these codes in a secret communication, please tell us its meaning. 

### Overview
The given file is a capture of a HID (Human Interface Device), particularly a USB keyboard. With a HID code set/mapping,
we can translate the HID capture to actual keypresses, which ends up being the typed-out flag.

### Solution
We're given a file called **TIC.txt**. To anyone unfamiliar with USB HID captures, it's really hard to figure out where
to even start with this problem.

After a lot of searching with different text in the given file, we might find something like 
https://deskthority.net/workshop-f7/xt-at-ps2-terminal-to-usb-converter-with-nkro-t2510-270.html or 
https://www.reddit.com/r/MechanicalKeyboards/comments/2o25pm/simplified_instructions_for_programming_teensy/.
We can figure out from this that this is perhaps a capture of a USB keyboard, with the different lines being keypresses
that we need to decode.

Some HID USB keyboard code sets/mappings we could use include the following:
* [Soarer's Converter documentation (docs > codes)](https://geekhack.org/index.php?topic=17458.0)
* [TMK HID code set definition file](https://github.com/tmk/tmk_core/blob/master/common/keycode.h)
* [TMK keycode symbol table](https://github.com/tmk/tmk_core/blob/master/doc/keycode.txt)

Pretty much, anytime you see a +<hexByte>, the key corresponding to <hexByte> is pressed down. Similarly, anytime you see
a -<hexByte>, the key corresponding to <hexByte> is released. -<hexByte> can be important when keys like SHIFT are pressed,
as it might make the difference between lower/uppercase letters and different symbols.

Decoding TIC.txt, we get the following keypresses. Note that something like <LSHIFT-down> indicates LSHIFT being pressed
down and <LSHIFT-up> indicates LSHIFT being released.
"this is your flag <RSHIFT-down>EKO<RSHIFT-up><LSHIFT-down>{<LSHIFT-up>holapianola<LSHIFT-down>}<LSHIFT-up><LCTRL-up>c"

From this we get our flag, **EKO{holapianola}**.
