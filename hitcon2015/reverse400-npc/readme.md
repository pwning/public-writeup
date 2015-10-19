## npc - Reversing 400 Problem - Writeup by Robert Xiao (@nneonneo)

### Description

> NPC says "I am NPC."
> 
> npc-4bc7ebfe94c8fdc93832bc0e7af1279b

### Hint

> Check the black/white connected components in 2D grid of cells.

### Reversing

The binary has a long `main` function which appears to be optimized and inlined C++. I used the Hex-Rays decompiler in IDA Pro to decompile it.

There are several stages in the function.

#### Length check

The binary calls `sub_402980` to check the validity of the input length. This function does a bunch of somewhat nasty math which I don't want to reverse. Instead, I take advantage of the fact that the function only proceeds to `memset` if the length check succeeds:

    for ((i=1; i<100; i++)); do echo $i; ltrace -ff ./npc $(python -c "print 'hitcon{' + 'A'*$i + '}'") 2>&1 | grep memset; done

This shows that `memset` is only called on an input length of 80.

#### Input conversion

At 0x400c2a, the binary then sets up some kind of table of size 127, inserting 0x20 values into the table at specific indices. It then runs through the input byte-by-byte, indexing into this table using the ASCII value of each input byte. I dumped the table using GDB, and picked a byte corresponding to a valid value ('A').

Using [qira](https://github.com/BinaryAnalysisPlatform/qira) we can watch this function fill a buffer bit-by-bit. The buffer is filled with 50 bytes of binary data from our 80-byte input, so we guess that each input character is converted into 5 output bits in a base32-like fashion.

#### String unpacking

Next, at 0x400ef5, the binary fills out some kind of array (a C++ vector) using a C++ string (which is initialized from the init function 0x401e60). Again, from laziness, we can just ask GDB to tell us what the vector contains after the function finishes. The vector contains 400 integers. Most are zero, with a few nonzeros between 1 and 8. We call this vector the "map".

#### First loop

At 0x40104a, the binary calls `sub_402490` which sets up two more C++ vectors: one containing the integers 0 to 400, and the other containing 400 1s.

It then goes into a triple loop at 0x401139 which has two nested loop variables going from 0-19. It now becomes clear that the program is operating on a 20x20 grid, and the bitwise operations on the buffer make it clear that the 50-byte input is interpreted as a 20x20 grid of bits. I call the two loop variables `r` and `c` (row and column).

The innermost loop is looping over the pairs in the array `{{1,0}, {0,1}}` which are clearly displacements `(dr, dc)` in the row and column axes respectively. In the innermost loop, the function checks to see if `bit[r,c] == bit[r+dr, c+dc]`. If they are equal, a pair of long `if` chains follows; each chain ends in a block that calls `sub_401FD0`.

On first blush, this function looks complicated since it does a bunch of array lookups and recurses, but I realized it was just recursively inlined. The original function definition resembles the following:

    int f(int **vec, int v) {
        int *x = &vec[0][v];
        if(v != *x) {
            *x = f(vec, *x);
        }
        return *x;
    }

The hint says that we are "checking black/white connected components in 2D grid of cells". Assuming the input represents a 20x20 grid of "black/white" cells, it is now clear that the triple loop is basically gathering the connected components of the input (connected horizontally or vertically), with the `sub_401FD0` function implementing the famous *union-find* algorithm used to group components together.

#### Second loop

In the second set of nested loops, the function checks each number in the map. If the number is nonzero, the function checks if the connected component in the input is black (0) and if it has size equal to the map's number. Thus, the map basically describes the size of the black regions of the input.

#### Third loop

For each nonzero element in the map, this loop inserts the ID of the corresponding black region into a `std::set`. If the region is already inserted, this loop fails, so each black region must correspond to only one nonzero map element.

#### Fourth loop

For each black region in the map, this loop checks to see if the ID is in the set, and fails if it is not. This enforces that each nonzero map element corresponds to exactly one black region, and vice-versa.

#### Fifth loop

This loop iterates over all the white squares and checks to see whether they are all in the same connected component. In other words, all white squares must be connected.

#### Sixth loop

This last loop rejects the input if there are four white squares in a 2x2 box anywhere in the input.

It is this requirement that finally clues me into what's going on here: the map is a Nurikabe puzzle, a Japanese puzzle that requires you to fill in a grid of black and white squares using exactly the same rules as are being checked here.

#### Solving Nurikabe

Armed with this knowledge, I downloaded and tried a few different Nurikabe solvers. The ["DotNet Nurikabe Solver"](http://sourceforge.net/projects/nurikabedotnet/) solved the puzzle, producing the solution

    01000101000100100110
    01011111111111111010
    11101001010010001110
    10100111010101110011
    10011100111101011110
    11110111010011100010
    10001100110100111010
    11100011011111000111
    10111001100010100000
    10000111011110111111
    11111100110011000100
    10010110001100111100
    10101011101010100111
    11101101011111100010
    10101011100010111011
    11011100011110001100
    01001011110001110100
    11111110100111001100
    10101010111101110111
    10101010010110010010

Encoding this solution yields the flag

    hitcon{7O^Im//SAofbOAmFFFS33AY.VF^S=d3YsIo*(AA//FIfDE"=ibiYAi/.ibo11V=-^+JO/Sb-im1si^-D}
