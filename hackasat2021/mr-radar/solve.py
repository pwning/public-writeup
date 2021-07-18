from pwn import *
from math import degrees
import pymap3d as pm
from datetime import datetime
from orbital import earth, KeplerianElements, utilities
from astropy.time import Time
from pytwobodyorbit import lambert
import os

host = 'moon-virus.satellitesabove.me'
port = 5021
ticket = None
try:
    ticket = os.environ['TICKET']
except:
    print("set TICKET env to interact with challenge server")

latitude = 8.7256 # deg latitude
longitude = 167.715 # deg longitude
altitude = 35 # meters

flight_time = 100.0 # difference in time between first and last pulse (seconds)
earth_mu = 3.986004418e14 # gravitational parameter of earth (m^3s^-2)

# returns eci position in meters and datetime of position 
def eci_position_from_pulse(pulse, lat, long, alt):
    time, az, el, r = pulse.split("\t")
    t = datetime.strptime(time, "%Y-%m-%d-%H:%M:%S.%f-%Z")

    # az: azimuth (degrees)
    # el: elevation (degrees)
    # r: range (km -> m) 
    x, y, z = pm.aer2eci(float(az), float(el), float(r) * 1000, lat, long, alt, t, deg=True)

    return [x, y, z], t

with open('radar_data.txt', 'r') as f:
    pulses = f.readlines()[1:]

initial_pulse = pulses[0]
final_pulse = pulses[-1]

# get positions
initial_pos, initial_time = eci_position_from_pulse(initial_pulse, latitude, longitude, altitude)
final_pos, final_time = eci_position_from_pulse(final_pulse, latitude, longitude, altitude)

# get velocity
initial_velocity, terminal_velocity = lambert(initial_pos, final_pos, flight_time, mu=earth_mu)

# get orbit from final position/velocity
r = utilities.Position(x=final_pos[0], y=final_pos[1], z=final_pos[2])
v = utilities.Velocity(x=terminal_velocity[0], y=terminal_velocity[1], z=terminal_velocity[2])
orbit = KeplerianElements.from_state_vector(r, v, earth, Time(final_time, format='datetime', scale='utc'))

print(orbit)
print(f"True Anomaly: {degrees(orbit.f)} deg")

# convert orbital elements into requested units
elements = [
    orbit.a / 1000, # semi-major axis (m -> km) 
    orbit.e, # eccentricity (dimensionless)
    degrees(orbit.i), # inclination (radians -> degree)
    degrees(orbit.raan), # RAAN (radians -> degrees)
    degrees(orbit.arg_pe), # argument of perigee (radians -> degrees)
    degrees(orbit.f), # true anomaly (radians -> degrees)
]

if not ticket: 
    exit(0)

# connect to server and send ticket 
io = remote(host, port)
print(io.recvline())
io.sendline(ticket)
print(io.recvuntil(":").decode())

# send elements
for element in elements:
    print(io.recvuntil(":").decode())
    io.sendline(str(element))

# get flag
print(io.recvall().decode())
