## mondai.zip - Miscellaneous Challenge - Writeup by Samuel Kim (@ubuntor)

### Description

We have a series of nested zips, each with a password.

### Solution

#### Stage 1
We get an encrypted zip named `y0k0s0.zip`.

Trying `y0k0s0` as the password worked.

**Password:** `y0k0s0`

#### Stage 2

We get another encrypted zip `mondai.zip` and a pcap `capture.pcapng`.

The pcap contains a series of pings, each with data of the form `abcd...`.

The lengths of the data look like they're in ascii range, so converting and
trying that as the password worked.

**Password:** `We1come`

#### Stage 3

We get another encrypted zip `mondai.zip` and a textfile `list.txt`.

The textfile contains a set of what appears to be random passwords.

Passing it into `fcrackzip` as a dictionary gave us the password.

**Password:** `eVjbtTpvkU`

#### Stage 4

We get another encrypted zip `1c9ed78bab3f2d33140cbce7ea223894`.

This looks like an md5 hash, so throwing it onto an online tool gave us the
password.

**Password:** `happyhappyhappy`

#### Stage 5

We get another encrypted zip `mondai.zip` and a textfile `README.txt` with
contents `password is too short`.

Using `zip2john` and `john` to crack the zip gave us the password.

**Password:** `to`

#### Final Stage

We get a textfile `secret.txt` with contents:

```
Congratulation!
You got my secret!

Please replace as follows:
(1) = first password
(2) = second password
(3) = third password
...

TWCTF{(2)_(5)_(1)_(4)_(3)
```

**Flag:** `TWCTF{We1come_to_y0k0s0_happyhappyhappy_eVjbtTpvkU}`
