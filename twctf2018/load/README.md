# Load — Pwnable Challenge — Writeup by Corwin de Boor (@strikeskids)

## Description

A service that allows you to any section of bytes from a file of your choice into memory. It immediately
exits afterwards.

## Solution

There is simple buffer overflow if you specify too large of a size to read from the file.
If we read from `/proc/self/fd/0` (`/dev/stdin`), then we are able to send data of our choice
as the "file".

Because stdio is closed before returning, we construct a ROP chain to connect to our local server.
We are able to store needed constants and strings in the "filename" in memory by appending data
after the nul with `fgets`. There is no syscall gadget and no provided libc, but we know that
read has a syscall instruction at a small offset. First, we use `/proc/self/mem` to copy the address
of `read` into `.bss`. Then, we use a modification gadget

	0x400a82: add byte ptr [rax], al; sub rsp, 8; add rsp, 8; ret;

to increment the address of read to the syscall instruction.
We use `lseek` to be able to set `rax`, because there is no gadget to load into `rax`.
We set up the `execve` using arguments
we've stored in `.bss`, and jump to the syscall. This indirect jump uses `init` as a stager.

We were unable to get a reverse shell working

	Connection from 35.221.105.100:37948
	bash: cannot set terminal process group (1): Inappropriate ioctl for device
	bash: no job control in this shell
	bash: fork: retry: No child processes
	bash: fork: retry: No child processes
	ls
	ls
	bash: fork: retry: No child processes
	ls
	read(net): Connection reset by peer

so we just sent the flag over by `cat`ting it.

Solution script in [exploit.py].
