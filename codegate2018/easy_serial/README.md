## easy_serial - Reversing Challenge

easy_serial is an unstripped ELF x64 binary that gives us the prompt:
```
Input Serial Key >>>
```
when run with no arguments. Typing in `asdf` and pressing enter gives us the error message `easy: Prelude.!!: index too large`. `Prelude.!!` is list indexing in the Haskell standard library, so we guess that this is a compiled Haskell binary.
This is easily confirmed by running `./easy +RTS --info`, which tells us that it was compiled with GHC 7.10.3.

We then download [gereeter's Haskell Decompiler](https://github.com/gereeter/hsdecomp), which analyzes elf binaries to recover a representation of the constructs that GHC compiled.
After using the tool with `python3 runner.py --inline-constructors ./easy`, we obtain the following (after a list of many closures and constructors):

```
Main_main_closure = >> $fMonadIO
    (putStrLn (unpackCString# "Input Serial Key >>> "))
    (>>= $fMonadIO
        getLine
        (\s1dZ_info_arg_0 ->
            >> $fMonadIO
                (putStrLn (++ (unpackCString# "your serial key >>> ") (++ s1b7_info (++ (unpackCString# "_") (++ s1b9_info (++ (unpackCString# "_") s1bb_info))))))
                (case && (== $fEqInt (ord (!! s1b7_info (I# 0))) (I# 70)) (&& (== $fEqInt (ord (!! s1b7_info (I# 1))) (I# 108)) (&& (== $fEqInt (ord (!! s1b7_info (I# 2))) (I# 97)) (&& (== $fEqInt (ord (!! s1b7_info (I# 3))) (I# 103)) (&& (== $fEqInt (ord (!! s1b7_info (I# 4))) (I# 123)) (&& (== $fEqInt (ord (!! s1b7_info (I# 5))) (I# 83)) (&& (== $fEqInt (ord (!! s1b7_info (I# 6))) (I# 48)) (&& (== $fEqInt (ord (!! s1b7_info (I# 7))) (I# 109)) (&& (== $fEqInt (ord (!! s1b7_info (I# 8))) (I# 101)) (&& (== $fEqInt (ord (!! s1b7_info (I# 9))) (I# 48)) (&& (== $fEqInt (ord (!! s1b7_info (I# 10))) (I# 102)) (&& (== $fEqInt (ord (!! s1b7_info (I# 11))) (I# 85)) (== $fEqInt (ord (!! s1b7_info (I# 12))) (I# 53))))))))))))) of
                    <tag 1> -> putStrLn (unpackCString# ":p"),
                    c1ni_info_case_tag_DEFAULT_arg_0@_DEFAULT -> case == ($fEq[] $fEqChar) (reverse s1b9_info) (: (C# 103) (: (C# 110) (: (C# 105) (: (C# 107) (: (C# 48) (: (C# 48) (: (C# 76) (: (C# 51) (: (C# 114) (: (C# 52) [])))))))))) of
                        False -> putStrLn (unpackCString# ":p"),
                        True -> case && (== $fEqChar (!! s1bb_info (I# 0)) (!! s1b3_info (I# 0))) (&& (== $fEqChar (!! s1bb_info (I# 1)) (!! s1b4_info (I# 19))) (&& (== $fEqChar (!! s1bb_info (I# 2)) (!! s1b3_info (I# 19))) (&& (== $fEqChar (!! s1bb_info (I# 3)) (!! s1b4_info (I# 7))) (&& (== $fEqChar (!! s1bb_info (I# 4)) (!! s1b2_info (I# 2))) (&& (== $fEqChar (!! s1bb_info (I# 5)) (!! s1b3_info (I# 18))) (&& (== $fEqChar (!! s1bb_info (I# 6)) (!! s1b4_info (I# 19))) (&& (== $fEqChar (!! s1bb_info (I# 7)) (!! s1b2_info (I# 3))) (&& (== $fEqChar (!! s1bb_info (I# 8)) (!! s1b4_info (I# 17))) (== $fEqChar (!! s1bb_info (I# 9)) (!! s1b4_info (I# 18))))))))))) of
                            <tag 1> -> putStrLn (unpackCString# ":p"),
                            c1tb_info_case_tag_DEFAULT_arg_0@_DEFAULT -> putStrLn (unpackCString# "Correct Serial Key! Auth Flag!")
                )
        )
    )
s1b4_info = unpackCString# "abcdefghijklmnopqrstuvwxyz"
s1bb_info = !! s1b5_info (I# 2)
s1b5_info = splitOn $fEqChar (unpackCString# "#") s1dZ_info_arg_0
s1b2_info = unpackCString# "1234567890"
s1b3_info = unpackCString# "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
s1b9_info = !! s1b5_info (I# 1)
s1b7_info = !! s1b5_info (I# 0)
```

We can see that the program essentially only has one real function, which was `main`.

The first thing we notice is that the program reads your input into `s1dZ_info_arg_0`.
This is then referenced by `s1b5_info = splitOn $fEqChar (unpackCString# "#") s1dZ_info_arg_0`, which we can correctly guess splits our input into strings separated by the character `#` and stores the result in the list `s1b5_info`.

Familiarity with GHC tells us that the functions `I#` and `C#` are constructors for `Int`s and `Char`s, respectively.
We then notice that `s1b7_info`, `s1b9_info`, and `s1bb_info` refer to the first, second, and third elements of the `s1b5_info` list, respectively, as `!!` indexes into a list.

Despite the decompiler failing to infer that the first `case` statement is an `if`, we are able to guess that `s1b7_info` (the first third of our input) should satisfy the first large expression. It is fairly clearly just checking each character in sequence for equality with a constant. We can reverse this easily using python's regular expression library. We extensively use capturing groups, which let us reference specific parts of the matched string by enclosing them in un-escaped parentheses.

```python
matches1 = re.findall(r"\(ord \(!! s1b7_info \(I# \d+\)\)\) \(I# (\d+)\)", case1)
print(''.join(chr(int(m)) for m in matches1))
```
This gives us the first third of the flag: `Flag{S0me0fU5`.

The second `case` statement pattern matches `reverse s1b9_info` (the reverse of the second third of our input) against a character list (`String`s are lists of `Char`s in Haskell).

```python
matches2 = re.findall(r"\(C# (\d+)\)", case2)
print(''.join(reversed([chr(int(m)) for m in matches2])))
```
This gives us the second third of the flag: `4r3L00king`.

The final `case` statement compares characters in the last third of the input (`s1bb_info`) to characters in `s1b2_info`, `s1b3_info`, and `s1b4_info`, adding a bit of indirection. Fortunately for us, we can do the replacement ourselves and then read it off in the same way we did the first third of the flag.

```python
infos = {
    's1b2_info' : "1234567890",
    's1b3_info' : "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    's1b4_info' : "abcdefghijklmnopqrstuvwxyz",
}

matches3 = re.findall(r"\(!! s1bb_info \(I# \d+\)\) \(!! (s1b._info) \(I# (\d+)\)\)", case3)
print(''.join(infos[which_info][int(idx)] for which_info, idx in matches3))
```

This gives us the final third of the flag: `AtTh3St4rs`. (We notice that we also have to add a trailing `}`.)

This is summarized in the python file [decode.py](./decode.py), which gives us our rather inspirational flag: 
```
Flag{S0me0fU5#4r3L00king#AtTh3St4rs}
```
