# Crosslinks

In this problem, we are given TLE orbital parameters for 75 satellites, and are tasked with determining which of the satellites is "us".  To accomplish this, we are given observations of other satellites relative to ours at known points in time.

Since the distances given were near-exact, the simplest solution was to simply take the first observation and find the satellite with a distance most closely mtching that observation; this is easily accomplished using `skyfield` to do the orbital math, and just checking all 74 possibilities against the selected observation.  Repeating this several times was sufficient to get a flag.

See `solve.py` for our implementation.
