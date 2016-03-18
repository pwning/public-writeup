## manager - Pwnable 287 Problem

We are given some sort of menu-based manager service. The assembly is a
pain to read because the author passed large structures by value
everywhere. After adding a user and logging into the service, there is
an if command that lets the user pass arguments to the ifconfig command,
which is run via popen. the arguments are filtered, but the filter does
not check for `$()`. Passing `$(sh)` gives a sell. A reverse shell was
used to get command output.
