## RamG-thunder – Reversing Challenge

RamG-thunder was a Windows command-line utility that posed as some kind of XORing-tool.

By activating a secret menu item, you'd be taken through a series of checks including:

* Must enter passwords that match xor-obfuscated `strncmp()`s
  - Process would fail if the strncmps didn't match.
* Some basic anti-debug checks
  - Could be bypassed by jumping over them
  - or just by doing stuff statically and not using a debugger! :P
* Some Window registry checks
  - Process wouldn't necessarily fail if you missed these...
  - ...but the results were used to build an XOR key.

Some of these checks would immediately fail the process, and some of these checks went towards building an XOR key. If the failing-checks were passed, the XOR key would be used to decrypt a data blob and drop a file.

It wasn't obvious how to pass the Windows registry checks to build the correct XOR key. I settled for not modifying my registry at all, and just inverting all the relevant conditional branches while running under a debugger.

The dropped file 'c' was a PNG file, however it was dropped under a slightly-wrong XOR key (presumably, because I passed those registry checks incorrectly) and was therefore corrupt. However, because the PNG file format has a relatively long header, I could determine some bytes of the XOR key that were likely wrong. Guessing what those PNG header bytes should have been (just taking bytes from a valid PNG file was sufficient) and guessing the length of the XOR key allowed me to correct 'c' into a valid PNG file. (It was fortunate for me that the XOR key was short and that the only incorrect bytes being used for it were near the front.)

'c' was a picture of the flag, 'ThANk_yOu_my_PeOP1E'.
