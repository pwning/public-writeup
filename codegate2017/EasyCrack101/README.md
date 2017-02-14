## EasyCrack 101 - reversing

We are given a zip file with 101 binaries in it. Each program takes an argument as input and checks if it passes. All binaries are similarly structured, but the predicates on the input is different per binary.

With simple tools like objdump and grep, we can easily find the goal address, which we can put into angr to solve. During the CTF, we parallelized the process so we can solve things faster.
