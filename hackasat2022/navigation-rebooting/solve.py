# type: ignore
import itertools
from typing import Sequence, Tuple
from pwn import *
from collections import defaultdict
from random import random
from skyfield.api import EarthSatellite, load
import numpy as np
from datetime import datetime
from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d

context.log_level = "debug"

host, port, ticket = "crosslinks2.satellitesabove.me", 5400, "ticket{echo230480mike3:GPLZjchtEWd8KTAsSz6gzQhxtsrLatEFOTPIMbrRS-AhQhdeJ0kD3wLgxvdBNhynQw}"

conn = remote(host, port)
conn.recvuntil(b"Ticket please:\n")
conn.sendline(bytes(ticket, "utf-8"))

def triangulate(observations: Sequence[Tuple[np.ndarray, float]]) -> np.ndarray:
	# Least squares solution
	q, qdist = observations[0]
	observations = observations[1:]

	A = np.array([
		np.concatenate([2 * (r - q), np.ones(1)])
		for r, rdist in observations
	])

	b = np.array([
		[(qdist ** 2 - np.linalg.norm(q) ** 2) - (rdist ** 2 - np.linalg.norm(r) ** 2)]
		for r, rdist in observations
	])

	print(A)
	print(b)

	x, resid, rank, s = np.linalg.lstsq(A, b, rcond=None)
	print("x:", x)
	print(resid)
	return x.reshape((4,))[0:3]

def solve_velocity(observations: Sequence[Tuple[np.ndarray, float]]) -> np.ndarray:
	A = np.stack([np.concatenate([row, np.ones(1)]) for row, _ in observations])
	b = np.array([val for _, val in observations])
	x, resid, rank, s = np.linalg.lstsq(A, b, rcond=None)
	print(A)
	print(b)
	print("x:", x)
	print(resid)
	return x.reshape((4,))[0:3]

def plot_sphere(center, radius, axes):
	u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
	x = radius * np.cos(u) * np.sin(v) + center[0]
	y = radius * np.sin(u) * np.sin(v) + center[1]
	z = radius * np.cos(v) + center[2]
	axes.plot_wireframe(x, y, z, color="red", alpha=0.2)

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
		d = float(d_str) - 15 # note: the "-15" here came from the other solver
		v = float(v_str)
		t = ts.from_datetime(time)
		observations[target_name] = (d, v)

		if observation_t is not None:
			assert t == observation_t
		else:
			observation_t = t

	fig = plt.figure()

	ax_p = fig.add_subplot(211, projection='3d')
	ax_p.set_xlabel("x")
	ax_p.set_ylabel("y")
	ax_p.set_zlabel("z")

	ax_v = fig.add_subplot(212, projection='3d')
	ax_v.set_xlabel("x")
	ax_v.set_ylabel("y")
	ax_v.set_zlabel("z")

	index = 0

	position_observations = []

	for target_name, (d, v) in observations.items():
		pos = satellites[target_name].at(observation_t).position.km
		position_observations.append((pos, d))

		if index < 5:
			plot_sphere(pos, d, ax_p)

		index += 1

		# vel_circ = plt.Circle(vel, v, color="b", fill=False)
		# ax.add_artist(vel_circ)

	# print(position_observations)
	position = triangulate(position_observations)

	velocity_observations = []

	for target_name, (d, f) in observations.items():
		p = position
		q = satellites[target_name].at(observation_t).position.km
		qvel = satellites[target_name].at(observation_t).velocity.km_per_s

		pq = (q - p)
		pqhat = pq / np.linalg.norm(pq)

		velocity_observations.append((pqhat, qvel.dot(pqhat) - f))

	velocity = solve_velocity(velocity_observations)
	max_dist_error = 0
	max_vel_error = 0

	for target_name, (d, v) in observations.items():
		pos = satellites[target_name].at(observation_t).position.km
		vel = satellites[target_name].at(observation_t).velocity.km_per_s
		pq = (pos - position)
		actual_dist = np.linalg.norm(pq)
		pqhat = pq / actual_dist
		actual_vel = (vel - velocity).dot(pqhat)
		dist_error = abs(actual_dist - d)
		vel_error = abs(actual_vel - v)
		max_dist_error = max(max_dist_error, dist_error)
		max_vel_error = max(max_vel_error, vel_error)
		print()
		print(target_name)
		print("  position:", pos)
		print("  velocity:", vel)
		print("  expected distance:", d)
		print("  actual distance:  ", actual_dist)
		print("  distance error:   ", dist_error)
		print("  expected velocity:", v)
		print("  actual velocity:  ", actual_vel)
		print("  velocity error:   ", vel_error)

		if dist_error > 10:
			print("  DIST_ERROR")

		if vel_error > 0.1:
			print("  VEL_ERROR")

	print()
	print("max dist error:", max_dist_error)
	print("max vel error:", max_vel_error)

	ax_p.scatter(position[0], position[1], position[2], color="green")
	ax_v.scatter(velocity[0], velocity[1], velocity[2], color="green")

	conn.recvuntil(b"What's my position: x,y,z\n")
	conn.sendline(f"{position[0]},{position[1]},{position[2]}".encode())
	conn.recvuntil(b"What's my velocity: vx,vy,vz\n")
	conn.sendline(f"{velocity[0]},{velocity[1]},{velocity[2]}".encode())

	ax_p.autoscale_view()
	ax_v.autoscale_view()
	# plt.show()

# conn.interactive()