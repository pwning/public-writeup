We are given a file containing IQ data and told to decode it.

Plotting the I and Q data as x and y values in a plot, we see the values nicely
align themselves into four quadrants, indicating the data is transmitted with
QPSK. From there, we still need to determine which quadrant corresponds to
which two-bit symbol. Luckily there are not many possibilities and we can try
them all until one works.

The following quick script decodes the data and prints the flag (as well as
some extra data which matches up with CCSDS headers):

```python
cs = [eval(x) for x in open("iqdata.txt").read().splitlines() if x]

def radio(x):
    if x.real < 0:
        if x.imag < 0:
            return 1
        return 0
    else:
        if x.imag < 0:
            return 2
        return 3

qpsk = [radio(c) for c in cs][::4]

comp = bytes.fromhex(hex(int("".join((["{:02b}".format(q) for q in qpsk])),2))[2:])
print(comp)
```
