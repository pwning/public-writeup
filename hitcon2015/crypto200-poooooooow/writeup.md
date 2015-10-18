# Poooooooow - Crypto 200 problem

This challenge is pretty straight forward. We send a number, and the server
will raise our number to the power of the flag, modulo a large prime number.

We simply note that the order of the group has several small factors (2 as well
as 3 repeated 336 times), which lets us efficiently calculate discrete
logarithms in certain subgroups. We send the number `pow(2, p/(2*3**306), p)`
as the base, which gives us a group of size `2*3**306` in which to work.

When we receive the response, we can easily calculate the discrete logarithm
in our subgroup, as it has a fairly small order. This gives us our flag.
