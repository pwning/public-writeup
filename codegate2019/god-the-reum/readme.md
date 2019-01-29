##god-the-reum

We are given a binary program that provides a simple wallet service.

```
====== Ethereum wallet service ========
1. Create new wallet
2. Deposit eth
3. Withdraw eth
4. Show all wallets
5. exit
```

The vulnerable code resides in the `withdraw` function located at `0xF2E`. This function frees a heap pointer if the value at it is 0, but does not clear out the value. This allows us to use the `show` function to "use" the pointer to leak out the heap address.

Since the challenge is running with the libc that has `tcache` enabled, we can abuse the double-free to eventually leak out the libc address when the freed chunk is put into the unsorted bin. In order to do that, we just have to make sure that we have allocated another chunk (such that `top` pointer isn't just moved and make the next pointer to be NULL), and `tcache` is full with 7 more frees.

After that, we should be able to use `show` function to leak out the libc address. From here we use the `developer` menu (which is a hidden menu with option 6), we can modify the next pointer of the `tcache` link to be `__free_hook`, then finally we could write the one-shot gadget address to it, again using the `developer` menu.

Triggering the one-shot gadget is simply to cause it to call `free` by withdrawing.