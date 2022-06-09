# type: ignore
from typing import Sequence, Tuple
from pwn import *
from skyfield.api import EarthSatellite, load
import numpy as np
from datetime import datetime

c = 299792.458

context.log_level = "debug"

host, port, ticket = "crosslinks2.satellitesabove.me", 5400, "ticket{echo230480mike3:GPLZjchtEWd8KTAsSz6gzQhxtsrLatEFOTPIMbrRS-AhQhdeJ0kD3wLgxvdBNhynQw}"

conn = remote(host, port)
conn.recvuntil(b"Ticket please:\n")
conn.sendline(bytes(ticket, "utf-8"))

def solve_position(observations: Sequence[Tuple[np.ndarray, float]]) -> np.ndarray:
	# apriori = np.array([6660.038200176077,-2063.0071762787684,-12.046236588299507, 0])
	apriori = np.array([0,0,0,0])

	while True:
		A = np.array([
			[
				(apriori[0] - obs_pos[0]) / np.linalg.norm(apriori[0:3] - obs_pos),
				(apriori[1] - obs_pos[1]) / np.linalg.norm(apriori[0:3] - obs_pos),
				(apriori[2] - obs_pos[2]) / np.linalg.norm(apriori[0:3] - obs_pos),
				c
			]
			for obs_pos, obs_rho in observations
		])

		b = np.array([
			obs_rho - np.linalg.norm(apriori[0:3] - obs_pos) - c * apriori[3]
			for obs_pos, obs_rho in observations
		])

		x = np.linalg.lstsq(A, b, rcond=None)[0]
		print(apriori, x)
		apriori = apriori + x * 0.01

		if np.linalg.norm(x) < 1e-9:
			break

	return apriori[0:3]

while True:
	conn.recvuntil(b"TLE\n")

	satellites = {}

	ts = load.timescale()

	for i in range(81):
		name = conn.recvline().strip().decode("utf-8")
		l1 = conn.recvline().strip().decode("utf-8")
		l2 = conn.recvline().strip().decode("utf-8")
		satellites[name] = EarthSatellite(l1, l2, name, ts)

	# print(satellites)

	observations = {}
	observation_t = None

	for i in range(81):
		conn.recvuntil(b"Observations ")
		target_name = conn.recvline().strip().decode("utf-8")
		conn.recvline()
		t_str, d_str, v_str = conn.recvline().decode("utf-8").split(", ") # e.g. 2022-01-26T09:10:36.138301+0000
		time = datetime.strptime(t_str, "%Y-%m-%dT%H:%M:%S.%f%z")
		d = float(d_str)
		v = float(v_str)
		t = ts.from_datetime(time)
		observations[target_name] = (d, v)

		if observation_t is not None:
			assert t == observation_t
		else:
			observation_t = t

	position_observations = []

	for target_name, (d, v) in observations.items():
		pos = satellites[target_name].at(observation_t).position.km
		position_observations.append((pos, d))

	position = solve_position(position_observations)

	velocity = [0.8502321732312385,4.578060492208078,6.085759610702348]

	conn.recvuntil(b"What's my position: x,y,z\n")
	conn.sendline(f"{position[0]},{position[1]},{position[2]}".encode())
	conn.recvuntil(b"What's my velocity: vx,vy,vz\n")
	conn.sendline(f"{velocity[0]},{velocity[1]},{velocity[2]}".encode())


conn.interactive()