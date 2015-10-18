# nanana (pwn, web 200)

Nanana was a web challenge with a login form submitting to a CGI script,
`/cgi/nanana`. Since this is also a pwnable, we expect that this is a
binary. Through some guessing, we find that the binary is available to
download at `/nanana`.

```
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      FILE
Partial RELRO   Canary found      NX enabled    No PIE          No RPATH   No RUNPATH   nanana
```

## The bugs

Reversing the binary, we see that it is using a CGI libary (which we could not
find the binary for). A library function is called to initialize a password in
a global buffer. The get parameters `username`, `password`, `job`, and `action`
are then copied into buffers on the stack. The copies are performed via:

```C
void get_params(char *username_buf, char *password_buf, char *job_buf, char *action_buf) {
  char *username = CGI_GET("username");
  if (username) {
    sprintf(username_buf, username);
    char *password = CGI_GET("password");
    if (password) {
      // same for job, action
    }
  }
}
```

This is both a stack buffer overflow and format string vulnerability.

Back in the main function, the password is compared against the global buffer,
and if it matches, a `do_job` function from the CGI library is called.

```C
if (strcmp(password_buf, g_password) == 0) {
  do_job(username_buf, action_buf, job_buf);
  system("cat fake-flag");
  return 0;
} else {
  puts("Auth Failed");
  return -1
}
```

## Exploitation

To exploit this, we use the format string vulnerability to overwrite the GOT
entry for `do_job` with `system` so that the program will execute a command in
`username_buf`. To get to this code path, we first need to leak the password.
We do this by using the buffer overflow to overwrite `argv[0]` with
`g_password`, so that the stack canary failure message includes the password.
The stack canary failure message looks like a valid HTTP header (`*** stack
smashing detected ***: argv0`), so we can obtain the leaked value by inspecting
that header.  Since `argv[0]` is normally a stack address, its bottom 6 bytes
are non-zero, whereas the address of `g_password` is `0x601090`. Since
`sprintf` will write exactly one null byte, we use the `username`, `password`,
and `job` fields to write zeros over the high bits of `argv[0]`, then write the
address of `g_password` using the action field.

This gives us the password: `hitconctf2015givemeshell`

Having leaked the password, we make another connection where we use the format
string vulnerability to point `do_job`'s GOT entry at `system`'s PLT entry. We
can then specify a command to run as the username and the correct password, run
arbitrary commands.

See
[exploit.py](https://github.com/pwning/public-writeup/blob/master/hitcon2015/web200-nanana/exploit.py)
for the full exploit.

## Flag

Flag: `hitcon{formatstringmusteasyforyouisntit?}`
