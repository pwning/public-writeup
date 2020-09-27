The challenge presents us with a
[URL](http://urlcheck1.chal.ctf.westerns.tokyo/) and a `tar` file. The page on
the URL has a text input and submit form, and at first glance looks like the
way to submit an exploit for the challenge.

Inside the `tar` archive, at the top level there are some files for configuring
a Docker container. These seem to set up and run a Python Flask application
that is accessible from the web on port 80. The only interesting part of the
archive is the `src/app.py` file, which contains the code for the server that
is running. This code makes a request to whatever IP/site you input (with some
restrictions) and prints the output.

The goal of the challenge is to access the `/admin-status` page from within the
network via server-side request forgery. In particular, we have to bypass the
following function that is responsible for filtering inputs and denying access
to internal URLs:

``` python
app.re_ip = re.compile('\A(\d+)\.(\d+)\.(\d+)\.(\d+)\Z')

def valid_ip(ip):
    matches = app.re_ip.match(ip)
    if matches == None:
        return False

    ip = list(map(int, matches.groups()))
    if any(i > 255 for i in ip) == True:
        return False
    # Stay out of my private!
    if ip[0] in [0, 10, 127] \
        or (ip[0] == 172 and (ip[1] > 15 or ip[1] < 32)) \
        or (ip[0] == 169 and ip[1] == 254) \
        or (ip[0] == 192 and ip[1] == 168):
        return False
    return True
```

The key observation is that the regular expression
`\A(\d+)\.(\d+)\.(\d+)\.(\d+)\Z` allows unlimited digit character inputs, as
long as each parsed octet integer is not greater than 255. This means that it
is possible to precede the octets with one or more `0` characters.

When IP octets are preceded by `0`, the low-level `inet_addr` function parses
the octet in octal, rather than decimal. (More info on that
[here](https://superuser.com/a/857618/326864)) Thus, by using `0177` instead of
`127` as the first octet of our input IP, we can input a number that the Python
filtering function parses as `177`, which is valid, but which the underlying
network functions parse as `127`, allowing us to make requests to the local
server.

The final input to the text box was:

```
http://0177.0.0.1/admin-status
```

This returned the flag `TWCTF{4r3_y0u_r34dy?n3x7_57463_15_r34l_55rf!}`.
