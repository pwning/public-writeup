# REVersiNG

## Beginning

As the name might suggest, REVersiNG is a binary reversing problem. However the name gives us another hint beyond just the problem's category. As we open the binary, we notice that it is beyond large. In fact, when faced with trying to generate its control-flow graph, Hopper simply died. This is because it was generated using `revng`, a tool for translating binaries from one architecture into another.

As the size would suggest, trying to reverse this monstrosity is enormously difficult. Initially, we began investigaating options for trying to rewrite the binary, as many of its constructs were relatively straightforward and could likely have been reduced to something simpler.

Fortunately for us, however, it became readily apparent that we would not need to do this. Suspiciously, the bytes at `0x400000` begin with `ELF`, indicating that maybe their is another binary located in the file. After extracting it and relocating it to `0x400000`, we can see that this was the original executable, a `mips` program with only a few interesting functions.

## Reversing

Without going into too much detail about the actual implementation, the binary first reads a file called `key` (which we assumed to be the flag), then `12` from `/dev/urandom`. After this initialization, it prompts the user for 1 byte, then another 4. Afterwards, it spits out those `12` bytes it read from `/dev/urandom` as well as two identical 128-byte strings.

Diving in a little deeper into the crypto portion of the code, we see that its doing a series of adds, rotates, and xors. In all likelihood, this means that it is likely some form of ARX hash. By drawing out the exact execution flow of the function, we see that it is identical to the Chacha20 hash. 

Now that we know what the operation being performed is, we need to determine what the attack should be. Looking back at out inputs, we see that the crypto function is being called twice with nearly identical arguments. The only bit that changes is the last argument, which iis initially `0`, but becomes `1` during the second pass. Furthermore, that input is being compared to the byte we entered initially. If they are the same, then it looks at the next 4 bytes. It treats those bytes as a pointer, and nulls out whatever is at that byte. 

Now, we have something interesting, we can null out exactly one byte during the process execution. Clearly, we should use this to attack the cipher. At a high-level, what the cipher does is (in 20 iterations), take the input, perform the ARX actions on it, add it to the original input, and return that as the output. Thus, if we can null out the corresponding input byte after its already been mixed as part of the ARX actions, we will then have at that byte just the mixed result. If we consider the `i`th byte of the flag, `Ai` to be the `i`th byte of the input, and `Mi` to be the `i`th byte of the mixed input, then from the first pass we know `Ai+Mi`, and from the second pass wit know `0+Mi`. Thus, if we simply subtract the second result from the first, we get back the original input!

In practice, this is very easy to do, because the point at which we have the overwrite occurs after the data is copied out for the `M` computation, but before it is mixed with `A`. Thus, at that point we can null out the byte we want to extract!

Here is the code that does so

```python
import subprocess
from binascii import hexlify, unhexlify
import random
import sys
from pwn import *

i = 0
p = 0

known = "KNOWN_PLAIN_TEXT" * 8

def random_str():
    global i,p
    #return chr(random.randint(0, 1)) + "\x00\x41".join([chr(random.randint(0, 255)) for i in range(4)])
    if p == 0:
        p = 1
    if p == 1:
        p = 0
        i += 1
    return chr(1) + "\x00\x41" + chr(i / 256 + 0x20) + chr(i % 256)



def trial(num):
    # input_data = subprocess.Popen("/file/rev", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    pipe = remote("pwn1.chal.ctf.westerns.tokyo", 16625)
    input_word = "\x00\x00\x41\x23" + chr(0x20 + num)
    pipe.send(input_word)
    data = pipe.recvall().split("\n")
    if len(data[2]) == 0:
        return "\x00"

    print hexlify(input_word) 

    data1_new = []
    data2_new = []

    for it in range(0, len(data[1]), 2):
       elt = int(data[1][it] + data[1][it+1], 16) ^ ord(known[it/2])
       data1_new.append(elt)
    for it in range(0, len(data[2]), 2):
       elt = int(data[2][it] + data[2][it+1], 16) ^ ord(known[it/2])
       data2_new.append(elt)

    thing = (data1_new[num] - data2_new[num] + 256) % 256
    print(data1_new[num], data2_new[num], thing, hex(thing), chr(thing))
    return chr(thing)
         

final = [trial(i) for i in range(0x10, 0x31)]

str = "".join(final)
print(hexdump(str))
print(repr(str))
with open("final_{}.txt".format(sys.argv[1]), "w") as f:
    f.write(str)

```

Note, that it is possible for this to fail, as the addition could cause a carry which we have no way to track. This is why we run it multiple times and save the output. However in practice, this was not an issue and our initial execution found the flag.