#!/usr/bin/env python

import random
import signal
import sys
import traceback
import IPython

PERM_MAPPED		= 0b1000
PERM_READ		= 0b0100
PERM_WRITE		= 0b0010
PERM_EXEC		= 0b0001

TYPE_R = 0
TYPE_I = 1

FLAG_NF = 0b0010
FLAG_ZF = 0b0001

CODE_DEFAULT_BASE   = 0x00000
STACK_DEFAULT_BASE  = 0xf4000

class Stdin:
    def __init__(self, stdin=sys.stdin):
        self._file = stdin

    def read(self, size):
        res = ''
        buf = self._file.readline(size)
        for ch in buf:
            if ord(ch) > 0b1111111:
                break
            if ch == '\n':
                res += ch
                break
            res += ch
        return res

    def write(self, data):
        return None


class Stdout:
    def __init__(self, stdout=sys.stdout):
        self._file = stdout

    def read(self, size):
        return None

    def write(self, data):
        out = ''.join(map(chr, data))
        self._file.write(out)
        self._file.flush()
        return len(out)


class Register:
    def __init__(self):
        self.register = {}
        self.register_list = ['r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7','r8', 'r9', 'r10', 'bp', 'sp', 'pc', 'eflags', 'zero']

    def init_register(self):
        for reg_name in self.register_list:
            self.register[reg_name] = 0

    def set_register(self, reg, value):
        if isinstance(reg, (int, long)) :
            if reg < len(self.register_list):
                reg = self.register_list[reg]
            else:
                self.terminate("[VM] Invalid register")

        elif reg not in self.register:
            self.terminate("[VM] Invalid register")

        self.register[reg] = value

    def get_register(self, reg):
        if isinstance(reg, (int, long)) :
            if reg < len(self.register_list):
                reg = self.register_list[reg]
            else:
                self.terminate("[VM] Invalid register")

        elif reg not in self.register:
            self.terminate("[VM] Invalid register")

        return self.register[reg]

    def regname(self, reg):
        return self.register_list[reg]


class FileSystem:
    def __init__(self):
        self.files = {}

    def load_file(self, filename):
        with open(filename, 'rb') as f:
            self.files[filename] = f.read()

    def open(self, filename):
        if filename in self.files:
            fd = File()
            fd.set_buffer(self.files[filename])
            return fd
        else:
            return -1


class File:
    def __init__(self):
        self.buffer = ''
        self.pos = 0
        self.size = 0

    def set_buffer(self, data):
        self.buffer = data
        self.size = len(self.buffer)

    def read(self, size):
        res = ''
        if self.pos >= self.size:
            return ''

        if self.pos + size >= len(self.buffer):
            res += self.buffer[self.pos : ]
            self.pos = len(self.buffer)
        else:
            res += self.buffer[self.pos : self.pos+size]
            self.pos += size
        return res

    def write(self, data):
        return None


class Memory:
    def __init__(self, size):
        self.memory = [0 for i in range(size)]
        self.pages = {}
        for page in range(0, size, 0x1000):
            self.pages[page] = 0

    def __getitem__(self, key):
        return self.memory[key]

    def __setitem__(self, key, val):
        self.memory[key] = val

    def get_perm(self, addr):
        if (addr & 0b111111111000000000000) not in self.pages:
            return 0
        else:
            return self.pages[addr & 0b111111111000000000000]

    def set_perm(self, addr, perm):
        self.pages[addr & 0b111111111000000000000] = perm & 0b1111

    def allocate(self, new_perm, addr=None):
        if addr:
            if not (self.get_perm(addr) & PERM_MAPPED):
                self.set_perm(addr, (PERM_MAPPED | new_perm) & 0b1111)
                return addr
            else:
                return -1

        for page, perm in self.pages.items():
            if not (self.get_perm(page) & PERM_MAPPED):
                self.set_perm(page, (PERM_MAPPED | new_perm) & 0b1111)
                return page
        return -1

    def check_permission(self, addr, perm):
        if self.get_perm(addr) & (PERM_MAPPED | perm):
            return True
        else:
            return False


