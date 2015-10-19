# matrix X matrix (pwn 175)

## Description

```
Matrix is magic!!!
nc 52.68.53.28 31337

matrix-a0e5c5c0a8f05896a7f03d8ed4588027
libc-3f6aaa980b58f7c7590dee12d731e099.so.6
```

## The bugs

In main, the program gets the size of the matrix from user. This value, however, can be negative.

```C
  ...
  printf("Hello %s \nThat is a program of matrix multiplication\n", name_buf);
  fflush(stdout);
  puts("Enter the size of matrix");
  fflush(stdout);
  __isoc99_scanf((__int64)"%d", (__int64)&v38);
  v43 = v38 - 1LL;
  v35 = 0LL;
  v34 = 8LL * v38;
  v44 = v38 - 1LL;
  v32 = v38;
  v33 = 0LL;
  v30 = v38;
  v31 = 0LL;
  v3 = alloca(16 * ((8 * v38 * (signed __int64)v38 + 22) / 16uLL));
  v45 = 8 * (((unsigned __int64)&v9 + 7) >> 3);
  v42 = abs(v38);
  for ( i = 0; i < v42; ++i )
  {
    for ( j = 0; j < v42; ++j )
    {
      printf("Enter the (%d,%d) element of the first matrix : ", i, j);
      fflush(stdout);
      __isoc99_scanf((__int64)"%lld", 8 * (j + ((unsigned __int64)v34 >> 3) * i) + v45);
    }
  }
  ...
```

In above code, we can see that `v34` is computed with possibly negative `v38`, which yields a memory corruption in `scanf`'s frame. Specifically, when `8 * (j + ((unsigned __int64)v34 >> 3) * i)` is -8, we overwrite the return address of `scanf`.

## Exploit

We use the bug twice:

1. Leak out the address of `puts` which lets us to calculate the libc base address, then return back to main.
2. Use libc base address to calculate address of `system`, and return to it. We store our command in the name buffer.

When exploiting the bug, we can send a hyphen (-) to prevent `scanf` from writing any value, thus preserving the original stack contents until we get to the return address.

See
[exploit.py](https://github.com/pwning/public-writeup/blob/master/hitcon2015/pwn175-matrix/exploit.py)
for the full exploit.

## Flag

Flag: `hitcon{tH4nK_U_4_pL4y1nG_W17H_3Bp_M47R1X}`
