# Power Level

In this challenge, we are provided access to a service that sends us
800,000 bytes of data and asked us 2 questions about it: to find the
frequency of the signal, and the signal-to-noise ratio (SNR).  An
example of the data sent can be found in
[example-samples](./example-samples).

Looking at the samples we receive, based on the size of the data
sent over, the 100000 samples we receive can be interpreted as 64-bit complex
values.

Taking a discrete Fourier transform allows us to consider each
frequency component separately.

We find that the magnitude at frequency 3125 is a very sharp peak
compared to everything else, and thus must be the signal frequency
(the number of samples and sampling frequency lines up to not require
any multiplier between the FFT frequency and actual frequency).

The SNR (in decibels) is 10 times the `log_10` of the ratio of power
level of the signal to the level of the noise.

The power levels are the square of the sums of magnitudes (and since
we want a ratio, this works independent of choice of normalization for
the FFT).

Implementing these operations using numpy (see [solve.py](./solve.py))
gives us a flag.
