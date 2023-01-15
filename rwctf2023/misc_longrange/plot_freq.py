import numpy as np
import scipy.io.wavfile as wf
import matplotlib.pyplot as pp
import scipy.signal as ss

rate, data = wf.read("sig.wav")
data = data / 32768.0
data = data[:, 0] + 1j * data[:, 1]

valid = np.abs(data) > 0.015
dvalid = valid[1:] & valid[:-1]

freq = np.diff(np.angle(data)) * dvalid
freq[freq > np.pi] -= 2 * np.pi
freq[freq < -np.pi] += 2 * np.pi
pp.plot(freq, ".-")
pp.show(block=True)
