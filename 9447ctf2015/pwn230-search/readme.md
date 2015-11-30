## Search Engine - Pwn 230 Problem - Writeup by Robert Xiao (@nneonneo)

### Description

> Ever wanted to search through real life? Well this won't help, but it will let you search strings.

> Find it at search-engine-qgidg858.9447.plumbing port 9447.

> search [md5sum=bf61fbb8fa7212c814b2607a81a84adf]

### Reversing

This program implements a very simple "word search" program. You can add a
sentence, which splits the sentence on spaces and allows you to search for the
words in the sentence.

There are two bugs here. First, when you enter 48 chars in `read_int`
(`sub_400A40`) the result is not null-terminated, allowing you to leak stack
data via the error message.

Second, the serious bug is that deleting a sentence (after locating it via
search) erases the sentence contents and frees the sentence, but doesn't remove
the words pointing at the sentence. This opens both a use-after-free bug (which
can be abused to leak information via the sentence printout) and a double-free
bug (which can be abused to corrupt the heap).

### Exploit

We can leak stack addresses via the `read_int` bug, heap addresses by freeing
two consecutive small sentences ("fastbin" sized, i.e. less than 128 bytes
total), and libc addresses by freeing a larger sentence ("smallbin" sized).
Thus, we can fully defeat ASLR. Note that we can search for a deleted sentence
by searching for a word containing all nulls, provided the sentence starts with
a non-null (for a freed chunk, this means the chunk must not be at the end of
the free list).

We can abuse the double free to corrupt the heap by creating three fastbin
sentences, then freeing all three. The result is the free chain
`[head]->a->b->c->NULL`. We can then free `b` again to get
`[head]->b->a->b->...` which results in a cycle. (We can't directly free `a`
because that would trigger glibc's double-free detection).

Now, we can allocate `b` as a sentence and overwrite the first 8 bytes (the
fastbin next pointer) with a pointer `p` of our choosing, since `b` is still
considered free according to `a`'s next pointer. Allocate twice more to put `p`
at the fastbin head. The fourth allocation, then, allocates anywhere in memory
we want _subject to the fastbin metadata constraint_. This constraint means that
the pointer has to have a valid fastbin metadata tag.

In the stack of the `main` function are some pointers like 0x400xxx. We can
deliberately misalign our pointer so that these pointers look like the word
0x000040, which is a valid metadata tag (for a fastbin chunk of size 0x40). I
picked a pointer that is near `main`'s saved EIP. Then, the allocation will let
us write a "sentence" over the saved EIP. Once we request an exit, `main`
returns and hands us a shell.

See the full exploit in `pwn.py`.

### Flag

    9447{this_w4S_heAPs_0f_FUn}
