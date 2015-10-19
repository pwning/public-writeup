# daybloom (misc 200)

## the intended way

the program did some hashing of memory before and after the shellcode was executed

then it checked if the hashes were equal, and if they were, it wrote the contents of a

buffer back to the client

therefore, the goal was to create a shellcode that left no traces of itself, which read

and wrote the flag to the buffer which is sent to the client

## the unintended way

... is the path i took. i used a timing attack to retrieve the flag byte by byte.

`hitcon{Y@uR $h3LlCo6e 1sT stea1th, B|0om}`
