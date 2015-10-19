# risky (rev 300)

## Description

```
RISKY machine

risky-13de1366628df39000749a782f69d894
```

## Reversing

The given binary was a [RISC-V](http://riscv.org/) ELF program that prompts for the correct code. When the correct code is given, the flag is generated and displayed. We couldn't run the binary, so everything was done statically.

We first started by obtaining and building the toolchain for RISC-V system. You can follow [these](http://riscv.org/download.html#tab_tools) instructions to easily set it up. With the tools in our hands, we opened up the binary with objdump ([output](https://github.com/pwning/public-writeup/blob/master/hitcon2015/rev300-risky/risky.disas)).

The program expected 5 groups of 4 letters, separated by dashes (i.e. XXXX-XXXX-XXXX-XXXX-XXXX). Only uppercase alphabets and numbers were allowed. Then, it uses each group of 4 letters as DWORD to do various checks on. The structure is similar to a traditional keygenme's, where you have to find the correct values for each DWORD that satisfy all of the conditions that are being checked -- and only when everything passes, the flag will be computed and printed.

## Solution

We will denote each of the group of letters by the register that contains their value: `s3`, `s2`, `s1`, `s5`, and `s0`, respectively.

As we read the code, we lay out the equations with these DWORDs as variables:

- `s1*s5 + s3*s2 + s0 == 0x181A9C5F`
- `s3*s1 + s2 + s0 == 0x2DEACCCB`
- `s2+s3+s1+s5+s0 == 0x8E2F6780`
- `(s1+s2+s0) * (s3+s5) == 0xB3DA7B5F`
- `s1+s2+s0 == 0xE3B0CDEF`
- `s3*s0 == 0x4978D844`
- `s2*s1 == 0x9BCD30DE`
- `(s2*s1) * (s1*s5) * s0 == 0x41C7A3A0`
- `s1*s5 == 0x313AC784`

Then, we run z3 to get the correct code: `KTIY-ML5M-VK7R-FE5Q-L6DD`. See
[solve.py](https://github.com/pwning/public-writeup/blob/master/hitcon2du015/rev300-risky/solve.py)
for the full solution.

## Flag

Flag: `hitcon{dYauhy0urak9nbavca1m}`
