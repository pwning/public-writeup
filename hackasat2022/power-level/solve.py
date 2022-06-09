import sys
import numpy as np
import matplotlib.pyplot as plt

sample_file = sys.argv[1]

with open(sample_file, 'rb') as f:
    dat = np.fromfile(f, dtype=np.dtype("complex64"))

F = np.fft.fft(dat)
A = abs(F)
loudest_freq = np.argmax(A)
print(loudest_freq)

Psignal = A[loudest_freq]*A[loudest_freq]
noise = np.delete(A, loudest_freq)
Pnoise = np.sum(np.square(noise))
SNR = Psignal / Pnoise
SNRdb = 10 * np.log10(SNR)
print(SNRdb)
