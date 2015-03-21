# Guesspw (100pts)

## Description
```
People kept stealing our flags, so we had our engineers implement a foolproof protection system.

NOTE : no bruteforce required, take it easy
```

## Solution

We are provided with SSH credentials and a server address. After logging in, we find a home directory for the *guesspw* user with a flag and setuid binary inside.

After loading the setuid binary into IDA, it is obvious that static analysis is not the way to go here. We notice that it opens a *password* file, calls *realpath* on something, compares some strings, and has a backdoor that executes */bin/sh*.

Using *strace*, we can infer that the binary expects one argument which is passed to *realpath* and then it is opened along with the *password* file. Clearly, the binary is comparing the password file with the contents of the file we specify as an argument. The question is how to *trick* the setuid binary and bypass the check without actually knowing the password.

The obvious solution is blocked by realpath (e.g. symlink to the password file). A similar solution, which does work, is to provide **/dev/fd/3** as the argument. Since *realpath* is called before the password file is opened, it will pass the *realpath* checks. And because the password file is opened before our file path, **/dev/fd/3** will resolve to **/home/guesspw/password**, bypassing the password verification.

```
user@cg2015-3:/tmp/.foo$ /home/guesspw/guesspw /dev/fd/3
user@\h:\w$ cat /home/guesspw/flag
cheapestflagever
```

## Flag
```
cheapestflagever
```