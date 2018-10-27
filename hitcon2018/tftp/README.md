## tftp

The challenge is a x86-64 Linux service implementing TFTP over TCP. 

The first bug we found was a potential stack buffer overflow in the function
handling a read / write request (e.g. open a file). However, the stack buffer
is passed in from the main function, which never returns, so we quickly gave
up on this bug.

While reviewing the code, we thought that the numerous calls to _syslog_ was
odd and that one of them likely used an attacker-controlled format string.
_syslog_, like the _printf_ family of functions, supports ```%n``` in the
format string which can be used to write arbitrary values to an arbitrary
address.

We found that the error case for an unknown mode when handling a file
request allows the attacker to inject into the _syslog_ format string at
_0x401B31_ with the mode parameter:

```c
    sprintf(state->pkt.msg, "unknown mode %s", state->mode);
    qmemcpy(&v30, &state->pkt, sizeof(v30));
    send_error(v30);
    syslog(3, state->pkt.msg);
```

Since the injection is in _syslog_, we will not be able to use the vulnerability
as an information leak. This makes bypassing ASLR much more difficult. The program
also has a read-only _.got_ so we need to find a different function pointer to
overwrite.

One of the few things we can easily modify are the buffer and state pointers in the
.bss section. We found that by using the ```%hhn``` format string we could overwrite
one byte of the state pointer so that it now points to within the _buffer_ memory,
which contains the packet we send to the server. Due to heap randomization, this
only works about 1 out of 16 attempts, but that is good enough.

Controlling the contents of the state struct is very convenient:

```
00000000 state           struc ; (sizeof=0x35C, align=0x4, mappedto_8)
00000000 direction       db ?
...
00000008 next_time       dq ?
00000010 filename        db 256 dup(?)
00000110 current_file    dq ?                    ; offset
00000118 opening_filename dq ?                   ; offset
00000120 mode            dq ?                    ; offset
00000128 curpos          dd ?
0000012C blksize         dd ?
00000130 delay           dd ?
00000134 num_processed   dd ?
00000138 last_blk        dw ?
0000013A next_blk        dw ?
0000013C input_size      dd ?                    ;
00000140 pkt1_datasize   dw ?
00000142 pkt2_datasize   dw ?
00000144 pkt_length      dd ?
00000148 pkt1            dq ?                    ; offset
00000150 pkt2            dq ?                    ; offset
00000158 pkt             error_packet ?
```

In particular, control of the ```direction```, ```lask_blk```, ```pkt1_datasize```, and ```pkt1``` fields lets us read from an arbitrary memory by sending an _ACK_ packet. When the server sees the _ACK_ packet, it uses the fake state to find the next data block (either _pkt1_ or _pkt2_) that it needs to send the client. We use this arbitrary read to leak a libc pointer from the binary's _.got_.

Next, we want to be able to overwrite a function pointer. We chose to attack the free hook ptr in libc, whose address we can calculate from the leaked _.got_ contents. We achieve an arbitrary write by constructing a fake state with ```current_file = stdin``` (we can leak this using our earlier read) and the other fields set appropriately. When the server processes this _ACK_ packet, it reads from ```stdin``` and writes the data to the buffer pointed to by ```pkt2 + 4```, which we set to the free hook ptr in libc.

After replacing the free hook ptr with ```system```, all calls to _free_ will run _system_ on the string first. The result is that any string constructed by _syslog_ will be executed by _system_, so we can just put ```;/bin/sh;``` in the packet as an unknown mode and we win.