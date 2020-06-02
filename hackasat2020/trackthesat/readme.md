## Ground Segment - Track the Sat - 44 points (106 solves)

### Background

> You're in charge of controlling our hobbiest antenna. The antenna is controlled by two servos, one for azimuth and the other for elevation. Included is an example file from a previous control pattern. Track the satellite requested so we can see what it is broadcasting

We are given a file containing a README with info about controlling the servos: they take in numbers between 2457 and 7372 for 0 to 180 degrees of rotation. We are also given a file with TLEs for several satellites. Finally a few examples are given that allow one to test their solution.

### Solution

This problem is a pretty trivial application of orbital tracking. We just need to find azimuth and elevation for a point on Earth to a satellite which most software packages easily handle. After that, we can just scale those numbers based on the provided PWM scale.

#### Dependencies and Instructions

To run the solution, install `pyorbital`, and then run `solve.py`
