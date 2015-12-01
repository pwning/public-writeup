## flagFinderRedux - Reverse Engineering 70 - Writeup by Ned Williamson (@nedwill)

`flagFinderRedux` is a reversing problem that checks user input against a computed flag. We can simply break on the `memcmp` to check the expected flag.

```
vagrant@vagrant-ubuntu-wily-64:/vagrant$ readelf -h ./flagFinderRedux-e72e7ac9b16b8f40acd337069f94d524 | grep Entry
  Entry point address:               0x400520
vagrant@vagrant-ubuntu-wily-64:/vagrant$ gdb ./flagfinder-bbc6305273a39e9ccd751c24df86ac61
Loaded 53 commands.  Type pwndbg for a list.
Reading symbols from ./flagfinder-bbc6305273a39e9ccd751c24df86ac61...(no debugging symbols found)...done.
Only available when running
pwn> x/10i 0x400520
   0x400520:	xor    ebp,ebp
   0x400522:	mov    r9,rdx
   0x400525:	pop    rsi
   0x400526:	mov    rdx,rsp
   0x400529:	and    rsp,0xfffffffffffffff0
   0x40052d:	push   rax
   0x40052e:	push   rsp
   0x40052f:	mov    r8,0x400840
   0x400536:	mov    rcx,0x4007d0
   0x40053d:	mov    rdi,0x40063e
pwn>
   0x400544:	call   0x4004f0 <__libc_start_main@plt>
   0x400549:	hlt
   0x40054a:	nop    WORD PTR [rax+rax*1+0x0]
   0x400550:	mov    eax,0x6010ef
   0x400555:	push   rbp
   0x400556:	sub    rax,0x6010e8
   0x40055c:	cmp    rax,0xe
   0x400560:	mov    rbp,rsp
   0x400563:	ja     0x400567
   0x400565:	pop    rbp
pwn> x/10i 0x40063e
   0x40063e:	push   rbp
   0x40063f:	mov    rbp,rsp
   0x400642:	push   r13
   0x400644:	push   r12
   0x400646:	push   rbx
   0x400647:	sub    rsp,0x38
   0x40064b:	mov    DWORD PTR [rbp-0x44],edi
   0x40064e:	mov    QWORD PTR [rbp-0x50],rsi
   0x400652:	mov    rax,rsp
   0x400655:	mov    r12,rax
pwn>
   0x400658:	cmp    DWORD PTR [rbp-0x44],0x2
   0x40065c:	je     0x400681
   0x40065e:	mov    rax,QWORD PTR [rbp-0x50]
   0x400662:	mov    rax,QWORD PTR [rax]
   0x400665:	mov    rsi,rax
   0x400668:	mov    edi,0x400854
   0x40066d:	mov    eax,0x0
   0x400672:	call   0x4004e0 <printf@plt>
   0x400677:	mov    eax,0x1
   0x40067c:	jmp    0x4007ba
pwn>
   0x400681:	mov    eax,DWORD PTR [rip+0x200a05]        # 0x60108c
   0x400687:	mov    esi,eax
   0x400689:	sub    rsi,0x1
   0x40068d:	mov    QWORD PTR [rbp-0x30],rsi
   0x400691:	mov    esi,eax
   0x400693:	mov    r8,rsi
   0x400696:	mov    r9d,0x0
   0x40069c:	mov    esi,eax
   0x40069e:	mov    rdx,rsi
   0x4006a1:	mov    ecx,0x0
pwn>
   0x4006a6:	mov    eax,eax
   0x4006a8:	mov    edx,0x10
   0x4006ad:	sub    rdx,0x1
   0x4006b1:	add    rax,rdx
   0x4006b4:	mov    ebx,0x10
   0x4006b9:	mov    edx,0x0
   0x4006be:	div    rbx
   0x4006c1:	imul   rax,rax,0x10
   0x4006c5:	sub    rsp,rax
   0x4006c8:	mov    rax,rsp
pwn>
   0x4006cb:	add    rax,0x0
   0x4006cf:	mov    QWORD PTR [rbp-0x28],rax
   0x4006d3:	mov    rax,QWORD PTR [rbp-0x28]
   0x4006d7:	mov    esi,0x6010a0
   0x4006dc:	mov    rdi,rax
   0x4006df:	call   0x4004c0 <strcpy@plt>
   0x4006e4:	mov    DWORD PTR [rbp-0x34],0x0
   0x4006eb:	mov    DWORD PTR [rbp-0x38],0x0
   0x4006f2:	mov    rax,QWORD PTR [rbp-0x28]
   0x4006f6:	mov    edx,0x4
pwn>
   0x4006fb:	mov    esi,0x40086a
   0x400700:	mov    rdi,rax
   0x400703:	call   0x400500 <memcmp@plt>
   0x400708:	test   eax,eax
   0x40070a:	jne    0x40077c
   0x40070c:	mov    eax,DWORD PTR [rip+0x20097a]        # 0x60108c
   0x400712:	mov    edx,eax
   0x400714:	mov    rax,QWORD PTR [rbp-0x50]
   0x400718:	add    rax,0x8
   0x40071c:	mov    rcx,QWORD PTR [rax]
pwn>
   0x40071f:	mov    rax,QWORD PTR [rbp-0x28]
   0x400723:	mov    rsi,rcx
   0x400726:	mov    rdi,rax
   0x400729:	call   0x400500 <memcmp@plt>
   0x40072e:	test   eax,eax
   0x400730:	jne    0x400751
   0x400732:	mov    rax,QWORD PTR [rbp-0x50]
   0x400736:	add    rax,0x8
   0x40073a:	mov    rax,QWORD PTR [rax]
   0x40073d:	mov    rsi,rax
pwn> b *0x400729
Breakpoint 1 at 0x400729
pwn> r 9447{wrongflag}
Starting program: /vagrant/flagfinder-bbc6305273a39e9ccd751c24df86ac61 9447{wrongflag}

Breakpoint 1, 0x0000000000400729 in ?? ()
LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
[--------------------------------------------------------REGISTERS---------------------------------------------------------]
 RAX  0x7fffffffe120 <-- '9447{C0ngr47ula...'
 RBX  0x3
 RCX  0x7fffffffe534 <-- '9447{wrongflag}...'
 RDX  0x46
 RDI  0x7fffffffe120 <-- '9447{C0ngr47ula...'
 RSI  0x7fffffffe534 <-- '9447{wrongflag}...'
 R8   0x46
 R9   0x0
 R10  0x377
 R11  0x7ffff7ba4e30 <-- mov    r15b, r13b
 R12  0x7fffffffe170 --> 0x7fffffffe2a8 --> 0x7fffffffe4ff <-- '/vagrant/flagfi...'
 R13  0x69
 R14  0x0
 R15  0x0
 RBP  0x7fffffffe1c0 --> 0x4007d0 <-- push   r15
 RSP  0x7fffffffe120 <-- '9447{C0ngr47ula...'
 RIP  0x400729 <-- call   0x400500
[-----------------------------------------------------------CODE-----------------------------------------------------------]
 => 0x400729    call   0x400500 <memcmp@plt>
        s1:        0x7fffffffe120 <-- '9447{C0ngr47ula...'
        s2:        0x7fffffffe534 <-- '9447{wrongflag}...'
        n:         0x46

    0x40072e    test   eax, eax
    0x400730    jne    0x400751

    0x400732    mov    rax, qword ptr [rbp - 0x50]
    0x400736    add    rax, 8
    0x40073a    mov    rax, qword ptr [rax]
    0x40073d    mov    rsi, rax
    0x400740    mov    edi, 0x40086f
    0x400745    mov    eax, 0
    0x40074a    call   0x4004e0 <printf@plt>

    0x40074f    jmp    0x40075b
[----------------------------------------------------------STACK-----------------------------------------------------------]
00:0000| rax rdi rsp  0x7fffffffe120 <-- '9447{C0ngr47ula...'
01:0008|              0x7fffffffe128 <-- 'gr47ulaT1ons_p4...'
02:0010|              0x7fffffffe130 <-- '1ons_p4l_buddy_...'
03:0018|              0x7fffffffe138 <-- '_buddy_y0Uv3_so...'
04:0020|              0x7fffffffe140 <-- '0Uv3_solved_the...'
05:0028|              0x7fffffffe148 <-- 'ved_the_H4LT1N6...'
06:0030|              0x7fffffffe150 <-- 'H4LT1N6_prObL3M...'
07:0038|              0x7fffffffe158 <-- 'prObL3M_n1c3_}'
[--------------------------------------------------------BACKTRACE---------------------------------------------------------]
>  f 0           400729
   f 1     7ffff7a2fa40 __libc_start_main+240
Breakpoint *0x400729
pwn> x/s 0x7fffffffe120
0x7fffffffe120:	"9447{C0ngr47ula"...
pwn>
0x7fffffffe12f:	"T1ons_p4l_buddy"...
pwn>
0x7fffffffe13e:	"_y0Uv3_solved_t"...
pwn>
0x7fffffffe14d:	"he_H4LT1N6_prOb"...
pwn>
0x7fffffffe15c:	"L3M_n1c3_}"
```

We can see the flag is `9447{C0ngr47ulaT1ons_p4l_buddy_y0Uv3_solved_the_H4LT1N6_prObL3M_n1c3_}`.
