## RedVelvet - Reversing Challenge

Simple reversing binary with many constraints on the input was given. The correct input that passes the check will be the flag.

We use angr to solve it automatically for us :)

```python
import subprocess
import angr
import sys
import simuvex
import claripy


project = angr.Project("./RedVelvet", load_options={'auto_load_libs': False})

addr = 0x4011A9
state = project.factory.blank_state(addr=addr)

def char(state, c):
    return state.solver.And(c <= '~', c >= ' ')

for i in range(27):
    c = state.posix.files[0].read_from(1)
    state.solver.add(char(state, c))

state.posix.files[0].seek(0)
state.posix.files[0].length = 27

ex = project.surveyors.Explorer(start=state, find=0x401534, avoid=0x4007D0)

ex.run()
correct_input = ex._f.posix.dumps(0)
print correct_input[:correct_input.index('\x00')]
```

After a while, we get the flag: `What_You_Wanna_Be?:)_la_la`