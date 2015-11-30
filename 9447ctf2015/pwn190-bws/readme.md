## BWS - Pwnable 190

```
My friend has been playing that annoying song far too long. Can you own his web server now?

The web page is at http://bws-ad8sfsklw.9447.plumbing
```

BWS is a HTTP server, which only accepts `GET` and `HEAD` requests.

The bug is in the function that deals with directory traversal.
When the sequence `../` is encountered in the filename, the program
traverses backwards in the filename searching for the `/` character.
If there is no `/` character in the filename before the `../` was
encountered, a stack underflow occurs.

Therefore, if the program found that there was a `/` in the stack,
and that `/` was not encountered in the filename, the return address
would be overwritten. This in turn allows for ROP because of the large
body of input stored on the stack.

`9447{1_h0pe_you_L1ked_our_w3b_p4ge}`
