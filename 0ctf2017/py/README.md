## py - Reversing Challenge - Writeup by Robert Xiao (@nneonneo)

We're given a `.pyc` file (compiled Python bytecode) where the opcodes have been randomly renumbered. The `.pyc` implements some kind of encryption algorithm, so we're being asked to reverse the encryption to get a flag from an encrypted file. We don't have the corresponding modified interpreter, so we'll have to guess how the opcodes were modified.

Using `hachoir3`, I dumped out the bytecode strings for the module and the two contained functions. The module code looks like this:

    99000099010086000091000099020088000091010099030088000091020099010053

whereas a normal module containing

    import x
    def a():
        pass
    def b():
        pass

has this code:

    6400006401006c00005a00006402008400005a01006403008400005a020064010053

      1           0 LOAD_CONST               0 (-1)
                  3 LOAD_CONST               1 (None)
                  6 IMPORT_NAME              0 (x)
                  9 STORE_NAME               0 (x)

      2          12 LOAD_CONST               2 (<code object a at 0x1005e3ab0, file "crypt_new.py", line 2>)
                 15 MAKE_FUNCTION            0
                 18 STORE_NAME               1 (a)

      4          21 LOAD_CONST               3 (<code object b at 0x1005e3cb0, file "crypt_new.py", line 4>)
                 24 MAKE_FUNCTION            0
                 27 STORE_NAME               2 (b)
                 30 LOAD_CONST               1 (None)
                 33 RETURN_VALUE        

The correspondence is obvious - 0x99 is `LOAD_CONST`, 0x86 is `IMPORT_NAME`, 0x91 is `STORE_NAME`, 0x88 is `MAKE_FUNCTION` and 0x53 is `RETURN_VALUE`. I took the module `opcode.py`, copied it and made [`new_opcodes.py`](new_opcodes.py), which removes all the existing opcodes and adds the new ones. This way, I can run `dis` over the provided `crypt.pyc` and get meaningful results ([`disas.py`](disas.py)):

      1           0 LOAD_CONST               0 (-1)
                  3 LOAD_CONST               1 (None)
                  6 IMPORT_NAME              0 (rotor)
                  9 STORE_NAME               0 (rotor)

      2          12 LOAD_CONST               2 (<code object encrypt at 0x1005e0cb0, file "/Users/hen/Lab/0CTF/py/crypt.py", line 2>)
                 15 MAKE_FUNCTION            0
                 18 STORE_NAME               1 (encrypt)

     10          21 LOAD_CONST               3 (<code object decrypt at 0x1005e3ab0, file "/Users/hen/Lab/0CTF/py/crypt.py", line 10>)
                 24 MAKE_FUNCTION            0
                 27 STORE_NAME               2 (decrypt)
                 30 LOAD_CONST               1 (None)
                 33 RETURN_VALUE        

Then it was just a process of assigning names to each unknown opcode. For example, this looks like `STORE_FAST`:

    encrypt:
      3           0 LOAD_CONST               1 ('!@#$%^&*')
                  3 <104>                    1

At the end, there was just one operator that was unclear. It was a binary operator that took a string on the left side and a number on the right. Possibilities included `[]` (subscript) or `*` (multiply).

I also had to find out what the `rotor` module was. The hint was that the `encrypt` function called `newrotor` as follows:

      7          64 LOAD_GLOBAL              0 (rotor)
                 67 LOAD_ATTR                1 (newrotor)
                 70 LOAD_FAST                4 (secret)
                 73 CALL_FUNCTION            1

Googling `rotor.newrotor` led me to [rotor docs](https://pl.python.org/docs/lib/module-rotor.html), where it seems `rotor` is an ancient encryption module for Python based on the German Enigma that was removed in Python 2.4. Luckily, [`rotormodule.c`](https://hg.python.org/cpython/file/2.3/Modules/rotormodule.c) from Python 2.3 still compiles cleanly against Python 2.7, and produces a usable module.

From there, it was just a matter of reimplementing the decryption algorithm (see [`crypt_new.py`](crypt_new.py)), and testing both possible opcodes. With the multiplication opcode selected, we get a successful flag decryption:

    flag{Gue55_opcode_G@@@me}
