## choices - Reversing Challenge - Writeup by Robert Xiao (@nneonneo)

We're given an LLVM pass module that implements a new LLVM pass (a step in the compilation process), and the command line that generated a particular program.

First, we reverse the `Choices` binary. Basically, it does the typical control-flow flattening trick, where the body of the `calculation` function is basically

    int count = 0;
    memcpy(data, "...", 0x38);

    while(1) {
        scanf("%d\n", &v);
        switch(v) {
            case 2199524334:
                ...
            case ...:
                ...
            case -11373196446:
                return;
        }
    }

with each `case` statement implementing one basic block. The big change here is that `scanf` - it means that instead of automatically deciding which block to run next (by setting the value of `v` at the end of each block), this particular obfuscation technique *asks* the user what to do next. To properly reconstruct the original program we have to *know* what order to call the blocks in, or we'll get garbage.

So, we reverse the `lib0opsPass` pass module. The module's function hook is set to `Oops::OopsFlattening::flatten`, which is a big function that totally rewrites a targeted function (avoiding `main`) by flattening that function's control flow into a large outer loop and an inner switch (plus it even synthesizes the call to `scanf`!)

The salient point is that the switch case numbers are *not* random, but instead generated using a call to `Oops::CryptoUtils::scramble32`, scrambling the original label number (which starts at `Label0` and increments by 1 for each basic block) into the new case number. `scramble32` uses the `CryptoUtils` entropy pool to encrypt each number, and that entropy pool is seeded using AES in counter mode (with the encryption key set to the given seed).

Since we know exactly how the labels are generated, it becomes quite trivial to reimplement the label encryption logic and get the case numbers corresponding to a linear execution of the original function.

[`choices.py`](choices.py) implements the label encryption logic, generating a big list of integers which we can just feed straight into `./Choices`. Upon executing the program, the flag pops out:

    flag{wHy_d1D_you_Gen3R47e_cas3_c0nst_v4lUE_in_7h15_way?}
