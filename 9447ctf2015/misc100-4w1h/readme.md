## 4w1h - Misc 100 Problem

### Description

`4w1h` is a cute problem: we get a series of images from Google Street View,
and we need to recover which direction the images are facing. 

### Solution

This involved simply recognizing monuments, as well as occasionally searching
for strings on Google and reverse image searching parts of the given image.

This gave us rough locations for each. From there, we played around a bit until
we had good enough guesses for each of the directions. In many cases we were
able to find exact matches, but in a few we settled for 'close enough'.

Our solutions are as follows:
```
0: NW https://www.google.com/maps/@-22.9577812,-43.2068356,3a,75y,1.63h,102.79t/data=!3m6!1e1!3m4!1s4DyY-3gRSrFV6ElpW69-IA!2e0!7i13312!8i6656
1: S https://www.google.com/maps/@1.2891171,103.8542178,3a,89.9y,180.07h,86.18t/data=!3m6!1e1!3m4!1sFQTioJ0q_lLqTVpU0GtSBw!2e0!7i13312!8i6656!6m1!1e1
2: N https://www.google.com/maps/@-33.8576596,151.209252,3a,28.4y,10.41h,91.91t/data=!3m6!1e1!3m4!1sM6Art2b882XlIU7EEphbmw!2e0!7i13312!8i6656
3: SE https://www.google.com/maps/@43.0836224,-79.077298,3a,90y,151.16h,82.53t/data=!3m6!1e1!3m4!1siL1i6KTNVw0j8BXMH_CnlA!2e0!7i13312!8i6656
4: W https://www.google.com/maps/@38.8893105,-77.0328766,3a,75y,274.37h,84.91t/data=!3m6!1e1!3m4!1sGXxnHvvXIh9ZIcV1gfjbxA!2e0!7i13312!8i6656!6m1!1e1
5: NE https://www.google.com/maps/@48.8611635,2.3342685,3a,90y,94.65h,81.35t/data=!3m6!1e1!3m4!1s7OfaKtViHw6flijhv34aNQ!2e0!7i13312!8i6656!6m1!1e1
6: NW https://www.google.com/maps/@59.9398238,30.3155033,3a,90y,323.59h,101.67t/data=!3m6!1e1!3m4!1smTEhn-Y1rbv3orgeV5DbNw!2e0!7i13312!8i6656
7: W https://www.google.com/maps/@41.882726,-87.6225599,3a,75y,275.1h,87.58t/data=!3m6!1e1!3m4!1sQZFXb5I7gYZegqvmi7kYOQ!2e0!7i13312!8i6656!6m1!1e1
8: N https://www.google.com/maps/@37.5750684,126.9768249,3a,75y,359.98h,86.08t/data=!3m6!1e1!3m4!1snQzQJfkLNSVcHQizsrBV2g!2e0!7i13312!8i6656
9: S (given as South in the image)
```

This gave us our flag `9447{NWSNSEWNENWWNS}`
