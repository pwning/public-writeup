## Ground Segment - I see what you did there - 146 points (23 solves)

### Background

> Your rival seems has been tracking satellites with a hobbiest antenna, and it's causing a lot of noise on my ground lines. Help me figure out what he's tracking so I can see what she's tracking

This is similar to the Track the Sat challenge in a lot of ways. We are given TLEs for satellites. We are also given triplets of signals from a known station tracking known satellites and unknown station tracking unknown satellites.

### Solution

The first step is to recover the azimuth and elevation data from the recovered signal. After plotting a couple signals and looking, we can see the PWM data is at exactly 50hz. Luckily there is 0 clock jitter, so this is pretty simple. The PWM pulses start precisely every 2048 samples, so we can just see when the falling edge occurs by looking for the next spike. Then we can recover the exact duty cycle by just taking the time of the falling edge and dividing by 2048.

We do this every second, just because that's how often we gave angles in the Track the Sat challenge. This matches up for the known data so things seem to work pretty well.

Figuring out what is being tracked is a pretty hard problem in principle. However we don't have too many satellites in the catalog, and we assume that satellites that error out with our orbital library are doing something weird and can be ignored. This means we can simply calculate the proper PWM data (again, already covered in Track the Sat), and see if it is consistent. If so: we've found our satellite.

This search could be made more efficient in a number of ways: making sure satellites are visible before bothering to do the calculations, only calculating the azimuth and elevation for a second or two for sanity checking, etc. However, it's fast enough so we don't need to worry.


#### Dependencies and Instructions

To run the solution, install `pyorbital`. Then download the supplemental problem material (`active.txt` and the unknown signals, for us placed in `rbs_m2-oscar87104papa/`) and then run `solve.py`
