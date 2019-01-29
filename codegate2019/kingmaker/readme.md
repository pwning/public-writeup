## KingMaker - Reversing - Writeup by Robert Xiao (@nneonneo)

We're given a 64-bit binary which runs on a server. The binary has a function containing the following code:

    puts("King : Congratuations to be a king!");
    system("/bin/cat ./flag");

It seems the point of this KingMaker challenge is to figure out how to get there. In `main`, the binary `mprotect`s its entire text section to RWX, indicating some self-modification. The program contains a series of five "tests" - in each test, it asks the user for a password (using `scanf("%s")` - but there's canaries so this isn't super exploitable), checks it against a local file, and then *xor-decrypts* a section of code using that key. You start off as a lowly prince, and your goal is to raise five stats - brave, wise, kind, decision, and sacrifice - all to exactly 5 to become a king and get a flag, by making the right decisions throughout.

I loaded the first segment up in a hex editor, and quickly saw patterns every 4 bytes (which makes sense - they `strncmp` 5 bytes when testing the password indicating that the actual password is 4 bytes long plus a null byte). Guessing that `\x00` was one of the more common bytes, I obtained the password `lOv3`, which when tested on the server turned out to be correct. (This password could also be obtained by guessing that the decrypted code started with `push rbp; mov rbp, rsp`).

That first segment constitutes a single function, which decrypts more code (using the same password), and *that* code decrypts some more code, and calls different functions depending on the choices you make; hence I had to do repeated iterations of "decrypt code, analyze new code, find new encrypted segments". Several of these functions raise the prince's stats by different amounts depending on the choices.

I repeated this process with the other segments, and pretty quickly got the rest of the keys: `D0l1`, `HuNgRYT1m3`, `F0uRS3aS0n`, and `T1kT4kT0Kk`. As before I had to decrypt all the functions they called, all the way down. In total, there were 37 encrypted functions.

With the functions in hand, the final step was to walk through all of the possible paths and work out how they affected the prince's stats. In total I found 8 branches, with around 3-4 choices each, making for less than 10000 possible paths - small enough for bruteforce. So I coded a quick bruteforce script:

    options = [
        [(2, 0, 0, 1, 0), (2, 0, 1, 0, 0), (2, 0, 2, 1, 0)],
        [(0, 0, 1, 0, 2), (0, -1, 0, 0, -1), (0, 2, 0, 0, 0)],
        [(-1, 0, -1, 1, 0), (1, 1, 0, 0, 0), (1, 1, 0, 0, 0), (1, 2, 0, 0, 0)],
        [(1, 1, 1, 2, 0), (1, 1, 1, 1, 2), (1, 2, 2, 1, 2)],
        [(0, 0, 1, 1, 0), (0, -1, 2, 0, 0), (0, -1, 1, 1, 0)],
        [(1, -1, -1, 2, 2), (0, 0, 0, 0, 0), (1, 0, 0, 0, 1), (0, 1, 1, 2, 0)],
        [(0, 1, 0, 0, 0), (0, 1, 1, 1, 0), (0, 1, 0, 0, 0)],
        [(-1, 0, 0, 1, 1), (0, 0, 1, 2, 1), (0, 0, 0, 2, 2)],
    ]

    import itertools

    for combo in itertools.product(*options):
        vec = [0, 1, 1, 2, 0]
        for add in combo:
            for i in range(5):
                vec[i] += add[i]
        if vec == [5,5,5,5,5]:
            print(combo)

This immediately spits out a viable path which ended with all stats equal to five. Translating to in-game commands:

    1
    lOv3
    1
    2
    2
    3
    D0l1
    1
    2
    1
    1
    2
    1
    HuNgRYT1m3
    2
    2
    3
    F0uRS3aS0n
    1
    1
    ALICEALLOFMYPROPERTYISYOURSALICE
    2
    T1kT4kT0Kk
    3
    2
    2
    1

(`ALICEALLOFMYPROPERTYISYOURSALICE` is derived from having to solve a Vigenère cipher, but the key is already given as `ALICE` so it was trivial). This sequence of moves, when piped into the remote server, produces a flag:

    He_C@N'T_see_the_f0rest_foR_TH3_TRee$
