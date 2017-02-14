## HelloProtector – Reversing

The program is protected with WinLicense, but it didn't seem to have many protection options on.
We were able to just run/attach the program and analyze it.

Essentially, the program checks if the volume name of the C: drive is a certain string by xor'ing with the key.
