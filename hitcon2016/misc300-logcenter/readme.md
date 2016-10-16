## LogCenter - Misc/Pwn 300 Problem

### Description

I build a log server and implement a special function.
However, it seems to have a little problem ...
nc 52.198.182.219 22222

### Writeup

We started by comparing the set of files we got, with those that are normally shipped with syslog-ng. We noticed that *libextfuncs.so* is not a normal part of syslog-ng, and it gives us a format-string vulnerability.

Once we figured out how to connect to the syslog-ng daemon, we quickly discovered that we do have a format-string vulnerability in the messages we send to the daemon. We can use this to get stack addresses, library addresses, and to read/write to memory.

Our plan for exploitation was to modify a return pointer on the stack to instead point to the *system* function. We get the address of *system* by following imports from syslog to get to libc. We used the saved rbp values on the stack to figure out the address we need to overwrite using *%n*.

Solution: [exploit.py](exploit.py)
