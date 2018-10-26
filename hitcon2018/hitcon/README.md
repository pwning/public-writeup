# hitcon

This problem simulates the schedule for HITCON. First, you choose when and
where each paper's talk should be held. Then, a thousand audience members (of
which you are one) each simultaneous go to their chosen talks. There are some
"nice" audience members that make their choices semi-deterministically. The
rest of the audience members make choices totally randomly. "You" get to
choose which talks you go to.

The main bug is a buffer overflow (`strcpy`, `strlen`) in the handling of the
question you ask. Unfortunately, you are only able to ask questions if the
talk is one of the desirable talks (desired by the "nice" audience members),
only one question can be asked, the "nice" audience members always have a
question, and you always get to ask after them. All this is to say, you need
to split up the nice audience members from yourself so that you have the
opportunity to ask a question. In order to do this, you will upset the "nice"
audience members and cause the conference to be cancelled after the talk.
Basically, we can only trigger the bug once.

Because everything is done on threads, the thread local that you are able to
overflow into occurs directly before the thread control block. Thus, you can
overflow onto the TCB and clobber the TCB self-pointer. This will allow you a
leak when it repeats your question back to you (it offsets from the TCB self-
pointer to find the question variable), and allow you a write when it asks for
your name.

The thread stack is a fixed offset away from the thread control block, so by
a partial overwrite of the TCB pointer, we can address the entire desirable
stack with only a 4-bit ASLR bruteforce. To win, we will find some targets
with proximate desirable addresses and return addresses.

It turns out that libc is allocated a fixed offset again away from the stack
and TCB. Therefore, a stack leak is sufficient to win. First, leak the stack.
Then, overwrite the return address with a one-gadget.

When writing this exploit, I didn't realize this offset was fixed and spent a
long time trying to leak actual libc addresses. All of the available libc
addresses on the stack occurred before any usable return addresses, so I
couldn't directly leak any libc addresses.

I also found a nice way to retrigger the bug by returning to the middle
of the talk function. Because all of the randomization occurred before the
threads were started, I was able to return to right before the
pthread_create and instantly retrigger the bug. As long as I didn't ever
return, I was allowed to continue.

In the end, this was a \~6-bit brute-force: 4 for the ASLR and \~2 bits
for the "nice" randomizations. See the [full exploit](exploit.py).
