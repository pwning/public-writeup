from pwn import *
def solve():
    p = remote("47.89.253.15", 9999)
    # p = remote("47.89.253.15", 9999)
    p.recvuntil("sha256(\"")
    a = p.recvuntil("\"")[:-1]
    prefixes = a.decode()
    print(prefixes)
    answer = input()
    # context.log_level = 'debug'

    p.sendline(answer)
    p.recvuntil("#")
    # p.sendline("apt install -y gdb")
    p.sendline("wget https://github.com/hugsy/gdb-static/raw/master/gdb-7.10.1-x64 && cp gdb-7.10.1-x64 /usr/bin/gdb")
    p.recvuntil("#")
    p.sendline("cd /opt/intel/sgxsdk/")
    p.recvuntil("#")
    p.sendline("source environment")
    p.recvuntil("#")
    p.sendline("cd SampleCode/SealUnseal/")

    p.recvuntil("#")
    p.sendline("cd App && rm App.cpp && wget https://f.fastb.in/App.cpp")
    p.recvuntil("#")
    p.sendline("cd .. && make")
    p.recvuntil("#")
    p.sendline("cp /root/app /root/app_old && cp app /root/app")
    p.recvuntil("#")
    p.sendline("cd /root")
    p.recvuntil("#")
    p.sendline("sgx-gdb app")

    p.interactive()

if __name__ == "__main__":
    import sys
    solve()
