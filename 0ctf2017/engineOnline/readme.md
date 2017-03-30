## engineOnline – Pwning

engineOnline was a remote pwnable with a provided glibc. The binary implements a kind of model-finder for a user-supplied system of boolean logical equations. As part of this, it ends up executing instructions like a VM. See the writeup for engineTest for more detail on this; both challenges used the same binary.

The rough logic of the program is as follows:

1. Read a user-supplied number `variable_count`. A global heap buffer `bit_buf` of this many bits is allocated.

2. Read a user-supplied list of equations into a heap buffer `prog_buf`. Each equation is a 5-qword long 'instruction', made up of an opcode and several indices into `bit_buf` as operands.

3. Perform a kind of topo-sort on the equations. The 5-qword instructions themselves are not reordered, but a new array is constructed indicating which order the equations should be evaluated in. As part of this step, *the indices mentioned in step 2 are sanitized*.

4. Read a user-supplied list of indices into `bit_buf` and user-supplied values (single bits) to set them to. This setting happens immediately, and *these indices may be out-of-bounds.*

5. Run an interpreter. This evaluates the equations (from step 2) like instructions running in in sorted-order (step 3), manipulating `prog_buf`. The writeup for engineTest has more details, but the gist is you get 4 instructions: single-bit And, Or, Xor, and Ite. Just those. There are no control flow or integer operations. The indices into `bit_buf` have (presumably) already been sanitized (in step 2), and *are not checked here.*

6. Read a user-supplied list of indices into `bit_buf` to print out.

7. If a 'debug' stack variable in the frame of main() got set (not possible without memory corruption), `gets(stack_buffer)` gets called and hands you ROP.

### Solution

The primary bug in the engineOnline binary is the one indicated in step 4 above: a one-shot out-of-bounds write that allows you to overwrite data after the end of a heap buffer. You have bit-level precision with your writes (i.e. you don't need to clobber anything), but ASLR is on so you (apparently) may only target other data on the heap. Because your input write indices are 64-bit values representing bit-indices, you only have 56-bits of range and therefore essentially can only write after the end of `bit_buf` buffer, not before the start of it.

In our exploit, we use this bug to modify `prog_buf`. Although `prog_buf` is user-supplied, it gets sanitized in step 3. We use the step-4 bug to modify `prog_buf` post-sanitization, which allows our VM instructions in step 5 to also access out-of-bounds indices after the end of `bit_buf`.

My exploit works as follows:

1. Send a very large `variable_count` and a very long list of equations, such that glibc's `operator new[]` uses `mmap()` to satisfy these allocation requests. Specific sizes are chosen such that mmap places `bit_buf` before libc (at a consistent offset even when ASLR is on) and `prog_buf` at some point after `bit_buf` (at a consistent offset, so we may edit `prog_buf` using the step-4 bug).

2. Have the VM program read glibc's `environ` variable to find a stack pointer, and overwrite the 'debug' variable from step 7, and copy a libc pointer for later use.

3. Use the step-6 feature to print out that libc pointer we copied. This lets us calculate the absolute address of the glibc magic gadget,

4. Since we overwrote the 'debug' variable, we use the step-7 `gets()` to ROP to the magic gadget.

Achieving step 2 of the exploit is the bulk of this CTF challenge, due to the hyper-limited VM instructions. Because the VM instructions cannot access a dynamic index, you must use self-modifying code techniques to achieve the stack overwrite.

Also, the VM doesn't have any addition instructions, so you need to implement that yourself in order to properly offset from `environ` to target the debug stack variable.

On top of all this, you have to work around the topo-sort from step 3 (step 3 of engineOnline, not the exploit). You have to make sure that your instructions have data dependencies strictly in the order you want them executed (or at least apparently so, before the self-modification takes effect).

An exploit.py attached. In it, I implemented a code-emitter for the VM that takes care of the self-modification overwrites.
