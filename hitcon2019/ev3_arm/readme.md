# EV3 Arm

We're given a `.rbf` file, a compiled binary for the EV3 robot.

We used [http://ev3treevis.azurewebsites.net/](http://ev3treevis.azurewebsites.net/)
to disassemble the `.rbf` file (disassembly in [disas](disas)), and figured out
that motor A was used for pen rotation, motor B was used for penup/pendown,
and motor C was used for forward/backward movement.

We then wrote a turtle script to draw the flag.

Solve script in [solve.py](solve.py).
