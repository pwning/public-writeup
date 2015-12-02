bigloop:

mov $0xB0001000, %ebx
movl $4, (%ebx)
movl $0, 8(%ebx)
movl $1, 4(%ebx)

loop:
mov $202, %esi
# 000000007b695f686f70655f6e6f5f6f
# 0000000072697465735f636f64655f6c
# 00000000746869737d00000000000000

#mov $200, %esi
#mov $201, %esi
mov $202, %esi

mov $0x100000,%ecx
xchg_loop:
xchg %esi, 8(%ebx)
loop xchg_loop

mov 4(%ebx), %eax
test %eax, %eax
jnz loop

mov $0x10, %edx
lea 8(%ebx),%ecx
xor %ebx,%ebx
mov $2, %eax
int $0xff

jmp bigloop
