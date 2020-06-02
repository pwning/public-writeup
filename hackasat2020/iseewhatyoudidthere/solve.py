from datetime import datetime, timedelta
import numpy
from pyorbital.orbital import Orbital
import socket


TICKET = b"ticket{oscar87104papa:GLcXrrgss52BoAIW_n5-d0OJPGZsxfimnajtuG1rRueS-WAXeQfJerF4mRgcHJr0Uw}"
SAMPLE_RATE = 102400
TICK = 2048

pwm_min = 0.05 * TICK
pwm_max = 0.35 * TICK

def pwm_for(az, el):
    low = pwm_min
    high = pwm_max

    if (az > 180):
        az -= 180
        el = 180 - el

    az_pwm = (az/180) * (high - low) + low
    el_pwm = (el/180) * (high - low) + low

    return az_pwm, el_pwm

def ground_truth(lat, lon, time, sat, duration):
    orb = Orbital(sat, tle_file="active.txt")
    delta = timedelta(seconds=1)
    azs = []
    els = []
    for i in range(duration):
        az, el = pwm_for(*orb.get_observer_look(time, lon, lat, 0))
        azs.append(az)
        els.append(el)
        time += delta
    return azs, els


def get_pwms(filename):
    dats = numpy.fromfile(filename, dtype='<f')
    chan1 = dats[::2]
    chan2 = dats[1::2]
    return get_pwm(chan1), get_pwm(chan2)


def get_pwm(dat):
    # split data up by second
    seconds = numpy.array_split(dat, len(dat)/SAMPLE_RATE)
    base = sum(seconds)/len(seconds)
    halfway = numpy.max(seconds[0] - base)/2
    return [numpy.mean(numpy.where(second - base > halfway)[0] % TICK) for second in seconds]

def consistent(expected, pwms):
    azs, els = expected
    pwm_azs, pwm_els = pwms
    
    for az, pwm_az in zip(azs, pwm_azs):
        if abs(az - pwm_az) > 2:
            return False
    for el, pwm_el in zip(els, pwm_els):
        if abs(el - pwm_el) > 2:
            return False
    return True


# sanity check
pwms = get_pwms("examples/signal_0.bin")
expected = ground_truth(32.4907, 45.8304, datetime.utcfromtimestamp(1586249863.726371), 'CANX-7', 120) 

assert consistent(expected, pwms)

pwms_chal0 = get_pwms("rbs_m2-oscar87104papa/signal_0.bin")
pwms_chal1 = get_pwms("rbs_m2-oscar87104papa/signal_1.bin")
pwms_chal2 = get_pwms("rbs_m2-oscar87104papa/signal_2.bin")

con = socket.create_connection(('antenna.satellitesabove.me', 5034))
con.recv(1024)
con.send(TICKET + b"\n")
problem_desc = con.recv(1024).split(b"\n")
lat = float(problem_desc[1][33:38])
lon = float(problem_desc[1][50:])
time = float(problem_desc[2].split()[-1])

possible_sats = [x.strip() for x in open("active.txt").read().split("\n")[::3]]

found = [None, None, None]
for sat in possible_sats:
    try:
        expected = ground_truth(lat, lon, datetime.utcfromtimestamp(time), sat, 120)
    except KeyboardInterrupt:
        break
    except:
        continue
    if consistent(expected, pwms_chal0):
        found[0] = sat
        print(sat)
    elif consistent(expected, pwms_chal1):
        found[1] = sat
        print(sat)
    elif consistent(expected, pwms_chal2):
        found[2] = sat
        print(sat)
    if all(found):
        break

for sat in found:
    con.send(sat.encode("utf8") + b"\n")
con.send(b"\n")
print(con.recv(1024).decode("utf8"))
