[BITS 64]
  xor r8, r8
  xor rcx, rcx
  xor rdx, rdx
  xor rsi, rsi
  mov rdi, 0x00800000 ; CLONE_UNTRACED
  mov eax, 0x38
  syscall

  test eax, eax
infloop:
  jnz infloop

  xor rdx, rdx
  xor rsi, rsi
  lea rdi, [rel prog]
  mov eax, 0x3b
  syscall

  nop
  int3

prog:
  db './server', 0

