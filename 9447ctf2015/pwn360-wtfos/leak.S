mov $0xb0000000, %ebx
mov $708, %ecx
alloc_loop:
  mov $0x14, %eax
  int $0xff
  add $0x1000, %ebx
  dec %ecx
  test %ecx, %ecx
  jnz alloc_loop

xor %ebx, %ebx
mov $0xb02c0ed0, %ecx
mov $0x26, %edx
mov $2, %eax
int $0xff

mov $0xb, %eax
int $0xff

