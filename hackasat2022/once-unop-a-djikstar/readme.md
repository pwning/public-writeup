# Once Unop a Djikstar

## Description

The challange is a Djikstar algorithm problem. We are given 3 CSV files which contain distances between the stars, and we are asked to find a path from our ship "ShippyMcShipFace" to the destination "Honolulu". Normal Dijkstra seems not working on this challenge, maybe the cost is not simply the sum of all distances.<!--more-->

However, the challenge also provided us with a Rust solver for this problem, but some parts of the code are patched by NOPs, making this program unable to run. Our task there is to fix this program.

## Fixes

The main logic is at function `once_unop_a_dijkstar::run`. There are 5 locations replaced by NOPs, we need to figure out what the original instructions were.

### Location #1 0x16BA0

The program first opens 3 CSV files to read the distance data. The first read operation is corrupted:

```
lea     rax, _ZN3csv6reader54Reader$LT$csv__reader__Reader$LT$std__fs__File$GT$$GT$9from_path17h5f1475e34a316447E ; csv::reader::Reader$LT$csv..reader..Reader$LT$std..fs..File$GT$$GT$::from_path::h5f1475e34a316447
lea     rdi, [rsp+9E8h+var_7C8] ; retstr
lea     rsi, [rsp+9E8h+var_738]
call    rax ; csv::reader::Reader$LT$csv..reader..Reader$LT$std..fs..File$GT$$GT$::from_path::h5f1475e34a316447 ; csv::reader::Reader$LT$csv..reader..Reader$LT$std..fs..File$GT$$GT$::from_path::h5f1475e34a316447
nop
nop
nop
nop
nop
nop
nop
nop
nop
lea     rdi, [rsp+9E8h+src] ; retstr
lea     rsi, [rsp+9E8h+var_7C8]
call    rax
```

We should not call same rax for 2 times. Apparently, we need a `lea rax` to set rax to another function. We can look at the other 2 read operations, and find out that a `_$LT$core..result..Result$LT$T$C$E$GT$$u20$as$u20$core..ops..try_trait..Try$GT$::branch` should be called after `csv::reader::Reader$LT$csv..reader..Reader$LT$std..fs..File$GT$$GT$::from_path`.

The first patch is changing `0x16BA0` to `lea rax, [0x30EA0]`.

### Location #2 0x16DB7

```
mov     [rsp+9E8h+var_938], rdi
mov     edx, 88h        ; n
mov     [rsp+9E8h+var_930], rdx
mov     rax, cs:memcpy_ptr
mov     [rsp+9E8h+var_928], rax
call    rax ; __imp_memcpy
mov     rsi, [rsp+9E8h+var_938] ; src
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
lea     rdi, [rsp+9E8h+var_690] ; dest
call    rax
```

A similar pattern of `mov rax, cs:memcpy_ptr` and `call rax` can be found at `0x16D9E` and `0x16F15`.

The second patch is changing `0x16DB7` to `mov rdx, [rsp+0xb8]` and `mov rax, [rsp+0xc0]`.

### Location #3 0x18AF8

After reading 3 CSV data files, we find a crash inside a small function, the call trace is `once_unop_a_dijkstar::run` -> `once_unop_a_dijkstar::parse_reader_file` -> `once_unop_a_dijkstar::get_target_traversal_cost`.

Inside `once_unop_a_dijkstar::get_target_traversal_cost` we can see that the function epilogue is missing, so we just put `add rsp 0x28`, then `ret`.


### Location #4 0x1721E

```
mov     rsi, [rsp+9E8h+var_9A8]
lea     rax, _ZN3std4sync5mutex14Mutex$LT$T$GT$4lock17h0afdb555768577f0E ; std::sync::mutex::Mutex$LT$T$GT$::lock::h0afdb555768577f0
lea     rdi, [rsp+9E8h+var_1B8] ; retstr
call    rax ; std::sync::mutex::Mutex$LT$T$GT$::lock::h0afdb555768577f0 ; std::sync::mutex::Mutex$LT$T$GT$::lock::h0afdb555768577f0
jmp     short $+2
lea     rsi, off_CD6F0
lea     rax, _ZN4core6result19Result$LT$T$C$E$GT$6unwrap17h86e77abf136d50a9E ; core::result::Result$LT$T$C$E$GT$::unwrap::h86e77abf136d50a9
lea     rdi, [rsp+9E8h+var_1B8]
nop
nop
nop
nop
nop
nop
mov     [rsp+9E8h+var_9B0], rax
jmp     short $+2
```

