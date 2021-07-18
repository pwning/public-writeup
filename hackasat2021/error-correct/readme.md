This challenge just tells us there is important telemetry but with a bit error
which prevents us from decoding it.

Again we are given a file which appears to be IQ data, and plotting it
(while excluding a few samples at the beginning which seem noisey) gives a
nice QPSK constellation, indicating QPSK data.

Attempting to decode this similar to the previous challenge with CSSDS data
encoded with QPSK doesn't seem to work. Based on the name of the challenge, it
seems pretty clear that there is some error correction involved.

Unfortunately with so many error correcting codes to choose from combined with
so many ways to read the QPSK symbols, as well as not knowing the correct bit
offset, it seems an overwhelming number of possibilities to test. Searching
[online](https://destevez.net/2017/01/coding-for-hit-satellites-and-other-ccsds-satellites/)
for guidance, it seems that there is a particular error correcting code used by
CCSDS satellites. Luckily this seems to be available in python through
scikit-dsp.

After trying this a bit, it doesn't appear to Just Work with our solution from
the previous problem (or the error correction is wrong). And unfortunately it
is slow to enumerate and look through everything. The previous cited blog also
mentions a synchronization word used by CCSDS to indicate the start of packets,
which can help us to determine if our data is correctly encoded and find the
proper bit offsets.

With this, we code up a search using the assumed error correcting code,
enumerating through possible symbol decodings for the QPSK, and searching for
the synchronization word to find the right decoding and bit offsets.

Luckily we find the sychronization word in a possible choice for the QPSK
decoding, and use this to sychronize our bitstream and recover the flag.

The following python code implements this solution and prints the flag:

```python
import numpy as np
import sk_dsp_comm.fec_conv as fec
import itertools

odata = np.fromfile("intermediate.bin", dtype="<c8")

# synchronization word to search for
syncword = "{:032b}".format(0x1acffc1d)

cc1 = fec.FECConv(('1011011','1111001'), 10)

def search():
    for offset in range(-4, 4+1):
        data = odata[85 + 4 * offset::4]

        # import matplotlib.pyplot as plt
        # plt.plot(data.real, data.imag, ".-")
        # plt.show(block=True)

        import itertools

        quadrants = [(0, 0), (0, 1), (1, 0), (1, 1)]
        for perm in itertools.permutations([0,1,2,3]):
            tmap = dict(zip(quadrants, perm))

            bits = np.array([data.real > 0, data.imag > 0], dtype=int).T
            bitstring = []
            prev = 0
            for chunk in bits:
                v = tmap[tuple(chunk)]
                bitstring.append(v % 4)
                prev = v

            bitstring = "".join(map(str, bitstring))
            bs = []
            prev = 0
            for i in range(0, len(bitstring), 4):
                byte = int(bitstring[i:i+4], 4)
                v = byte
                bs.append(f"{v:08b}")
                prev = byte

            print(offset, perm)
            bs = np.asarray([int(c) for c in "".join(bs)])
            bs_fec = cc1.viterbi_decoder(bs, 'hard')
            bitstream = "".join(str(int(c)) for c in bs_fec)
            if syncword in bitstream:
                print("syncword found!")
                print( bitstream )
                # start of bitstream is where we found the syncword
                syncd = bitstream[bitstream.index(syncword):]

                # truncate it to a multiple of 8 bits to make our life easier
                truncated = syncd[:-(len(syncd) % 8)]

                # finally convert to ascii
                return (bytes.fromhex(hex(int(truncated, 2))[2:]))

print(search())
```
