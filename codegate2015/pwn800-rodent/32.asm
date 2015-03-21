[BITS 32]
  push 0x33
  call getpc
getpc:
  add dword [esp], 5
  retf
