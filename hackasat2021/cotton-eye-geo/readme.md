In this problem we are given a position and velocity for a satellite in Earth
orbit, and asked to give a time and delta-v for one maneuver to bring us to
a new orbit.

Plotting the current orbit, we can see it is an elliptical orbit already in
the correct plane, and with the apogee at the desired altitude for the
target circular orbit.

For anyone with a bit of orbital mechanics knowledge (or who has ever played
Kerbal Space Program), this makes the maneuver trivial: at the apogee, simply
increase thrust in the prograde direction until we raise the perigee to
the same altitude.

This could be done with math, or with a simple python program.

```python
from orbital import earth, KeplerianElements, Maneuver, plot, plot3d
from scipy.constants import kilo
import numpy
from datetime import datetime, timedelta

# the state vector we are given for our satellite
r = numpy.array([8449.401305, 9125.794363, -17.461357])
v = numpy.array([-1.419072, 6.780149, 0.002865])
# the current time
ts = "2021-06-26-19:20:00.000000-UTC"
tf = "%Y-%m-%d-%H:%M:%S.%f-UTC"
tt = datetime.strptime(ts, tf)

orbit = KeplerianElements.from_state_vector(r*kilo, v*kilo, earth)

# the target (circular) orbit
target_a = 42164*kilo
target_e = 0.005

target_orbit = KeplerianElements.with_altitude(target_a, body=earth)

# figure out at what time our position reaches our perigee
while True:
    orbit.propagate_anomaly_by(M=0.001)
    if abs(numpy.linalg.norm(orbit.r) - target_a) < (2*kilo):
        break

# estimate the speed we want
needed_vel = numpy.linalg.norm(target_orbit.v)

# apply that same speed in the prograde direction
v_est = orbit.r/numpy.linalg.norm(orbit.r) * needed_vel
v_est = numpy.array([v_est.x, -v_est.y, v_est.z])

# search +/- 10% to get the velocity just right
best_v = None
best_e = 1
for x in numpy.arange(0.9,1.1,0.00005):
    orbit2 = KeplerianElements.from_state_vector(orbit.r, v_est*x, earth)
    if abs(orbit2.a - target_a) < 10*kilo and orbit2.e < 0.0009 and orbit2.e < best_e:
        best_e = orbit2.e
        best_v = v_est*x

mtime = tt + timedelta(seconds=orbit.t)
move = (best_v - orbit.v)/1000
print("vel: ", move[0], move[1], move[2])
print("ts: ", datetime.strftime(mtime, tf))

mtime = tt + timedelta(orbit.t)
```

This will print out the delta-V and the time of the maneuver. Sending that to
the server will return us the flag.
