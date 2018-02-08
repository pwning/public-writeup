## Simple CMS - Web Challenge

We are given a URL and a zip file with PHP source code, [4f6b17dc3d565ce63ef3c4ff9eef93ad.zip](4f6b17dc3d565ce63ef3c4ff9eef93ad.zip). From a brief
look at *dbconn.php*, it is obvious that this is not your typical web challenge.

This challenge implements its own file-based database, which inspires us to look for a vulnerability in the implementation in *dbconn.php*. While
reading **rbPack**, we notice that a single-byte char is used to store the length of a string field. This will cause problems if the string is
longer than 255 bytes, because PHP will silently cast the input of **chr** as an 8-bit integer.

Using this vulnerability, we can trick the database into parsing our string as the remaining columns of the row. Thankfully, the member tables
are organized with the *lvl* field at the end of the row, so we can trivially trick it into returning *lvl* as **2** giving us admin. The only
annoying part is that we need to make sure that the fake *pw* has a known MD5 hash.

A complete exploit can be found in [exploit.py](exploit.py).

