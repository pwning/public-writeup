# oemu (1000pts)

## Description
Pwnable for Ubuntu 14.04 64-bit 

## Solution
At first glance, this challenge probably implements a VM of some sort due to the string *Initialize virtual memory*. We also see that it reads in a key, does some stuff, prints *[OK]*, and then does **int 3**. When we connect to the service however, we get a prompt so there is probably a signal handler for the **int 3**. Looking at the xrefs to *sigaction* and *signal* we find a handler for *SIGTRAP* at 0x401702.

The first thing the signal handler does is subtract one from the RIP in context. This effective causes the program is inifinitely loop by executing the **int 3**. Then based on the return value of 0x401178, it may exit the program.

The function at 0x401178 appears to be the main logic for the program. Depending on the state, it may call system, syscall, getchar, or putchar. Looking at the case that doesn't do any of these, we see:

```
    v11 = sub_401B6E(&stru_65BC90, var_9C);
    v12 = sub_401B6E(&stru_65BC90, var_98);
    sub_401C28(&stru_65BC90, var_98, v12 - v11, 1);
    if ( (signed int)sub_401B6E(&stru_65BC90, var_98) <= 0 )
        dword_65BCA8 = v20;
```

The code above could be summarized as read in two values, subtract them, store it back to one of the values, and compare that value to zero. This sounded familiar, and indeed it is an implementation of **subleq**. At this point, a lot of things become obvious, such as 0x606160 is the VM memory and the *key* is used to decrypt this memory. While there are lots of possible values for *key*, the most obvious one to try first was 0xCCCCCCCC, which worked and let us run the program locally.

At this point, we looked up more information about **subleq** and found http://mazonka.com/subleq/ which had a C++ interpreter. This interpreter looked very similar to the binary, so we assumed the binary was derived from this source code. The major difference, besides obfuscation, was the *syscall/system* instruction and the *push* instruction. We reimplemented both of these in the C++ program and copied the VM memory into the source code. With these changes, we now had a working copy of the binary that we could modify and add debug tracing.

When looking at the output of the *help* command, which we guessed, we see that a few of the commands say *priv* next to them. When we try to run these commands, it responds with *Unauthorized*, but we don't see any way to actually authenticate. So, our first challenge is to figure out the authenticate command. While we could try to statically analyze the VM program, it sounded much easier to try some dynamic analysis first.

Our theory was that the VM would *strcmp* our input with some constant strings. We would expect to see instructions that took a byte of our input and then compared it with another byte. We used our custom interpreter to output every instruction as it was executed with pc, A, B, \*A, and \*B, plus *input*, *output*, *push* and *syscall* as appropriate. We then grepped for the first byte of our input (*zzzzzzzzzzzzzzzzzzzzz*), and got this output after uniq:

```
[a]=122 [b]=0 
[a]=122 [b]=100 ('d')
[a]=122 [b]=101 ('e')
[a]=122 [b]=103 ('g')
[a]=122 [b]=104 ('h')
[a]=122 [b]=105 ('i')
[a]=122 [b]=112 ('p')
[a]=122 [b]=113 ('q')
[a]=122 [b]=115 ('s')
[a]=122 [b]=122
[a]=122 [b]=200
```

Now that we have the possible first letters, we repeat this process setting the first letter appropriately, and we get these possible digraphs:

```
de
dm
ex
ge
he
in
pi
qu
se
```

All of these match up with commands that are listed in help, with the exception of *de*. We repeat our process to find the entire string which is:

```
debug#login
```

When we run this command, we are asked for a password. We repeat our process but this time for the password, and we get the string:

```
admin!1234
```

Now we are able to authenticate to the service and can try to exploit it. Our assumption is that we will be required to overflow some buffer which will then overwrite the VM program allowing us to eventually call *system*. We use gdb to dump the VM memory of our interpreter after executing the *set* command, and notice that the variable values are stored at the top of the VM memory and are never freed. The next step is to try to overflow this heap memory into the VM code below by setting a variable to a large string many times. The result was the VM program restarting, so we knew we managed to corrupt the VM program code and cause it to jump back to PC 0. Instead of sending 0x41, we instead send 0xCE which is the beginning of the heap memory, and now the VM just infinitely loops.

At this point we need to write some shellcode for *subleq* that will setup a call to the *syscall* instruction. At the same time, we are limited to ascii values in the memory so we cannot easily put a *syscall* instruction into memory or reference memory outside of 0x000 - 0x100. Our solution was to write shellcode that would write the real code to 0x080 and then jump there [1]. Unfortunately, we can't reference memory beyond 0x0FF, so we had to first write a stager that would allow us to execute more instructions.

The stager shellcode reads in three bytes, an A, a B, and a constant value. The constant value is stored at 0xFF so that it can be used by the generated instruction. The A and B are combined with a constant C to generate an instruction which will do one operation and then go back to the beginning of the stager. This way we execute as many **subleq** as we want, we are just limited by not having branches available to us.

The second shellcode that is read by the stager will slowly construct the real shellcode one byte at a time. The real shellcode we want is:

```
push 0x00 [x10]
push 0x03
push address of "sh\0"
push 0x3B
syscall
```
This will result in a call to *system* with the argument **sh**, giving us a shell.

[1] Based on the other exploits for this challenge, we now know that there is a much easier way to do this. But we documented our solution for compeleteness.

## Flag

```
THE(age)1ofvpPM00ir23VKle is 8888Past
```
