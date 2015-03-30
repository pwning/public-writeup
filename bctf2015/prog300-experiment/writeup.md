## experiment - Programming 300 Problem - Writeup by Robert Xiao (@nneonneo)

The problem consists of 50 questions about integers; if you can answer all of them, you get a flag! The name of the survey ("Overcomplicated Experiment of Integer Syndrome") abbreviates to OEIS, which hints at the Online Encyclopedia of Integer Sequences.

The first 10 questions are a bunch of expressions which you can simply evaluate and determine if they are integers or not. But be careful: occasionally they send you `__import__('os').popen('rm -ri *').read()`, so be cautious if you are using `eval` in Python.

Then they start asking you to give specific items from sequences of integers. First they ask for the nth prime (n < 10000?), then the nth fibonacci number, then the number of unlabeled trees on n nodes. These are all pretty easy to calculate (or find online).

The next 32 questions ask you for elements of sequences from OEIS. So you basically have to search up the sequence based on its description and the first few elements of that sequence, then respond with the nth element from that sequence. Luckily, OEIS provides a downloadable list of names for each sequence (`names.gz`), and for every entry you can find a big list of entries at `oeis.org/Annnnnn/bnnnnnn.txt`. So we just use these two resources to solve these 32 problems.

The last 5 questions ask you for elements of integer sequences that are beyond the ones in the OEIS database, so you have to use some other method to get the desired answers. Here, it is very useful to use the Maple/Mathematica formulae listed on the corresponding OEIS entries to calculate the answers. See the `solve.py` program for a bit more detail (some dependencies are missing but can be computed/downloaded). Once you've answered all the questions, you get a flag - `BCTF{Y0u_h4ve_m0ar_7ermz_than_205}`.