We set rax to some function pointer, so the next step should be `call rax`, but `call rax` is only 4 bytes long, there are still 2 bytes missing.

This is the most tricky point in this challenge, the argument `var_1B8` is the result object of the previous call `std::sync::mutex::Mutex$LT$T$GT$::lock`, which, if we look at the [Rust documentation for `Mutex<T>::lock`](https://doc.rust-lang.org/std/sync/struct.Mutex.html#method.lock), is a `LockResult<MutexGuard<'_, T>>`. For `Result<T, E>` type in Rust, we know that Rust uses a 1 byte flag to indicate whether this `Result` is `T(Successful)` or `E(Error)`.

An object bigger than 8 bytes but smaller than 16 bytes can be returned in rax and rdx. For our case, the actual object is in rax, and the flag byte is in dl. This way of returning a `Result` object can also be seen at 0x17F5B and 0x1836B.

We place a `mov [rsp+0x37], dl` after `call rax` to make things work.

### Location #5 0x172FE

This one requires the most imagination:

```
nop
nop
nop
nop
nop
nop
nop
lea     rdi, [rsp+9E8h+var_1A0]
lea     rsi, [rsp+9E8h+var_1F8]
call    rax
```

We don't know what function to call, so I tried putting a breakpoint to see what arguments are passed to it. We see our source and destination node in rsi and rdx. And we know all node distances are in our hashmap, and that it should return a `Option<Vec<once_unop_a_dijkstar::Node>>` for the code that follows. By looking at the list of all functions in this binray, I found a group of `pathfinding::directed::*` functions which seem to be the implementation of Dijkstra algorithm.

I tried to call the top level function, `pathfinding::directed::dijkstra::dijkstra`, luckily, it worked. So for this place, we need a `lea rax, [0x23D40]`

## Extracting the result

Unfortunately, there is still a big hole at 0x173CF. But we have already got the result in a vector, the code left is just printing them out. So the easiest way is to extract the result from the memory. I put a breakpoint at 0x17382, right after a `unwrap` which gives us the `Vec<once_unop_a_dijkstar::Node>`. We can see that a 6-element vector is in rdi after `call rax`:

```
pwndbg> x/4xg 0x7fffffffdbf0
0x7fffffffdbf0: 0x00005555557248c0      0x0000000000000006
0x7fffffffdc00: 0x0000000000000006      0x4132bf010a248c96
pwndbg> x/40xg 0x00005555557248c0
0x5555557248c0: 0x000055555571f980      0x0000000000000010
0x5555557248d0: 0x0000000000000010      0x00005555556f5cd0
0x5555557248e0: 0x0000000000000019      0x0000000000000019
0x5555557248f0: 0x0000555555772300      0x000000000000000d
0x555555724900: 0x000000000000000d      0x000055555574dd60
0x555555724910: 0x0000000000000030      0x0000000000000030
0x555555724920: 0x000055555573c760      0x000000000000000d
0x555555724930: 0x000000000000000d      0x000055555576d0c0
0x555555724940: 0x0000000000000031      0x0000000000000031
0x555555724950: 0x000055555574f3a0      0x000000000000000d
0x555555724960: 0x000000000000000d      0x000055555576bd00
0x555555724970: 0x0000000000000023      0x0000000000000023
0x555555724980: 0x000055555574d100      0x000000000000000e
0x555555724990: 0x000000000000000e      0x0000555555748610
0x5555557249a0: 0x0000000000000001      0x0000000000000001
0x5555557249b0: 0x000055555574d140      0x0000000000000008
0x5555557249c0: 0x0000000000000008      0x0000000000000008
0x5555557249d0: 0x0000000000000000      0x0000000000000000
0x5555557249e0: 0x000000000000000d      0x00000000000004f1
0x5555557249f0: 0x00007ffff7f69000      0x00007ffff7f69000
pwndbg> x/s 0x000055555571f980
0x55555571f980: "ShippyMcShipFace\016"
pwndbg> x/s 0x0000555555772300
0x555555772300: "Starlunk-63-6"
pwndbg> x/s 0x000055555573c760
0x55555573c760: "Starlunk-58-7\177"
pwndbg> x/s 0x000055555574f3a0
0x55555574f3a0: "Starlunk-53-8\177"
pwndbg> x/s 0x000055555574d100
0x55555574d100: "Starlunk-24-15"
pwndbg> x/s 0x000055555574d140
0x55555574d140: "Honolulu\340\213\366\367\377\177"
```
