## Serial - Pwnable 444 Problem

A simple x64 problem where you can add, remove, and dump items from an array.
An item is a structure similar to:
```
struct item {
    char data[24];
    void (*dump_func) (struct item []);
};
```
However, the code that adds a new item first sets the *dump_func* pointer and 
then uses strlen plus memcpy to write the data. The source pointer is a
32-byte attacker controlled string, so a trivial overflow of the function
pointer is possible.

The function pointer gets called when we use the dump items command. It only
uses the function pointer from the first item in the array, however. Also,
the argument to the function is the item array, which happens to start with
an attacker-controlled string.

First we needed to figure out a valid key to connect to the problem. This is
easily done manually or with Angr. The key is: **615066814080**.

Basic overview of the exploit:
 - Send key
 - Add item with format string that will print a libc address from the stack,
   and overwrite the function pointer to point to **printf**
 - Dump items to get the a leaked pointer into **libc_start_main**
 - Calculate the address of **system** using the leaked pointer
 - Remove the first item
 - Add item with shell command, and overwrite the functionp pointer to
   **system**

Complete exploit is in *exploit.py*. Sample output:
```
[+] Opening connection to 175.119.158.133 on port 23232: Done
0x7fd7480fcba0
0x7fd7480a8000
0x7fd7480ec3d0
[*] Switching to interactive mode
>> func : 0x7fd7480ec3d0
$ cat /home/serial/flag
flag is {Do_Y0u_like_Funct10n_pOint3r?:D}
```
