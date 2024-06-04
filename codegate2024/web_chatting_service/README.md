# Chatting Service&emsp;<sub><sup>Web, 250 points</sup></sub>

_Writeup by [@bluepichu](https://github.com/bluepichu)_

This problem has a lot going on, but almost all of it can be ignored because the `internal` service, which has the flag, is exposed.  This corresponds with the `Flask` service in the handout, which gives us access to a debug interface.  (It's unclear to me if the problem was intentionally configured this way?  I'm assuming that there was some way that attackers were supposed to talk to this service from the main `Go` application, but I didn't really look into that at all once I realized we could just talk to `Flask` directly.)

The internal service has a route `/login` which checks if the specified user and session are valid, and if they are, invokes `internalDaemonService` on the provided command.  This function either adds a message to MySQL, or, if the command starts with `admin://`, sends it along to the `terminal` binary for execution, after checking it against a filter.  Weirdly, none of this requires the user to actually _be an admin_, so we can send `admin://` commands to this service after creating a user and logging in to get a valid session identifier.

My solution to bypassing this filter was to send these three commands in sequence:

```
admin://apt update
admin://echo "y" | apt install "netcat-o$(echo penbsd)" > x && echo done
admin://printf 'get flag\nquit\n' | netcat localhost 11211
```

I'm sure there was a better way to solve this than installing packages as part of my exploit, but this was the first thing I thought of and it was pretty funny.  The third command is the most relevant one; it's talking to the memcached server running in this container, which has the flag at the key `flag`.