class EMU:
    def __init__(self):
        self.config     = {'NX':False}
        self.firmware   = None
        self.is_load    = False
        self.register   = Register()
        self.register.init_register()
        self.pipeline   = []
        self.memory     = Memory(2 ** 20)
        self.checkperm  = []
        self.filesystem = FileSystem()
        self.terminated = False
        self.breakpoints = set()
        self.single_step = False

        self.syscall_table  = [self.sys_exit, self.sys_open,
                               self.sys_write, self.sys_read,
                               self.sys_alloc, self.sys_rand]

        self.op_hander_table = [self.op_load_tri, self.op_load_byte,
                                self.op_store_tri, self.op_store_byte,
                                self.op_mov, self.op_swap, self.op_push,
                                self.op_pop, self.op_syscall,
                                self.op_add_tri, self.op_add_byte,
                                self.op_sub_tri, self.op_sub_byte,
                                self.op_sar, self.op_shl,
                                self.op_mul, self.op_div,
                                self.op_inc, self.op_dec,
                                self.op_and, self.op_or,
                                self.op_xor, self.op_mod,
                                self.op_cmp_tri, self.op_cmp_byte,
                                self.op_jmp_greater, self.op_jmp_less,
                                self.op_jmp_equal, self.op_jmp_not_equal,
                                self.op_jmp, self.op_call]

    def set_timeout(self, timeout = 30):
        def handler(signum, frame):
            print 'timeout!'
            sys.exit(-1)
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(timeout)

    def set_mitigation(self, nx=False):
        if nx:
            self.config['NX'] = nx

    def init_pipeline(self, stdin, stdout):
        self.pipeline.append(Stdin(stdin))
        self.pipeline.append(Stdout(stdout))

    def load_firmware(self, firm_name):
        try:
            with open(firm_name, 'rb') as f:
                data = f.read()

            self.firmware = [ord(byte) for byte in data]
            self.is_load = True


            if self.config['NX']:
                stack_perm = PERM_READ | PERM_WRITE
            else:
                stack_perm = PERM_READ | PERM_WRITE | PERM_EXEC


            for i in range(0, len(data) / 0x1000 + 1):
                self.memory.allocate(PERM_READ | PERM_WRITE | PERM_EXEC, addr=CODE_DEFAULT_BASE + i*0x1000)

            self.write_memory(CODE_DEFAULT_BASE, self.firmware, len(self.firmware))

            for i in range(0, len(data) / 0x1000 + 1):
                self.memory.set_perm(CODE_DEFAULT_BASE + i*0x1000, PERM_MAPPED | PERM_READ | PERM_EXEC)


            self.memory.allocate(stack_perm, addr=STACK_DEFAULT_BASE)
            self.memory.allocate(stack_perm, addr=STACK_DEFAULT_BASE + 0x1000)

            self.register.set_register('pc', CODE_DEFAULT_BASE)
            self.register.set_register('sp', STACK_DEFAULT_BASE+0x1fe0)

        except:
            self.terminate("[VM] Firmware load error")

    def bit_concat(self, bit_list):
        res = 0
        for bit in bit_list:
            res <<= 7
            res += bit & 0b11111111
        return res

    def disas(self, start_addr='pc', limit=10):
        if isinstance(start_addr, str):
            start_addr = self.register.get_register(start_addr)

        disas_queue = set()
        disas_queue.add(start_addr)

        disas_done = set()
        count = 0
        while len(disas_queue) > 0:
            q = sorted(list(disas_queue))
            pc = None
            while len(q) > 0:
                pc = q.pop(0)
                if pc not in disas_done:
                    break;
            disas_queue = set(q)
            if pc is None:
                break
            self.terminated = False
            while not self.terminated:
                if pc in disas_done:
                    break
                op, op_type, opers, op_size = self.dispatch(pc)
                if not self.memory.check_permission(pc, PERM_EXEC) or not self.memory.check_permission(pc + op_size - 1, PERM_EXEC):
                    return
                self.register.set_register('pc', pc + op_size)
                op_handler = self.op_hander_table[op]
                print '%4x:  %s' % (pc, op_handler(op_type, opers, disas=True, disas_queue=disas_queue))
                count += 1
                if count >= limit:
                    return
                disas_done.add(pc)
                pc += op_size
            print

    def bp(self, addr):
        self.breakpoints.add(addr)

    def remove_bp(self, addr):
        self.breakpoints.remove(addr)

    def execute(self):
        try:
            while 1:
                cur_pc = self.register.get_register('pc')
                if cur_pc in self.breakpoints or self.single_step:
                    self.dump_regs()
                    print
                    print 'Breakpoint: %x' % cur_pc
                    self.disas('pc', 1)
                    IPython.embed(display_banner=False)
                op, op_type, opers, op_size = self.dispatch(cur_pc)

                if not self.memory.check_permission(cur_pc, PERM_EXEC) or not self.memory.check_permission(cur_pc + op_size - 1, PERM_EXEC):
                    self.terminate("[VM] Can't exec memory")

                if self.terminated:
                    return

                self.register.set_register('pc', cur_pc + op_size)
                op_handler = self.op_hander_table[op]
                op_handler(op_type, opers)
        except:
            traceback.print_exc(file=sys.stdout)
            print
            self.dump_regs()
            self.terminate("[VM] Unknown error")

    def dump_regs(self):
        for i in xrange(len(self.register.register_list)):
            print '%s = %s' % (self.register.regname(i), hex(self.register.get_register(i)))

    def dump_tri(self, addr, count=10):
        if isinstance(addr, str):
            addr = self.register.get_register(addr)
        tris = self.read_memory_tri(addr, count)
        for tri in tris:
            print '0x%x: %0x%x' % addr, tri
            addr += 3

    def dump_str(self, addr):
        if isinstance(addr, str):
            addr = self.register.get_register(addr)
        print '0x%x: %s' % (addr, self.read_memory_str(addr))

    def dump_bytes(self, addr, count=27):
        if isinstance(addr, str):
            addr = self.register.get_register(addr)
        data = self.read_memory(addr, count)
        print '0x%x:' % addr,
        for d in data:
            print hex(d),

    def dispatch(self, addr):
        opcode = self.bit_concat(self.read_memory(addr, 2))
        op = (opcode & 0b11111000000000) >> 9
        if op >= len(self.op_hander_table):
            self.terminate("[VM] Invalid instruction")

        op_type = (opcode & 0b00000100000000) >> 8
        opers   = []
        if op_type == TYPE_R:
            opers.append((opcode & 0b00000011110000) >> 4)
            opers.append((opcode & 0b00000000001111))
            op_size = 2

        elif op_type == TYPE_I:
            opers.append((opcode & 0b00000011110000) >> 4)
            opers.append(self.read_memory_tri(addr+2, 1)[0])
            op_size = 5

        else:
            self.terminate("[VM] Invalid instruction")

        return op, op_type, opers, op_size


    def read_memory(self, addr, length):
        if not length:
            return []

        if self.memory.check_permission(addr, PERM_READ) and self.memory.check_permission(addr + length - 1, PERM_READ):
            res = self.memory[addr : addr + length]
            return res
        else:
            self.terminate("[VM] Can't read memory")


    def read_memory_str(self, addr):
        res = []
        length = 0

        while 0 not in res:
            res.append(self.memory[addr + length])
            length += 1
        res = res[:-1]
        length -= 1

        if not length:
            return '', 0

        if self.memory.check_permission(addr, PERM_READ) and self.memory.check_permission(addr + length - 1, PERM_READ):
            return ''.join(map(chr,res)), length
        else:
            self.terminate("[VM] Can't read memory")


    def read_memory_tri(self, addr, count):
        if not count:
            return []

        if self.memory.check_permission(addr, PERM_READ) and self.memory.check_permission(addr + count*3 - 1, PERM_READ):
            res = []
            for i in range(count):
                tri = 0
                tri |= self.memory[addr + i*3]
                tri |= self.memory[addr + i*3 + 1]  << 14
                tri |= self.memory[addr + i*3 + 2]  << 7
                res.append(tri)
            return res
        else:
            self.terminate("[VM] Can't read memory")


    def write_memory(self, addr, data, length):
        if not length:
            return

        if self.memory.check_permission(addr, PERM_WRITE) and self.memory.check_permission(addr + length - 1, PERM_WRITE):
            for offset in range(length):
                self.memory[addr + offset] = data[offset] & 0b11111111
        else:
            self.terminate("[VM] Can't write memory")


    def write_memory_tri(self,addr,data_list, count):
        if not count:
            return

        if self.memory.check_permission(addr, PERM_WRITE) and self.memory.check_permission(addr + count*3 - 1, PERM_WRITE):
            for i in range(count):
                self.memory[addr + i*3] =       (data_list[i] & 0b000000000000001111111)
                self.memory[addr + i*3 + 1] =   (data_list[i] & 0b111111100000000000000) >> 14
                self.memory[addr + i*3 + 2] =   (data_list[i] & 0b000000011111110000000) >> 7
        else:
            self.terminate("[VM] Can't write memory")


    # ld.t rA, [rB]
    def op_load_tri(self, op_type, opers, disas=False, disas_queue=None):
        if op_type == TYPE_R:
            if disas:
                return 'ld.t %s, [%s]' % (self.register.regname(opers[0]), self.register.regname(opers[1]))
            src = self.register.get_register(opers[1])
            dst = opers[0]

            data = self.read_memory_tri(src, 1)[0]
            self.register.set_register(dst, data)

        else:
            self.terminate("[VM] Invalid instruction")

    # ld.b rA, [rB]
    # preserves the high bytes
    def op_load_byte(self, op_type, opers, disas=False, disas_queue=None):
        if op_type == TYPE_R:
            if disas:
                return 'ld.b %s, [%s]' % (self.register.regname(opers[0]), self.register.regname(opers[1]))
            src = self.register.get_register(opers[1])
            dst = opers[0]

            ch = self.read_memory(src, 1)[0]
            org_dst = self.register.get_register(dst)
            self.register.set_register(dst, (org_dst & 0b111111111111110000000) | ch)
        else:
            self.terminate("[VM] Invalid instruction")


    # st.t rA, [rB]
    def op_store_tri(self, op_type, opers, disas=False, disas_queue=None):
        if op_type == TYPE_R:
            if disas:
                return 'st.t %s, [%s]' % (self.register.regname(opers[0]), self.register.regname(opers[1]))
            src = self.register.get_register(opers[0])
            dst = self.register.get_register(opers[1])
            self.write_memory_tri(dst, [src], 1)
        else:
            self.terminate("[VM] Invalid instruction")


    # st.b rA, [rB]
    def op_store_byte(self, op_type, opers, disas=False, disas_queue=None):
        if op_type == TYPE_R:
            if disas:
                return 'st.b %s, [%s]' % (self.register.regname(opers[0]), self.register.regname(opers[1]))
            src = self.register.get_register(opers[0])
            dst = self.register.get_register(opers[1])
            self.write_memory(dst, [src & 0b1111111], 1)
        else:
            self.terminate("[VM] Invalid instruction")


    # mov rA, R/I
    def op_mov(self, op_type, opers, disas=False, disas_queue=None):
        if op_type == TYPE_R:
            if disas:
                return 'mov %s, %s' % (self.register.regname(opers[0]), self.register.regname(opers[1]))
            src = self.register.get_register(opers[1])
            dst = opers[0]

            self.register.set_register(dst, src)

        elif op_type == TYPE_I:
            if disas:
                out = 'mov %s, #%x' % (self.register.regname(opers[0]), opers[1])
                next_op, _, _, _ = self.dispatch(self.register.get_register('pc'))
                if opers[0] == 0 and next_op == 8:
                    sc = ['SYS_EXIT', 'SYS_OPEN', 'SYS_WRITE', 'SYS_READ', 'SYS_ALLOC', 'SYS_RAND'][opers[1]]
                    out = 'mov r0, #%s' % sc
                return out
            src = opers[1]
            dst = opers[0]

            self.register.set_register(dst, src)

        else:
            self.terminate("[VM] Invalid instruction")

    # swp rA, rB
    def op_swap(self, op_type, opers, disas=False, disas_queue=None):
        if op_type == TYPE_R:
            if disas:
                return 'swp %s, %s' % (self.register.regname(opers[0]), self.register.regname(opers[1]))
            src = opers[1]
            dst = opers[0]

            org_src = self.register.get_register(src)
            org_dst = self.register.get_register(dst)

            self.register.set_register(src, org_dst)
            self.register.set_register(dst, org_src)

        else:
            self.terminate("[VM] Invalid instruction")


    # push R/I
    def op_push(self, op_type, opers, disas=False, disas_queue=None):
        if op_type == TYPE_R:
            if disas:
                return 'push %s' % self.register.regname(opers[0])
            src = self.register.get_register(opers[0])
            sp = self.register.get_register('sp')

            self.register.set_register('sp', sp-3)
            self.write_memory_tri(sp-3, [src], 1)

        elif op_type == TYPE_I:
            if disas:
                return 'push #%x' % opers[0]
            src = opers[1]
            sp = self.register.get_register('sp')

            self.register.set_register('sp', sp-3)
            self.write_memory_tri(sp-3, [src], 1)

        else:
            self.terminate("[VM] Invalid instruction")


    # pop rA
    def op_pop(self, op_type, opers, disas=False, disas_queue=None):
        if op_type == TYPE_R:
            if disas:
                if opers[0] == 13:
                    self.terminated = True
                    return 'ret'
                return 'pop %s' % self.register.regname(opers[0])
            dst = opers[0]
            sp = self.register.get_register('sp')

            value = self.read_memory_tri(sp, 1)[0]
            self.register.set_register(dst, value)
            self.register.set_register('sp', sp+3)

        else:
            self.terminate("[VM] Invalid instruction")

    # add.t rA, R/I
    def op_add_tri(self, op_type, opers, disas=False, disas_queue=None):
        if op_type == TYPE_R:
            if disas:
                return 'add.t %s, %s' % (self.register.regname(opers[0]), self.register.regname(opers[1]))
            src = self.register.get_register(opers[1])
            dst = opers[0]

            org_dst = self.register.get_register(dst)
            self.register.set_register(dst, (org_dst + src) & 0b111111111111111111111)

        elif op_type == TYPE_I:
            if disas:
                return 'add.t %s, #%x' % (self.register.regname(opers[0]), opers[1])
            src = opers[1]
            dst = opers[0]

            org_dst = self.register.get_register(dst)
            self.register.set_register(dst, (org_dst + src) & 0b111111111111111111111)

        else:
            self.terminate("[VM] Invalid instruction")


    # add.b rA, R/I
    def op_add_byte(self, op_type, opers, disas=False, disas_queue=None):
        if op_type == TYPE_R:
            if disas:
                return 'add.b %s, %s' % (self.register.regname(opers[0]), self.register.regname(opers[1]))
            src = self.register.get_register(opers[1]) & 0b11111111
            dst = opers[0]

            org_dst = self.register.get_register(dst)
            self.register.set_register(dst, (org_dst & 0b111111111111110000000) | ((org_dst + src) & 0b1111111))

        elif op_type == TYPE_I:
            if disas:
                return 'add.b %s, #%x' % (self.register.regname(opers[0]), opers[1])
            src = opers[1]
            dst = opers[0]

            org_dst = self.register.get_register(dst)
            self.register.set_register(dst, (org_dst & 0b111111111111110000000) | ((org_dst + src) & 0b1111111))

        else:
            self.terminate("[VM] Invalid instruction")

    # sub.t rA, R/I
    def op_sub_tri(self, op_type, opers, disas=False, disas_queue=None):
        if op_type == TYPE_R:
            if disas:
                return 'sub.t %s, %s' % (self.register.regname(opers[0]), self.register.regname(opers[1]))
            src = self.register.get_register(opers[1])
            dst = opers[0]

            org_dst = self.register.get_register(dst)
            self.register.set_register(dst, (org_dst - src) & 0b111111111111111111111)

        elif op_type == TYPE_I:
            if disas:
                return 'sub.t %s, #%x' % (self.register.regname(opers[0]), opers[1])
            src = opers[1]
            dst = opers[0]

            org_dst = self.register.get_register(dst)
            self.register.set_register(dst, (org_dst - src) & 0b111111111111111111111)

        else:
            self.terminate("[VM] Invalid instruction")


    # sub.b rA, R/I
    def op_sub_byte(self, op_type, opers, disas=False, disas_queue=None):
        if op_type == TYPE_R:
            if disas:
                return 'sub.b %s, %s' % (self.register.regname(opers[0]), self.register.regname(opers[1]))
            src = self.register.get_register(opers[1]) & 0b11111111
            dst = opers[0]

            org_dst = self.register.get_register(dst)
            self.register.set_register(dst, (org_dst & 0b111111111111110000000) | ((org_dst - src) & 0b1111111))

        elif op_type == TYPE_I:
            if disas:
                return 'sub.b %s, #%x' % (self.register.regname(opers[0]), opers[1])
            src = opers[1]
            dst = opers[0]

            org_dst = self.register.get_register(dst)
            self.register.set_register(dst, (org_dst & 0b111111111111110000000) | ((org_dst - src) & 0b1111111))

        else:
            self.terminate("[VM] Invalid instruction")


    # sar rA, R/I
    def op_sar(self, op_type, opers, disas=False, disas_queue=None):
         if op_type == TYPE_R:
            if disas:
                return 'sar %s, %s' % (self.register.regname(opers[0]), self.register.regname(opers[1]))
            dst = opers[0]
            value = self.register.get_register(opers[1])

            org_dst = self.register.get_register(dst)
            self.register.set_register(dst, org_dst >> value)

         elif op_type == TYPE_I:
            if disas:
                return 'sar %s, #%x' % (self.register.regname(opers[0]), opers[1])
            dst = opers[0]
            value = opers[1]

            org_dst = self.register.get_register(dst)
            self.register.set_register(dst, org_dst >> value)
         else:
            self.terminate("[VM] Invalid instruction")


    # shl rA, R/I
    def op_shl(self, op_type, opers, disas=False, disas_queue=None):
         if op_type == TYPE_R:
            if disas:
                return 'sar %s, %s' % (self.register.regname(opers[0]), self.register.regname(opers[1]))
            dst = opers[0]
            value = self.register.get_register(opers[1])

            org_dst = self.register.get_register(dst)
            self.register.set_register(dst, (org_dst << value) & 0b111111111111111111111)

         elif op_type == TYPE_I:
            if disas:
                return 'sar %s, #%x' % (self.register.regname(opers[0]), opers[1])
            dst = opers[0]
            value = opers[1]

            org_dst = self.register.get_register(dst)
            self.register.set_register(dst, (org_dst << value) & 0b111111111111111111111)
         else:
            self.terminate("[VM] Invalid instruction")


    # mul rA, R/I
    def op_mul(self, op_type, opers, disas=False, disas_queue=None):
         if op_type == TYPE_R:
            if disas:
                return 'mul %s, %s' % (self.register.regname(opers[0]), self.register.regname(opers[1]))
            dst = opers[0]
            value = self.register.get_register(opers[1])

            org_dst = self.register.get_register(dst)
            self.register.set_register(dst, ((org_dst * value) & 0b111111111111111111111))

         elif op_type == TYPE_I:
            if disas:
                return 'mul %s, #%x' % (self.register.regname(opers[0]), opers[1])
            dst = opers[0]
            value = opers[1]

            org_dst = self.register.get_register(dst)
            self.register.set_register(dst, ((org_dst * value) & 0b111111111111111111111))
         else:
            self.terminate("[VM] Invalid instruction")


    # div rA, R/I
    def op_div(self, op_type, opers, disas=False, disas_queue=None):
         if op_type == TYPE_R:
            if disas:
                return 'div %s, %s' % (self.register.regname(opers[0]), self.register.regname(opers[1]))
            dst = opers[0]
            value = self.register.get_register(opers[1])

            if value == 0:
                self.terminate("[VM] Divide by zero")

            org_dst = self.register.get_register(dst)
            self.register.set_register(dst, (int(org_dst / value) & 0b111111111111111111111))

         elif op_type == TYPE_I:
            if disas:
                return 'div %s, #%x' % (self.register.regname(opers[0]), opers[1])
            dst = opers[0]
            value = opers[1]

            if value == 0:
                self.terminate("[VM] Divide by zero")

            org_dst = self.register.get_register(dst)
            self.register.set_register(dst, (int(org_dst / value) & 0b111111111111111111111))
         else:
            self.terminate("[VM] Invalid instruction")


    # inc rA
    def op_inc(self, op_type, opers, disas=False, disas_queue=None):
         if op_type == TYPE_R:
            if disas:
                return 'inc %s' % self.register.regname(opers[0])
            src = opers[0]
            value = self.register.get_register(src)
            value += 1

            self.register.set_register(src, value)

         else:
            self.terminate("[VM] Invalid instruction")


    # inc rA
    def op_dec(self, op_type, opers, disas=False, disas_queue=None):
         if op_type == TYPE_R:
            if disas:
                return 'dec %s' % self.register.regname(opers[0])
            src = opers[0]
            value = self.register.get_register(src)
            value -= 1

            self.register.set_register(src, value)

         else:
            self.terminate("[VM] Invalid instruction")


    # and rA, R/I
    def op_and(self, op_type, opers, disas=False, disas_queue=None):
        if op_type == TYPE_R:
            if disas:
                return 'and %s, %s' % (self.register.regname(opers[0]), self.register.regname(opers[1]))
            src = self.register.get_register(opers[1])
            dst = opers[0]

            org_dst = self.register.get_register(dst)
            self.register.set_register(dst, (org_dst & src) & 0b111111111111111111111)

        elif op_type == TYPE_I:
            if disas:
                return 'and %s, #%x' % (self.register.regname(opers[0]), opers[1])
            src = opers[1]
            dst = opers[0]

            org_dst = self.register.get_register(dst)
            self.register.set_register(dst, (org_dst & src) & 0b111111111111111111111)

        else:
            self.terminate("[VM] Invalid instruction")


    # or rA, R/I
    def op_or(self, op_type, opers, disas=False, disas_queue=None):
        if op_type == TYPE_R:
            if disas:
                return 'or %s, %s' % (self.register.regname(opers[0]), self.register.regname(opers[1]))
            src = self.register.get_register(opers[1])
            dst = opers[0]

            org_dst = self.register.get_register(dst)
            self.register.set_register(dst, (org_dst | src) & 0b111111111111111111111)

        elif op_type == TYPE_I:
            if disas:
                return 'or %s, #%x' % (self.register.regname(opers[0]), opers[1])
            src = opers[1]
            dst = opers[0]

            org_dst = self.register.get_register(dst)
            self.register.set_register(dst, (org_dst | src) & 0b111111111111111111111)

        else:
            self.terminate("[VM] Invalid instruction")


    # xor rA, R/I
    def op_xor(self, op_type, opers, disas=False, disas_queue=None):
        if op_type == TYPE_R:
            if disas:
                return 'xor %s, %s' % (self.register.regname(opers[0]), self.register.regname(opers[1]))
            src = self.register.get_register(opers[1])
            dst = opers[0]

            org_dst = self.register.get_register(dst)
            self.register.set_register(dst, (org_dst ^ src) & 0b111111111111111111111)

        elif op_type == TYPE_I:
            if disas:
                return 'xor %s, #%x' % (self.register.regname(opers[0]), opers[1])
            src = opers[1]
            dst = opers[0]

            org_dst = self.register.get_register(dst)
            self.register.set_register(dst, (org_dst ^ src) & 0b111111111111111111111)

        else:
            self.terminate("[VM] Invalid instruction")


    # mod rA, R/I
    def op_mod(self, op_type, opers, disas=False, disas_queue=None):
        if op_type == TYPE_R:
            if disas:
                return 'mod %s, %s' % (self.register.regname(opers[0]), self.register.regname(opers[1]))
            src = self.register.get_register(opers[1])
            dst = opers[0]

            org_dst = self.register.get_register(dst)
            self.register.set_register(dst, (org_dst % src) & 0b111111111111111111111)

        elif op_type == TYPE_I:
            if disas:
                return 'mod %s, #%x' % (self.register.regname(opers[0]), opers[1])
            src = opers[1]
            dst = opers[0]

            org_dst = self.register.get_register(dst)
            self.register.set_register(dst, (org_dst % src) & 0b111111111111111111111)

        else:
            self.terminate("[VM] Invalid instruction")


    # cmp.t rA, R/I
    def op_cmp_tri(self, op_type, opers, disas=False, disas_queue=None):
        if op_type == TYPE_R:
            if disas:
                return 'cmp.t %s, %s' % (self.register.regname(opers[0]), self.register.regname(opers[1]))
            src = self.register.get_register(opers[1])
            dst = self.register.get_register(opers[0])

            tmp = dst - src
            if tmp == 0:
                eflags = FLAG_ZF

            elif tmp < 0:
                eflags = FLAG_NF

            else:
                eflags = 0b0000

            self.register.set_register('eflags', eflags & 0b111111111111111111111)

        elif op_type == TYPE_I:
            if disas:
                return 'cmp.t %s, #%x' % (self.register.regname(opers[0]), opers[1])
            src = opers[1]
            dst = self.register.get_register(opers[0])

            tmp = dst - src
            if tmp == 0:
                eflags = FLAG_ZF

            elif tmp < 0:
                eflags = FLAG_NF

            else:
                eflags = 0b0000

            self.register.set_register('eflags', eflags & 0b111111111111111111111)

        else:
            self.terminate("[VM] Invalid instruction")


    # cmp.b rA, R/I
    def op_cmp_byte(self, op_type, opers, disas=False, disas_queue=None):
        if op_type == TYPE_R:
            if disas:
                return 'cmp.b %s, %s' % (self.register.regname(opers[0]), self.register.regname(opers[1]))
            src = self.register.get_register(opers[1]) & 0b000000000000001111111
            dst = self.register.get_register(opers[0]) & 0b000000000000001111111

            tmp = dst - src
            if tmp == 0:
                eflags = FLAG_ZF

            elif tmp < 0:
                eflags = FLAG_NF

            else:
                eflags = 0b0000

            self.register.set_register('eflags', eflags & 0b111111111111111111111)

        elif op_type == TYPE_I:
            if disas:
                return 'cmp.b %s, #%x' % (self.register.regname(opers[0]), opers[1])
            src = opers[1] & 0b000000000000001111111
            dst = self.register.get_register(opers[0]) & 0b000000000000001111111

            tmp = dst - src
            if tmp == 0:
                eflags = FLAG_ZF

            elif tmp < 0:
                eflags = FLAG_NF

            else:
                eflags = 0b0000

            self.register.set_register('eflags', eflags & 0b111111111111111111111)

        else:
            self.terminate("[VM] Invalid instruction")


    # jg rA R/I
    def op_jmp_greater(self, op_type, opers, disas=False, disas_queue=None):
        if op_type == TYPE_R:
            if disas:
                return 'jg %s + %s' % (self.register.regname(opers[0]), self.register.regname(opers[1]))
            eflags = self.register.get_register('eflags')
            base = self.register.get_register(opers[0])
            offset = self.register.get_register(opers[1])

            if not (eflags & FLAG_NF) and not (eflags & FLAG_ZF):
                self.register.set_register('pc', (base + offset) & 0b111111111111111111111)

        elif op_type == TYPE_I:
            if disas:
                if opers[0] == 13:
                    target = (self.register.get_register('pc') + opers[1]) & 0x7ff
                    disas_queue.add(target)
                    return 'jg #%x' % target
                return 'jg %s + #%x' % (self.register.regname(opers[0]), opers[1])
            eflags = self.register.get_register('eflags')
            base = self.register.get_register(opers[0])
            offset = opers[1]

            if not (eflags & FLAG_NF) and not (eflags & FLAG_ZF):
                self.register.set_register('pc', (base + offset) & 0b111111111111111111111)

        else:
            self.terminate("[VM] Invalid instruction")


    # jl rA R/I
    def op_jmp_less(self, op_type, opers, disas=False, disas_queue=None):
        if op_type == TYPE_R:
            if disas:
                return 'jl %s + %s' % (self.register.regname(opers[0]), self.register.regname(opers[1]))
            eflags = self.register.get_register('eflags')
            base = self.register.get_register(opers[0])
            offset = self.register.get_register(opers[1])

            if (eflags & FLAG_NF) and not (eflags & FLAG_ZF):
                self.register.set_register('pc', (base + offset) & 0b111111111111111111111)

        elif op_type == TYPE_I:
            if disas:
                if opers[0] == 13:
                    target = (self.register.get_register('pc') + opers[1]) & 0x7ff
                    disas_queue.add(target)
                    return 'jl #%x' % target
                return 'jl %s + #%x' % (self.register.regname(opers[0]), opers[1])
            eflags = self.register.get_register('eflags')
            base = self.register.get_register(opers[0])
            offset = opers[1]

            if (eflags & FLAG_NF) and not (eflags & FLAG_ZF):
                self.register.set_register('pc', (base + offset) & 0b111111111111111111111)

        else:
            self.terminate("[VM] Invalid instruction")


    # je rA R/I
    def op_jmp_equal(self, op_type, opers, disas=False, disas_queue=None):
        if op_type == TYPE_R:
            if disas:
                return 'je %s + %s' % (self.register.regname(opers[0]), self.register.regname(opers[1]))
            eflags = self.register.get_register('eflags')
            base = self.register.get_register(opers[0])
            offset = self.register.get_register(opers[1])

            if (eflags & FLAG_ZF):
                self.register.set_register('pc', (base + offset) & 0b111111111111111111111)

        elif op_type == TYPE_I:
            if disas:
                if opers[0] == 13:
                    target = (self.register.get_register('pc') + opers[1]) & 0x7ff
                    disas_queue.add(target)
                    return 'je #%x' % target
                return 'je %s + #%x' % (self.register.regname(opers[0]), opers[1])
            eflags = self.register.get_register('eflags')
            base = self.register.get_register(opers[0])
            offset = opers[1]

            if (eflags & FLAG_ZF):
                self.register.set_register('pc', (base + offset) & 0b111111111111111111111)

        else:
            self.terminate("[VM] Invalid instruction")

    # jne rA R/I
    def op_jmp_not_equal(self, op_type, opers, disas=False, disas_queue=None):
        if op_type == TYPE_R:
            if disas:
                return 'jne %s + %s' % (self.register.regname(opers[0]), self.register.regname(opers[1]))
            eflags = self.register.get_register('eflags')
            base = self.register.get_register(opers[0])
            offset = self.register.get_register(opers[1])

            if not (eflags & FLAG_ZF):
                self.register.set_register('pc', (base + offset) & 0b111111111111111111111)

        elif op_type == TYPE_I:
            if disas:
                if opers[0] == 13:
                    target = (self.register.get_register('pc') + opers[1]) & 0x7ff
                    disas_queue.add(target)
                    return 'jne #%x' % target
                return 'jne %s + #%x' % (self.register.regname(opers[0]), opers[1])
            eflags = self.register.get_register('eflags')
            base = self.register.get_register(opers[0])
            offset = opers[1]

            if not (eflags & FLAG_ZF):
                self.register.set_register('pc', (base + offset) & 0b111111111111111111111)

        else:
            self.terminate("[VM] Invalid instruction")



    # jmp rA R/I
    def op_jmp(self, op_type, opers, disas=False, disas_queue=None):
        if op_type == TYPE_R:
            if disas:
                return 'jmp %s + %s' % (self.register.regname(opers[0]), self.register.regname(opers[1]))
            base = self.register.get_register(opers[0])
            offset = self.register.get_register(opers[1])

            self.register.set_register('pc', (base + offset) & 0b111111111111111111111)

        elif op_type == TYPE_I:
            if disas:
                if opers[0] == 13:
                    target = (self.register.get_register('pc') + opers[1]) & 0x7ff
                    disas_queue.add(target)
                    return 'jmp #%x' % target
                return 'jmp %s + #%x' % (self.register.regname(opers[0]), opers[1])
            base = self.register.get_register(opers[0])
            offset = opers[1]

            self.register.set_register('pc', (base + offset) & 0b111111111111111111111)

        else:
            self.terminate("[VM] Invalid instruction")


    # call rA R/I
    def op_call(self, op_type, opers, disas=False, disas_queue=None):
        if op_type == TYPE_R:
            if disas:
                return 'call %s + %s' % (self.register.regname(opers[0]), self.register.regname(opers[1]))
            base = self.register.get_register(opers[0])
            offset = self.register.get_register(opers[1])
            ret_addr = self.register.get_register('pc')

            self.op_push(1, [0, ret_addr])
            self.register.set_register('pc', (base + offset) & 0b111111111111111111111)

        elif op_type == TYPE_I:
            if disas:
                if opers[0] == 13:
                    target = (self.register.get_register('pc') + opers[1]) & 0x7ff
                    disas_queue.add(target)
                    return 'call #%x' % target
                return 'call %s + #%x' % (self.register.regname(opers[0]), opers[1])
            base = self.register.get_register(opers[0])
            offset = opers[1]
            ret_addr = self.register.get_register('pc')

            self.op_push(1, [0, ret_addr])
            self.register.set_register('pc', (base + offset) & 0b111111111111111111111)

        else:
            self.terminate("[VM] Invalid instruction")


    # syscall
    def op_syscall(self, op_type, opers, disas=False, disas_queue=None):
        if disas:
            return 'syscall'
        syscall_num = self.register.get_register('r0')
        if 0 <= syscall_num < len(self.syscall_table):
            syscall = self.syscall_table[syscall_num]
            syscall()

        else:
            self.terminate("[VM] Invalid syscall")


    def sys_exit(self):
        self.terminate('[VM] Exiting')


    def sys_open(self):
        filename, filename_len = self.read_memory_str(self.register.get_register('r1'))

        fd = self.filesystem.open(filename)
        if fd != -1:
            self.pipeline.append(fd)
            self.register.set_register('r0', len(self.pipeline) - 1)
        else:
            self.register.set_register('r0', 0b111111111111111111111)


    def sys_write(self):
        fd = self.register.get_register('r1')
        buf = self.register.get_register('r2')
        size = self.register.get_register('r3')

        data = self.read_memory(buf, size)

        if 0 <= fd < len(self.pipeline):
            self.pipeline[fd].write(data)
            self.register.set_register('r0', size)
        else:
            self.register.set_register('r0', 0)


    def sys_read(self):
        fd = self.register.get_register('r1')
        buf = self.register.get_register('r2')
        size = self.register.get_register('r3')

        if 0 <= fd < len(self.pipeline):
            data = map(ord, self.pipeline[fd].read(size))
            self.write_memory(buf, data, len(data))
            self.register.set_register('r0', len(data) & 0b111111111111111111111)
        else:
            self.register.set_register('r0', 0)


    def sys_alloc(self):
        res_ptr = self.register.get_register('r1')
        perm = self.register.get_register('r2')

        addr = self.memory.allocate(perm)
        if addr != -1:
            self.write_memory_tri(res_ptr, [addr], 1)
            self.register.set_register('r0', 1)
        else:
            self.register.set_register('r0', 0)


    def sys_rand(self):
        self.register.set_register('r0', random.randrange(0, 2**21-1))


    def terminate(self, msg):
        print msg
        self.terminated = True
