# type: ignore
from pwn import *
from collections import defaultdict

context.log_level = "debug"

host, port, ticket = "bitflipper.satellitesabove.me", 5100, "ticket{kilo724075quebec3:GHzGbhQyAzk0-vCEHXkseedkyaz6UWKGe81DO24euHhgDqz3TyBpnjMUq5S_FXFNZg}"

freq = defaultdict(lambda: 0)
conspiracy = [1]

for i in range(15):
	last = conspiracy[-1]
	conspiracy.append(last ^ (last << 1))

conn = remote(host, port)
conn.recvuntil(b"Ticket please:\n")
conn.sendline(bytes(ticket, "utf-8"))
print("sent ticket")

for i in range(3):
	val = 16
	while True:
		conn.recvuntil("Guess: ")
		conn.sendline(str(conspiracy[16 - val]))
		out = conn.recvline().strip().decode("utf-8")
		if "Reset" in out:
			continue
		val = int(out)

conn.interactive()
