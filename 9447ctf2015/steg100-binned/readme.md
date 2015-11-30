## binned - Misc 100 Problem - Writeup by Robert Xiao (@nneonneo)

### Description

>  We noticed this binary running in prod. Can you find out what it is hiding? 

### Solution

Disassembling this program shows that it makes a ton of weird system calls, such
as `getpeername` on an unconnected socket, `sysinfo`, `syslog`, and `capget`. We
use `strace` to dump out the full list of syscalls that it calls:

    write(1, "Begin working out flag...\n", 26) = 26
    fork()                                  = 14458
    getpeername(3, 0x7ffdfa5ad500, [16])    = -1 ENOTCONN (Transport endpoint is not connected)
    getpeername(3, 0x7ffdfa5ad500, [16])    = -1 ENOTCONN (Transport endpoint is not connected)
    getsockopt(3, SOL_SOCKET, SO_ERROR, [0], [4]) = 0
    setfsgid(3)                             = 1000
    shmdt(0x7ffdfa5ad44c)                   = -1 EINVAL (Invalid argument)
    getgid()                                = 1000
    getsockname(3, {sa_family=AF_INET, sin_port=htons(0), sin_addr=inet_addr("0.0.0.0")}, [16]) = 0
    sysinfo({uptime=140676, loads=[96, 1024, 2784] totalram=2084810752, freeram=911798272, sharedram=0, bufferram=190918656} totalswap=1071640576, freeswap=1071640576, procs=420}) = 0
    geteuid()                               = 1000
    umask(01)                               = 02
    shutdown(3, SHUT_WR)                    = -1 ENOTCONN (Transport endpoint is not connected)
    setresuid(1000, 1000, 1000)             = 0
    rmdir("10")                             = -1 ENOENT (No such file or directory)
    umask(01)                               = 01
    ftruncate(3, 1000)                      = -1 EINVAL (Invalid argument)
    getpgid(0x387a)                         = 14454
    umask(01)                               = 01
    shmdt(0x7ffdfa5ad44c)                   = -1 EINVAL (Invalid argument)
    getpeername(3, 0x7ffdfa5ad500, [16])    = -1 ENOTCONN (Transport endpoint is not connected)
    bind(3, {sa_family=AF_INET, sin_port=htons(8888), sin_addr=inet_addr("8.8.8.8")}, 4200256616) = -1 EINVAL (Invalid argument)
    bind(3, {sa_family=AF_INET, sin_port=htons(8888), sin_addr=inet_addr("8.8.8.8")}, 4200256616) = -1 EINVAL (Invalid argument)
    setuid(14454)                           = -1 EPERM (Operation not permitted)
    getdents(3, 0x7ffdfa5ad510, 1)          = -1 ENOTDIR (Not a directory)
    syslog(SYSLOG_ACTION_READ, 0x7ffdfa5ad530, 100) = -1 EPERM (Operation not permitted)
    umask(01)                               = 01
    shmdt(0x7ffdfa5ad44c)                   = -1 EINVAL (Invalid argument)
    shutdown(3, SHUT_RDWR)                  = -1 ENOTCONN (Transport endpoint is not connected)
    times({tms_utime=0, tms_stime=0, tms_cutime=0, tms_cstime=0}) = 1732024425
    msgsnd(1, {0, "\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\260C|\0\0\0\0"}, 32, IPC_NOWAIT) = -1 EINVAL (Invalid argument)
    capget(NULL, NULL)                      = -1 EFAULT (Bad address)
    write(1, "Flag worked out!\n", 17)      = 17

Let's look at the syscall numbers corresponding to each of these (64-bit):

    fork = 57
    getpeername = 52
    getpeername = 52
    getsockopt = 55
    setfsgid = 123

Notice that this is `9447{` if you interpret the numbers as ASCII points. Thus,
the syscall numbers must be encoding the flag (ignoring the `write` at the start
and end). Here's the full list of syscall numbers:

    57
    52
    52
    55
    123
    67
    104
    51
    99
    107
    95
    48
    117
    84
    95
    77
    121
    95
    67
    52
    49
    49
    105
    78
    103
    95
    67
    48
    100
    69
    125

which translates to

    9447{Ch3ck_0uT_My_C411iNg_C0dE}
