# Seal-Unseal&emsp;<sub><sup>Misc, 451 points</sup></sub>

_Writeup by [@ath0](https://fastb.in)_

I worked on this challenge with [Mindy]().

They give us four files, and with a little online scavengery we found that they are based on [a sample](https://github.com/intel/linux-sgx/tree/master/SampleCode/SealUnseal) from the official SGX SDK. The sample happens to share the name of the challenge.

## About the challenge architecture
- `app` is the binary that you run just like any other userspace binary. It is responsible for loading the (signed) enclave binaries via SDK functions such as `sgx_create_enclave`. We noticed that, unlike the App.cpp provided in the SDK sample, this binary does not make any calls to load the 'unseal' enclave.
- `libenclave_seal.signed.so` -- uses some crypto to encrypt a global string (at 0x282000). The string reads `rwctf{}`, but presumably they replaced this with the actual flag when they actually sealed it.
- `sealed_data_blob.txt` is where the `app` binary writes the sealed bytes that are produced by the `libenclave_seal.signed.so`.
- `libenclave_unseal.signed.so` -- this is a signed binary that contains the necessary logic to unseal the sealed data, and compares it with a constant string. Notably, this binary does not return the string back to the `app` binary -- it simply checks that it unseals as expected.


We didn't know a lot about SGX, but I knew that if we didn't have a signed binary that could unseal and give us the unsealed bytes, we were *theoretically* toast. Enclave memory is supposed to be encrypted so even the host OS cannot read it. But this was a "baby" challenge, so there must be a catch. SGX enclaves can be compiled in debug mode, in which you can literally just attach GDB and poke around at enclave memory.

In `app`, the call to `sgx_create_enclave` is as follows:

```
sgx_create_enclave("libenclave_seal.signed.so", 1, 0, 0, &var_28, 0)
```

The second argument [is the debug flag](https://github.com/intel/linux-sgx/blob/master/common/inc/sgx_urts.h#L88)! This means the enclaves were compiled in debug mode, so we should just be able to attach GDB to the unseal enclave at the right time and dump the flag...

Only, it doesn't work! Locally we were getting `SGX_ERROR_MAC_MISMATCH`, and the decrypted data seemed like garbage. It seems like we must not have the right keys? We realized (and apparently so had a bunch of other people) that the challenge was broken -- the key depends on the chip, and we didn't have access to the hardware used to generate the challenge.

Eventually the organizers got infra up so that we could run on the same machine that performed the seal, but it was pretty slow and we had trouble getting sgx-gdb to run and break in the right spot before our connections would time out. With time running out (we had less than half an hour remaining) we found that the decrypted data actually remained in one of the mapped `/dev/sgx` memory mappings **even after the enclave call had returned**, and locally we were able to dump it with `dd`.

For the final solution, we were finally able to get gdb to run long enough that we just used the `find` command to search the largest of the `/dev/sgx` memory mappings for the flag, after unseal had been run. See `App.cpp` for our very lighly modified verison of the App.cpp (we were able to compile it on remote, see `solve.py`).


