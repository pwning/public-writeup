# vimshell — Miscellaneous Problem — Writeup by Artemis Tosini

## Description

We are given a web shell to a copy of vim. They've disabled the Q, g, and colon keys, so that we can't simply run a shell by entering command mode using `:!`.

## Solution

The website shows us a picture of src/normal.c. Several commands have been patched out of the source. However, they kept in ^W, which allows one to enter command mode using `^W :`. See src/normal.c:

```c
/* "CTRL-W :" is the same as typing ":"; useful in a terminal window */
cap->cmdchar = ':';
cap->nchar = NUL;
nv_colon(cap);
```

Unfortunately, most browsers do not allow overriding ^W. Our solution was to run this on a Mac, where ^W doesn't do anything by default.
	
Once we have run `^W :`, we enter command mode and we can simply `! /bin/sh` to run a shell, and find that /flag exists. When we cat the file, we get the flag

    TWCTF{the_man_with_the_vim}
