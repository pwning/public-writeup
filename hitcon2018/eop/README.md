# eop - Reversing
## Benjamin Lim (jarsp)

After examining the program we quickly come to the conclusion that 'eop' stands
for 'Exception-Oriented Programming'. The program takes in a 48 byte key, and calls
a main loop three times, once for each of its 16 byte chunks, and writes to
a 48 byte buffer that is compared to another buffer in the program. The loop
consists entirely of 124 exception handlers that raise an exception which triggers
another handler to continue to computation. This makes decompilation annoying
as IDA refuses to decompile past the throw. To get around this we programatically
patch all the functions to skip over the throwing blocks and straight into the catch
block, and chain the end of the catch block into the beginning of the next.
This allows us to extract a decompiled version of the code.

Examining the decompiled code and some of the magic constants in the binary leads
us to believe that it is performing the Twofish cipher. In any case, we noted that
the operations in the cipher are entirely reversible, so extracting out the cipher
into python and reversing it gives the flag.
