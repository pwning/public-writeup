import os, sys
from pwn import *

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")
context.log_level = 'warning'    # 'debug' 'info' 'warning' 'error' 'critical'

ef = sys.argv[1]
s = os.path.getsize(ef)
with open(ef, "rb") as f:
    d = f.read()

# nc 198.11.180.84 6666
r = remote("198.11.180.84", 6666)
r.recvline()
r.sendlineafter(":", str(s).encode() + b"\n" + d)
r.interactive()
