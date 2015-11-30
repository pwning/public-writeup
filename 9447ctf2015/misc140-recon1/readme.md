## Recon 1 - Misc 140 Problem - Writeup by Robert Xiao (@nneonneo)

### Description

> Someone has attacked your site. We have attached a log collected from the time of the attack.

> This task is split into two parts. The end goal (Recon 2) is to find the full name of the attacker.

> The flag for Recon 1 is *not* the name of the attacker. Recon 1 flag will appear as 9447{...} on your screen when you find it. 

### Solution

In the provided log file, we can see that the address `192.241.254.77` has
repeatedly accessed `/admin`, getting 403s until the last entry, where it gets a
200 response. This is probably the IP that attacked us.

`dig -x 192.241.254.77` yields the name `www.williestoleyour.pw`. Going to that
site yields a fairly generic looking site which promises to offer penetration
testing. Clearly, "willie" stole our passwords.

There's not much of interest on `www.williestoleyour.pw` itself. However, using
the Internet Archive, we find an old version of the site here:
https://web.archive.org/web/20151115002534/http://www.williestoleyour.pw/. On
this backup page you can see an old email address: `info@dynamiclock.pw`.

Visiting `dynamiclock.pw` takes us to a new page which offers services by
"William", and a flag: `9447{YouAreStalKey}`
