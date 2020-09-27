In the beginning, we are given the following text and told that the flag forms
a sentence:

```
BC552
AC849
JL106
PQ448
JL901
LH908
NH2177
```

Each of these numbers appears to be an airline flight number, which Google
searches confirm. There isn't much information about each flight, but we do
notice a pattern where many of the origin locations match up with destinations
of other flights.

```
BC552:  OKA -> NGO
AC849:  LHR -> YYZ
JL106:  ITM -> HND
PQ448:  TBS -> ODS
JL901:  HND -> OKA
LH908:  FRA -> LHR
NH2177: NRT -> ITM
```

We then rearrange the flights into chains where the source and destination
airports match.

```
NRT -> ITM -> HND -> OKA -> NGO
LHR -> YYZ
TBS -> ODS
FRA -> LHR
```

Taking the first letter of each gives some fragments of words:

```
NIHON LY TO FL
```

Keeping with the theme of flying, we can rearrange (and smoosh two "L"s
together) to get the required "sentenece":

```
FLY TO NIHON
```

Finally, since we know that the flag is all capital letters with no spaces
as-per the challenge hint, we get:

```
TWCTF{FLYTONIHON}
```
