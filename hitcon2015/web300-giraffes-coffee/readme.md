## Giraffe's Coffee - Web 300 Problem - Writeup by Robert Xiao (@nneonneo)

### Description
> Find the flag!<br>
> http://52.69.0.204

### Solution

First thing we do is go to View Source, which tells us to go look at the source code at `index.phps`. Although the web interface only lets you register and login, the source code shows that there are functions for "verify" and "reset" which together allow you to reset a user's password. It's clear that our goal is to reset the password for the `admin` account.

Everything seems escaped properly, so we aren't going to get in via SQLi. Instead, look at the reset password functions. `reset` generates a password reset token which is "mailed" to the IP address that the user originally registered with; passing that token to `verify` will reset the user's password.

The token is generated using `mt_rand`, which is not cryptographically secure. In fact, the first time `mt_rand` is called, PHP will generate a random 32-bit seed and pass it to `mt_srand` (if `mt_srand` has not already been called), and therefore the random number sequence is determined entirely by a single 32-bit number. Furthermore, with `mod_php`, the `mt_rand` state is preserved for all requests in a particular worker process.

We can observe values of `mt_rand` by resetting the password for a newly-registered account and watching port 110 on our machine. Thus, if we can get a *fresh* HTTP worker, then we can bruteforce to find the seed for that worker, and then use HTTP Keep-Alive to continue making requests to that worker with our known `mt_rand` value.

The attached `reset.py` script makes a pair of reset requests to get two consecutive `mt_rand` values, then applies the [Openwall `php_mt_seed` bruteforcer](http://www.openwall.com/php_mt_seed/) to bruteforce the seed. It then resets the admin's password and logs in to get the flag: `hitcon{howsgiraffesfeeling?no!youonlythinkofyourself}`
