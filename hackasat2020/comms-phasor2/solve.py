import numpy as np
import scipy.io.wavfile as wf
import matplotlib.pyplot as plt

rate, data = wf.read('challenge.wav')
data = data / 32768.0

# empirically determined offset
points = data[88::4]

plt.plot(points[:, 0], points[:, 1], 'o')
angles = np.angle(points[:, 0] + points[:, 1] * 1j)

vals = ((angles % (2 * np.pi)) - (np.pi / 4)) / (np.pi / 2)
bits = []
prev = 0
for i in vals:
    v = (int(round(i)) - prev) % 4
    prev = int(round(i))
    bits.append(['00', '01', '11', '10'][v])

bits = ''.join(bits)
for i in range(0, len(bits), 8):
    print(chr(int(bits[i:i+8], 2)), end='')
print()
