## meow - Reversing Challenge

meow was a 64-bit Linux binary, accessible as a remote service (i.e. a pwnable).

Upon startup, it prompted the user for a 10-character password, checked that the MD5 matched `9f46a92422658f61a80ddee78e7db914`, and then decrypted two blobs of data into RWX memory.

The larger of the two blobs (size 0xB6), which we called `cat_fun`, was made accessible as a function in a menu. As there doesn't seem to be any bug in the non-encrypted code, we're going to have to decrypt the blobs to exploit this program.

Looking at the decryption routine (`sub_D1D`), it appears to decrypt data by permuting the input bytes and XORing on various bytes of the key - it's a very simple algorithm that's probably susceptible to a known-plaintext attack (in this case, we know that at least one of the ciphertexts must decrypt to an x64 function).

The first step was to implement the decryption routine in Python, and have it "symbolically" decrypt an input text to produce a set of constraints (see [`gen_constraints.py`](gen_constraints.py)).

Then, we assumed that `cat_fun` started with a typical x64 prologue `push rbp ; mov rbp, rsp ; sub rsp, 0x?? ; mov ...` and ended with a `ret`. We used Z3 to solve this set of plaintext constraints to recover the key (see [`recover_key.py`](recover_key.py)).

With the key `$W337k!++y` in hand, we decrypted `cat_fun` and the smaller blob, and saw a contrived, trivial stack buffer overflow:

    lea     rax, [rbp+8]
    mov     edx, 18h        ; count
    mov     rsi, rax        ; buf
    mov     edi, 0          ; fd
    mov     eax, 0
    syscall                 ; LINUX - sys_read

Furthermore, the smaller blob decrypted to a set of gadgets, including a `pop rdi` and `execve` code, so it was trivial to put together a payload (see [`exploit.py`](exploit.py)). Running this gave a shell, which we used to obtain the flag:

    flag{what a lovely kitty!}
