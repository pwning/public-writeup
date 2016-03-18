## cemu - Misc 512 Problem

There are 5 stages of assembly quizzes if we connect to the server. The server emulates x86 code that is provided by the user.

 - Stage 1: Set registers to given values.
 - Stage 2: Set registers such that it satisfies the given mathematical condition.
 - Stage 3: Find a secret value in memory. (Memory scan)
 - Stage 4: Control EIP
 - Stage 5: Read flag
 
We just used pwntool's asm to assemble the insturctions.

Complete exploit is in *exploit.py*.