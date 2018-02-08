   0:  call main
   5:  xor r0, r0
   7:  syscall

main:
   9:  push bp
   b:  mov bp, sp
   d:  sub.t sp, #3c
  12:  mov r5, bp
  14:  sub.t r5, #3
  19:  mov r6, #12345
  1e:  st.t r6, [r5]
  20:  mov r0, #cd # "name>"
  25:  call writestr
  2a:  mov r1, #42
  2f:  mov r5, bp
  31:  sub.t r5, #3c
  36:  mov r0, r5
  38:  call read
  3d:  mov r0, #d3 "bye\n"
  42:  call writestr
  47:  mov r5, bp
  49:  sub.t r5, #3
  4e:  ld.t r6, [r5]
  50:  cmp.t r6, #12345
  55:  jne #5
  5a:  mov sp, bp
  5c:  pop bp
  5e:  ret

read:
  60:  mov r3, r1
  62:  mov r2, r0
  64:  mov r1, #0
  69:  mov r0, #SYS_READ
  6e:  syscall
  70:  ret

writestr:
  90:  push r0
  92:  push r1
  94:  mov r1, r0
  96:  call strlen
  9b:  swp r0, r1
  9d:  call write
  a2:  pop r1
  a4:  pop r0
  a6:  ret

write:
  72:  push r1
  74:  push r2
  76:  push r3
  78:  mov r3, r1
  7a:  mov r2, r0
  7c:  mov r1, #1
  81:  mov r0, #SYS_WRITE
  86:  syscall
  88:  pop r3
  8a:  pop r2
  8c:  pop r1
  8e:  ret

strlen:
  a8:  push r1
  aa:  push r2
  ac:  xor r1, r1
  ae:  xor r2, r2
  b0:  ld.b r2, [r0]
  b2:  cmp.b r2, #0
  b7:  je #c5
  bc:  inc r0
  be:  inc r1
  c0:  jmp #b0
  c5:  mov r0, r1
  c7:  pop r2
  c9:  pop r1
  cb:  ret


