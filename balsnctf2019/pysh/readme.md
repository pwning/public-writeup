# pyshv1, pyshv2, pyshv3 - misc

This is a series of challenges that had to be done in order (pyshv2 and pyshv3's code packages were encrypted with the previous challenges' flags). In each one a simple "Python shell" loads a pickle representing the "user". The unpickler is "secure" in that it only accepts objects from certain modules; nevertheless, it is still vulnerable to an evil pickle attack.

## Capabilities

The pickle "language" lets us set any dictionary key, and write to any object attribute, but does not provide a way to read dictionary keys or attributes. It also lets us call any function that we can get a reference to. In evil pickle attacks, the usual approach is to get a reference to `__builtins__.eval` and then call that to execute arbitrary code. However, pysh's secure unpickler only lets us access objects from specific modules, blocking that attack.

## pyshv1

This unpickler gave us access to the `sys` module. We use this to get a reference to `sys.modules`. We can then set `sys.modules['sys']` to any object in order to access its attributes. This allows us to perform the following chain of operations:

```
obj0 = sys.modules
obj0['sys'] = sys.modules
# now that sys.modules['sys'] = sys.modules,
# accessing globals in "sys" results in getting attributes of that dictionary
obj0['sys'] = sys.__getitem__('builtins')
# now sys.modules['sys'] = sys.__builtins__
sys.__getattribute__('eval')("__import__('os').system('/bin/sh'))
```

See [`exploit1.py`](exploit1.py) for the code.

## pyshv2

This unpickler only lets us access the private `structs` module, which is a totally empty module! However, we can abuse built-in attributes of modules with the following sequence:

```
structs.__loader__.__dict__ = structs.__dict__
# modifying structs.__loader__'s attributes now modifies structs attributes too
# the BUILD opcode copies all key/value pairs from a dict to the attributes of an object
BUILD(structs.__loader__, structs.__builtins__)
# now structs contains all the elements of builtins
structs.eval("__import__('os').system('/bin/sh'))
```

## pyshv3

This unpickler lets us access the same `structs` module, but now it has a class in it. As it turns out, our exploit for pyshv2 works perfectly on pyshv3 without modification, so we got two flags for the price of one. (Perhaps we found an unintended solution?)

See [`exploit23.py`](exploit23.py) for the code.
