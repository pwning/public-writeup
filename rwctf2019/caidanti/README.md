## caidanti (Flag 1) - rev problem - 167 points (26 solves)

We're given a bundle that launches a Fuchsia VM. We're also given a nice
menu-style pwnable with which we're all duly familiar. This one is great
though because if you use menu option 114514, it will execute your
shellcode! How hard can this be?

First off: syscalls in Fuchsia are a bit annoying--they can't be called
directly, only through the VDSO which is randomized. Luckily for us
when our shellcode is called, there's a pointed in the VDSO in the rcx
register. That helps a bit, but even writing data back out to the screen
is not easy through the direct syscalls. Instead we also use a pointer
on the stack which goes into the FDIO library--the convenience functions
for "standard" IO type things.

Because shellcode is annoying, we end up using the 
[shellcode compiler](https://scc.binary.ninja/) from Binary Ninja. With
a bit of work we can use this to write C code to call all
the stuff we want.

Unfortunately, the flag isn't inside our executable `caidanti`, it is
inside the companion program `caidanti-storage-service`. This means
we need to do IPC calls (or FIDL calls, if you live in Fuchsia land)
to fetch the flag from the storage service.

Additionally, the handle IPC channel is random, and unlike a Unix system it
is not just a small integer we can guess. Instead we find a pointer
to the base of our executable, and from that we are able to get the
proper handle.

Normally FIDL generates templates you can use to talk to other apps, but
don't have that. Instead we reverse engineer the storage service program
to find out what the raw IPC message it wants to receive is. After some
work we figure out the message we need to send. Due to laziness, we
use the asynchronous calls and read until there is data. Because we use the
low level calls and not FIDL itself, we print some extra data back.

Putting that all together, we end up with some [shellcode](part1.c)
(here presented in C that we compile with the shellcode compiler),
plus a small stub of assembly to extract our register and stack values of
libraries we want that we put into our [python exploit script](exploit.py).

Given we started with code execution, we find we agree with the flag
`rwctf{Turns_out_this_is_harder_than_expected}`

## caidanti (Flag 2) - pwn problem - 320 points (9 solves)

One of the FIDL IPC commands we can execute is the `GetContent` call, which is
supposed to read the contents of a particular item from the storage service.
What this call actually does, however, is receive a handle to a virtual memory
object (VMO) from the storage service and map this VMO into `caidanti`'s memory
space - basically, a shared memory mapping. Reversing
`caidanti-storage-service`, we found that this VMO region contained the entire
"database" C++ object which implemented the storage service. This included a
virtual function table pointer, a pointer to the shared memory region (in the
address space of the service), a pointer to a stack object, and all 16 of the
key-value pairs which made up the database.

Because this memory region is shared between the two processes, it's possible to
use our shellcode running inside `caidanti` to modify the shared memory, and
thereby modify the database object which lives in `caidanti-storage-service`.
By carefully corrupting pointers (such as virtual function table pointers) we
can take control over the service, which will allow us to read flag 2 which only
it has access to.

First, we noted that the keys of the database ("secrets") were stored using a
form of C++ `string`, which meant that we could overwrite them with pointers to
data and then leak that data using the `ListKeys` FIDL call. The existing
pointers in the VMO revealed the executable base address and VMO address, so we
used the `ListKeys` leak to leak out libc, fdio, and vDSO pointers, then leaked
out the random XOR keys used to encrypt pointers for `longjmp`.

To achieve code execution, we overwrote the virtual function table pointer for a
`std::function` object stored in the VMO, which is called as the service is
being shutdown (which we can trigger with a `Reset` FIDL call). Usefully, the
relevant virtual function call looks like `func->vtable->call((char
*)(&func)+16)`, which allows us to put arbitrary data at `func+16`. We used this
to call `longjmp` with a fake `jmpbuf` at `func+16`, and chained it into a stack
pivot which pivoted the stack into the VMO. From there, a quick ROP chain was
used to read the flag and dump it into the VMO region for our shellcode to read.

We didn't have to modify our exploit script, only the shellcode
([`part2.c`](part2.c)). Running this exploit gives us the flag after a few
moments:
`rwctf{No_wonder_there_is_zero_reference_to_fuchsia::mem::Range_in_their_codebase}`.
