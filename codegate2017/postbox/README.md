## postbox - Pwnable Challenge

There are two types of objects that are allocated in the same arrays: a post and a user. When the service searches for a post or a user, it distinguishes between them by looking at a type field that is either 0 (post) or 1 (user). This gives us a hint that it is probably a type confusion vulnerability.

The bug is in the delete function. A free block is distinguished by the value -1 in the array of indices. However the delete function doesn't set the last element in the array of indices to -1, instead it gets copied from the array of types. This results in a dangling reference to either object 0 or 1. The delete function also sets the type field to 0, so if we arrange it properly, we can have a dangling reference to a freed user object whose type field was set to 0.

The post objects have function pointers in their structures. These function pointers overlap with a user-controlled string in the user structure. We use this to get RIP-control, which we set to 0x41297F. This results in an execve call with /bin/sh as the target.
