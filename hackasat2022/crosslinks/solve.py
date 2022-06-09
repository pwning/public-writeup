# type: ignore
from pwn import *
from collections import defaultdict
from random import random
from skyfield.api import EarthSatellite, load
import numpy as np
from datetime import datetime

context.log_level = "debug"

host, port, ticket = "crosslinks.satellitesabove.me", 5300, "ticket{foxtrot251655whiskey3:GJs6DkwHX--L4IKX3Xus_mKOHZ66y2BxS326fnIenHp9rihAPow4-yuDsYuXEiFAqw}"

conn = remote(host, port)
conn.recvuntil(b"Ticket please:\n")
conn.sendline(bytes(ticket, "utf-8"))

while True:
	conn.recvuntil(b"TLE\n")

	satellites = {}

	ts = load.timescale()

	for i in range(75):
		name = conn.recvline().strip().decode("utf-8")
		l1 = conn.recvline().strip().decode("utf-8")
		l2 = conn.recvline().strip().decode("utf-8")
		satellites[name] = EarthSatellite(l1, l2, name, ts)

	print(satellites)

	conn.recvuntil(b"Observations ")
	target_name = conn.recvline().strip().decode("utf-8")
	conn.recvline()
	t_str, d_str, _ = conn.recvline().decode("utf-8").split(", ") # e.g. 2022-01-26T09:10:36.138301+0000
	time = datetime.strptime(t_str, "%Y-%m-%dT%H:%M:%S.%f%z")
	d = float(d_str)
	t = ts.from_datetime(time)

	target = satellites[target_name]

	print(target_name, t)

	closest = ""
	closest_delta = float("inf")

	for sat in satellites:
		dist = np.linalg.norm((satellites[sat] - target).at(t).position.km)
		delta = abs(dist - d)
		print(sat, dist)
		if delta < closest_delta:
			closest_delta = delta
			closest = sat

	conn.sendline(closest)

# conn.interactive()