# Piranha Gun (stego 50)

This challenge gives you a shell under some namespaces isolation, and vaguely asks that you find "jungle.chest".

Because you're root in this namespace, you can `mount -t proc proc /proc` to restore procfs to aid in your exploration of this system.

With proc, you can notice that there's a mountpoint at `/chest`, but `/chest` is empty.

As it turns out, this mount is shadowing a file that is in the real `/chest` directory. You can `umount /chest` to view it.

This file is `/chest/jungle.chest`, which contains the flag.

Free fun fact: The `mount` command just uses `/etc/mtab` to show mounts, but `/etc/mtab` is not guaranteed to have anything to do with reality (in fact, you can use `mount -n` and `umount -n` to skip updating `/etc/mtab`, leaving it incorrect). In the case of this challenge, since `/etc/mtab` is from outside the namespace jail, `mount` will show the state of the system outside of the jail. So it doesn't include the `/chest` mountpoint! On linux, the way to get real mount information is to use `/proc/mounts`, or the more modern `/proc/self/mountinfo`.
