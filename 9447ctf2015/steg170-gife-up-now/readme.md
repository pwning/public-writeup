## gife up now - Steganography 170 Problem

### Description

`gife up now` is an animated gif with QR codes, the frames themselves are used
to encode two different messages in two different ways.

### Solution

To start off, we read off the QR codes in the images, and get something like
the following:
```
two parts all lower
add 9447{ to start and { to the end
first looks like '7do'
cut off 450ms
second like https://www.youtube.com/watch?v=5xxTkB5bGy4
like faucet script
```

The first thing we recovered was the `tap code`, which the youtube link and
word faucet presumably hinted towards. There are 89 total frames in the image,
but only 26 unique QR codes, looking at the repeated QR codes:
```
for x in `seq 0 88`; do zbarimg gif_$(printf "%02d" $x).gif 2>/dev/null; done  | cut -d ':' -f 2-100 | uniq -c | awk '{print $1}' | tr -d '\n' | perl -p -e 's/(..)/\1 /g'
```
We get `14 34 44 14 34 34 44 14 34 44 14 54 44`, which corresponds to
`dotdootdotdyt`.

After a few hints and poking the organizers, we were also able to get the
first part of the key, which was simply Morse code. Each frame is on the
screen for 400ms or 500ms, so using the shorter frames as `.` and the
longer as `-`:
```
identify -format "%T\n" gife-f97a0c3eb838999e25dbda2d1f469674.gif | tr -d '\n' | tr -d '0' | tr '54' '-.'
```
We ended up with `-..-----...-..--------...-..----....-..-----...-..--------...-..--------...-..--------...`

Attempting to use only the characters `7`, `d`, and `o`, we decoded the Morse to
`do7doo7dodido7doo7doo7doo7`.
We made the assumption that `di` was supposed to be another `7`, and that
ended up working, giving us the flag `9447{do7doo7do7do7doo7doo7doo7dotdootdotdyt}`

(The organizers fixed the `s/di/7/` problem with a new binary after we solved
the problem and let them know)
