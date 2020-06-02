## Communication Systems - Ground Control to Major Tom - 257 points (8 solves)

_Writeup by: Robert Xiao (@nneonneo)_

### Background

> You killed that last one. Ready to take it to the next level?

We're given a single WAV file, with a sampling rate of 32000 Hz, two channels, 83456 samples long.

### Solution

After having done [Phasors to Kill](../comms-phasor2/readme.md), this setup looked extremely similar. Like the previous problem, this signal has two channels, and what looks like phase-shift keying (PSK) encoding in the middle. On both sides of the signal, there's a constant tone - a mix of 1000 and 1500 Hz frequencies (with 500 and 2500 Hz components too). Since this tone seems to be constant and not modulated, I ignored it completely. It might have been helpful for figuring out whether this was a real radio protocol.

Like the previous problem, plotting the instantaneous phases shows four hotspots, suggesting QPSK. Experimenting with the samples per symbol, I found that plotting every 8th sample produced a nice constellation diagram, so I used the same demodulator as the Phasors to Kill solution to extract bits. However, while the resulting bits had a clear repeating sequence every 96 bits (suggesting that the demodulation approach was correct), all I could get was meaningless garbage.

I could tell it was differentially encoded - differential decoding produced repeating patterns, while non-differential decoding did not - so I focused on the decoding from phases to codes. Previously we used a Gray code; this time, I tried all permutations of phase to code mappings, and found that a *different* Gray code table (`1, 0, 2, 3`) produced meaningful results - bytes that were clearly ASCII.

The resulting data had some clear "framing" in the form of bytes with the hex pattern `FE BE EF DE AD` every 12 bytes. Stripping those out gives us the lyrics:

```
Ground Control to Major Tom
Ground Control to Major Tom
Take your protein pills and put your helmet on
Ground Control to Major Tom (ten, nine, eight, seven, six)
Commencing countdown, engines on (five, four, three)
Check ignition and may God's love be with you (two, one, liftoff)
This is Ground Control to Major Tom
You've really made the grade
And the papers want to know whose shirts you wear
Now it's time to leave the capsule if you dare
"This is Major Tom to Ground Control
I'm stepping through the door
And I'm floating in a most peculiar way
And the starUUUUUU0P{9oflag{...}UU0P>92s look very different today
For here
Am I sitting in a tin can
Far above the world
Planet Earth is blue
And there's nothing I can do
Though I'm past one hundred thousand miles
I'm feeling very still
And I think my spaceship knows which way to go
Tell my wife I love her very much she knows
Ground Control to Major Tom
Your circuit's dead, there's something wrong
Can you hear me, Major Tom?
Can you hear me, Major Tom?
Can you hear me, Major Tom?
Can you "Here am I floating 'round my tin can
Far above the moon
Planet Earth is blue
And there's nothing I can do"
```

with the flag in the middle (some non-printable characters have been stripped).

The full solve script can be found in [solve.py](solve.py). Put it in the same directory as `challenge.wav` and run the script under Python 3; it requires the NumPy, SciPy and Matplotlib dependencies.
