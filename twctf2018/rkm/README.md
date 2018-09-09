# ReadableKernelModule — Pwnable/Misc Problem — Writeup by Corwin de Boor (@strikeskids)

## Description

This problem takes the StringIPC vulnerable kernel module from CSAW Finals 2015 and removes the write
primitive.

## Solution

First, we grabbed the solution script from the CSAW problem author and got arbitrary kernel read to work.
We discovered a UAF vulnerability if you have multiple file-descriptors open. This UAF is caused
by not giving a refcount to the `state->channel` variable. Using this UAF, we land a buffer allocation
on top of an old channel allocation (using `realloc` so the buffer is not zeroed). This gives us
a kernel address-space leak.

Now, we land a `seq_operations` structure on top of another UAF channel. This `seq_operations`
structure has 4 function pointers, one of which is directly underneath the `channel->offset` field. By
seeking the channel, we are able to set the function pointer to our desired target. We cause
a `seq_operations` structure to be allocated by opening `/proc/self/comm`.

For the exploit, we put a stack pivot gadget `lea rsp, qword [r10-0x08] ; ret` into the function
pointer. For some reason, we still control `r10` after the user-kernel transition.
We store data in kernel memory by opening a pipe and writing data to it, and we can
find this data with the arbitrary kernel read. In our buffer, we put a ROP chain that calls 
`commit_creds(prepare_kernel_creds(0))`. Then, we jump to a syscall return area, which brings us
successfully to user space.

The whole chain is triggered when the function pointer in the `seq_operations` is called. This
happens upon a read. We set up `r10`, call `read` on the `/proc/self/comm` file descriptor, and then
open a shell (which now has uid 0).

Solution script in [exploit.c].
