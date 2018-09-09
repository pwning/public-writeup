# TWGC — Pwnable Problem — Writeup by Corwin de Boor (@strikeskids)

## Description

A choice-action style problem where you can create and update "variables". You can also
add a reference from one variable to another. In order to resolve these references, we have a
garbage collector.

## Solution

There were a few unintentional bugs in this problem that were not exploitable. However, there is a
clear intentional bug in the garbage collector. When an object is promoted to the major heap,
its references are not recursively moved.

We create an object, force 15 minor collection by allocating, add some children to our original
object, and force another minor collection. This causes the children of our original object
to be collected but leaves their pointers intact. We get a heap leak by overlapping the ref
pointer of a new object with the value pointer. We get an mmap-base leak by overlapping the next-position
pointer of a just-freed object with another value pointer. We note that all of the `mmap` regions are
allocated close together by the kernel, so we use a kernel-dependent offset between them (there aren't
many possibilities).

To actually run the exploit, we construct a fake reference table and overwrite the reference table
of another structure. We get a libc leak by pointing our reference table to a free-list pointer
in the heap. Then, we finish by pointing our reference table to `__malloc_hook`. The only constraint
is we need know the "name" of `__malloc_hook`, which ends up being `""`. We overwrite `__malloc_hook`
with one-gadget.

Unfortunately, this exploit seemed to be dependent on a lot of different offsets, so I had to try
a bunch of different values in order to get things to land on the server once I got them working locally.

Solution script in [exploit.py].