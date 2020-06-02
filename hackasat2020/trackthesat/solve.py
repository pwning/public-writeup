#!/usr/bin/env python3
from pyorbital.orbital import Orbital
from datetime import datetime, timedelta
from time import sleep
import socket

tle_path = "./active.txt"
ticket = b"ticket{oscar21289india:GNa1--OU2pfEIF7G00MnKc-q_ejS-MWUhEtjslW5NQYurtES2gIJUGwR20QAYk2HsQ}"
pwm_min = 2457
pwm_max = 7372

con = socket.create_connection(('trackthesat.satellitesabove.me', 5031))

con.recv(1024)
con.send(ticket + b"\n")
problem_desc = con.recv(1024).split(b"\n")
for line in problem_desc:
    if line.startswith(b"Latitude"):
        lat = float(line.split()[1])
    elif line.startswith(b"Longitude"):
        lon = float(line.split()[1])
    elif line.startswith(b"Start time"):
        time = float(line.split()[-1])
    elif line.startswith(b"Satellite"):
        sat = line.split(maxsplit=1)[1].decode("utf8")
    elif b"observations" in line:
        duration, step = [
            int(x) for x in problem_desc[5].split() if x.isdigit()
        ]

orb = Orbital(sat, tle_file=tle_path)

current_time = datetime.utcfromtimestamp(time)


def pwm_for(az, el):
    low = pwm_min
    high = pwm_max

    if (az > 180):
        az -= 180
        el = 180 - el

    az_pwm = (az/180) * (high - low) + low
    el_pwm = (el/180) * (high - low) + low

    return az_pwm, el_pwm


delta = timedelta(seconds=step)
for i in range(duration):
    az, el = orb.get_observer_look(current_time, lon, lat, 0)
    paz, pel= (pwm_for(az,el))
    res = (", ".join([str(time+i), str(int(round(paz))), str(int(round(pel)))]))
    con.send(res.encode("utf8") + b"\n")
    current_time += delta

con.send(b"\n")
print(con.recv(1024).decode("utf8"))
