# Zoo - Pwnable Challenge

This service implements a zoo simulator where you can adopt,
feed, clean, and care for your animals.

    struct animal {
        bool valid;
        char name[20];
        struct item* food[20];
        char *species;
        struct item* dung[25];
        int likes;
        int food_tl;
        int food_hd;
        int dung_tl;
        int dung_hd;
        bool ill;
        bool hasMedicine;
    };

    union item {
        char *type;
        struct medicine meds;
    };

    struct medicine {
        char *type;
        long long dungpos;
        char name[8];
        char description[0x68];
    };

The animal struct implements two ring-buffers for the food
and the dung items.

The zoo and the animals are preallocated at the start of the binary.
After that, the only things allocated or freed are the `struct item`s, which
all have the same size.

The main bug is a heap buffer overflow in the description field of the medicine.
This allows you to overrun and completely control the prev-size and size fields
of the follow heap chunks.

There is also a nul-termination bug in the animal `name` field that allows
you to get a heap address leak. If you make a name of exactly 20 characters long,
when you feed the animal it will print out the name in addition to the address
of the first food.

The final bug is a contrived action that allows you to overwrite
the data in any of the items that do not look like they were produced by
the program---it lets you write stuff when it notices corruption.

The exploit is complicated by the fact that the dung is not always produced
when you feed the animal. Rather, it is only produced when the animal
has sufficient food and the food count is odd.

In order to trigger the first bug, many dung need to be produced to make the animal
sick. Then, visiting the hospital prescribes the animal with medicine. Instead of
feeding the animal food, the `feed` function feeds medicine, allowing you to
trigger the main vulnerability.

The exploit does the following

1. Trigger the first vulnerability to get a heap leak
2. Reserve a two items to be freed later.
2. Adopt more animals and hospitalize two of them, enabling medicinal feeding for both
3. Have the adopted name fields simulate the size field and the fwd pointer of a heap chunk.
4. Free the item, enabling a medicine to land at the beginning of the heap. Using this medicine,
overflow the size and prev-size field of the next chunk. Simulate a large free chunk followed by
the next chunk. In addition, have this medicine itself simulate the fwd and bwd ptrs of the
chunks before and after the large chunk in the free list.
5. Free the next item, consolidating backwards into the large chunk. This large chunk will be
`unlinked` from the list (unlinking from the simulated chunks in the medicine).
6. Allocate to use up the remaining free chunks
7. Prepare the animal after the target for the contrived exploit (take the animal on many walks).
7. Allocate medicine on top of the fake chunk, landing first on the item pointers and then on
the species pointer.
8. Point the species pointer at the current location of the fwd and bwd pointers of the large chunk
in order to leak a libc address
9. Allocate another medicine chunk, landing on top of the item pointers in the next animal. Set things
up so that there are no non-zero values in the item pointers. Additionally, set another
item pointer to the item pointers array so that we can clear the data left by malloc
on the item pointers.
10. Using an item pointer, overwrite `__free_hook` with the address of `system`. Also,
add a new item pointing to `"/bin/sh"` (stored in the owner of the zoo) as the next food to be used up.
11. Use up the next food, freeing `"/bin/sh"`.
