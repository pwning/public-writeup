.global open
open:
    mov $0x2,%rax
    syscall
    ret

.global ioctl
ioctl:
    mov $0x10,%rax
    syscall
    ret

.global clone
clone:
    mov $0x38,%rax
    syscall
    ret

.global exit
exit:
    mov $0x3c,%rax
    syscall
    ret

.global fsync
fsync:
    mov $0x4a,%rax
    syscall
    ret

.global setresuid
setresuid:
    mov $0x75,%rax
    syscall
    ret

.global getuid
getuid:
    mov $0x66,%rax
    syscall
    ret

.global execve
execve:
    mov $0x3b,%rax
    syscall
    ret

.global close
close:
    mov $0x3,%rax
    syscall
    ret

.global read
read:
    mov $0x0,%rax
    syscall
    ret

.global write
write:
    mov $0x1,%rax
    syscall
    ret

.global fork
fork:
    mov $0x39,%rax
    syscall
    ret

.global setsid
setsid:
    mov $0x70,%rax
    syscall
    ret

.global socket
socket:
    mov $0x29,%rax
    syscall
    ret

.global nanosleep
nanosleep:
    mov $0x23,%rax
    syscall
    ret

.global gettimeofday
gettimeofday:
  mov $0x60,%rax
  syscall
  ret

.global sched_setaffinity
sched_setaffinity:
  mov $0xcb,%rax
  syscall
  ret

.global msgget
msgget:
  mov $68,%rax
  syscall
  ret

.global msgsnd
msgsnd:
  mov $69,%rax
  syscall
  ret

.global msgrcv
msgrcv:
  mov $70,%rax
  syscall
  ret

.global chmod
chmod:
  mov $0x5a,%rax
  syscall
  ret

.global kill
kill:
  mov $0x3e,%rax
  syscall
  ret
