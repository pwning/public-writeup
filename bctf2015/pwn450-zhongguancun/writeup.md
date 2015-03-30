## zhongguancun - Pwn 450 Problem - Writeup by Robert Xiao (@nneonneo)

zhongguancun implements a electronics store creator which lets us add items (phones or watches) to sell, generate a store menu, and test the store by buying items.

We can add up to 16 items of either type to the store. The item structure contains a vtable pointer as the first entry, which points to a function table for the appropriate item type. The item structure looks like

    struct item_vtable {
        int wholesale(item *this, int qty);
        void tostring(item *this, char *buf);
    };

    struct item {
        struct item_vtable *vtable;
        char name[32];
        char description[80];
        int price;
        int itemtype;
    };

After adding some items, we can create the store menu. The function that creates the menu allocates a 2840-byte buffer, puts a header on it, and then calls `tostring` for each item to add it to the menu. The size of this buffer is very peculiar - maybe it's that way for a reason. Let's try to overflow it.

The store name can be 63 characters long. The longest possible item string we can make is

    Blackberry OS Phone [31 char name] -1000000000 CNY description: [63 char desc]

and if we make 16 of these, the final menu is 2853 bytes long: just barely an overflow (by 13 bytes plus a null byte).

What can we do with a 13 byte overflow? The heap looks like

    [size field] [2844-byte allocation]  [size field] [next allocation]

where the size fields are 4 bytes long. 14 bytes overflows the 4 byte padding on the end of the menu, the 4 byte size field of the next allocation, and the first 5 bytes of the next object. So we can overwrite the first 5 bytes of a heap object. The only heap objects in this program are items, the "money" value for trying out the store, and the menu itself. Overwriting the money value is basically useless, so that leaves the items. Specifically we can overwrite the `vtable` of the item.

Normally we'd just overflow with a pointer to some writable memory (e.g. something we control in `.bss`) and win that way. But, the complicating factor here is that the program actually checks to see if it can write to the `vtable`, and dies if the `vtable` is writable (it performs this check by relying on `read` to EFAULT if the target buffer is not writable). So we can only point the `vtable` at read-only memory.

We choose to point the `vtable` at a shifted copy of the original vtable:

                  ...
    old vtable -> phone::wholesale
    new vtable -> phone::tostring
                  0

such that the target item's `wholesale` function actually calls `phone::tostring`. Now we can use this as a somewhat controlled write, since we can ask for the wholesale price for that item with (almost) any quantity we want, and the quantity will be passed to `phone::tostring` as the destination buffer.

The rest of the exploit then is constructing the victim item so that its `tostring` makes useful changes to memory.

The easy solution is just to overwrite GOT with a guessed pointer to libc, then bruteforce to beat ASLR. I've opted to be a bit more careful and do this without any guessing needed.

We construct the `description` of the victim item so that the end of it overwrites the start of the statically-allocated item table, thus allowing us to corrupt other items. These new items are constructed so that their `price` fields overlap with (1) an entry in the item table and (2) the GOT. We use these two entries to leak heap addresses and libc addresses respectively (by buying the corrupt item and looking at the change in our money). We don't need valid vtable entries for these items.

A third item is corrupted so that its `vtable` points at a pointer to main (from `_start`). This item will allow us to recurse into main, resetting the store registration bit and allowing us to re-enter the store name - we'll use this to write addresses to libc once we know them.

A final fourth item starts on the store name, which we will use to write data from the newly-input store name to the GOT.

We can then ask for the wholesale price of our victim item to trigger the overwrites, then ask to buy our newly corrupted items (1) and (2) to leak pointer values. We ask for the wholesale price of the third item to recurse into main and reset the store flag, write our new GOT entries to the store name, and ask for the wholesale price of the fourth item to overwrite the GOT. Specifically here we choose to overwrite `atoi` with `system`, and finally trigger `system` by asking to buy item number `/bin/bash -i`.

To sum up:
- overflow heap buffer by maximizing item length (with tricks like negative prices)
- use overflow to overwrite vtable to make it a controlled write primitive
- overwrite item entries to achieve the following goals:
    - leak heap address (didn't need this in the end)
    - leak libc address
    - reset store registration flag
    - copy store name to GOT

Running `pwn.py`, we get the flag: `BCTF{h0w_could_you_byp4ss_vt4ble_read0nly_ch3cks}`
