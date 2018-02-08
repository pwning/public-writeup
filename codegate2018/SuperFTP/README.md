## SuperFTP - Pwnable Challenge

SuperFTP implements a fake file downloading service with no real
download functionality. The supported actions are:

1. Create an account
1. Login (trivial stack buffer overflow when reading username/password)
1. Download file
1. Secret admin menu, available if you login with admin/P3ssw0rd
  1. Download file
  1. (other irrelevant items)

Unfortunately, the program has stack canaries and PIE, which need to be
bypassed before exploiting the trivial buffer overflow.

Looking at the difference between the admin/regular version, we see that they are similar

`g_url` is populated as follows:

```c++
// Non-admin version:
g_url = malloc(...);  // at program startup
std::reverse(input_url.begin(), input_url.end());
strcpy(g_url, input_url.c_str());
process_url();
string result(g_url);
std::reverse(result.begin(), result.end());
// print result

// Admin version:
char totally_random_stack_buf[1024];
g_url = &totally_random_stack_buf;
std::reverse(input_url.begin(), input_url.end());
strcpy(g_url, input_url.c_str());
process_url();
string result(g_url);
std::reverse(result.begin(), result.end());
// print result
```

The `process_url` function looks like this:

```c++
void process_url() {
  some_list<int> indices;
  for (int i = 0; i < g_url.size(); ++i) {
    if (memcmp(g_url + i, "/../", 4) == 0) {
      indices.insert(i);
    }
  }
  if (!indices.empty()) {
    int index = indices.first();
    int next_slash = index + 4;
    while (g_url[next_slash] != '/') {  // no null check
      ++next_slash;
    }
    for (int i = 1; i <= index; ++i) {
      g_url[next_slash - i] = g_url[index - i];
    }
    g_url += next_slash - index;
    process_url();
  }
}
```

The bug is that `process_url` does not terminate at the end of the
string when looking for the next slash. The stack layout of the admin
download function looks like:

```c
char url_buf[1024];
uint32_t stack_canary;
uint32_t saved_ebx;  // contains address of GOT (binary is PIE)
```

If `url_buf` doesn't contain any slashes, and byte 1 of the stack canary
is a slash (byte 0 of a canary is always 0), then after `process_url`,
`g_url` points to byte 1 of the stack canary. This conveniently leaks
back the stack canary and an address in the binary.

Testing this locally, we confirm that the stack canary and an address
from the binary is leaked back when byte 1 of the canary is a slash.

We can then use this information (`system` is conveniently referenced by
dead code in the binary) to exploit the trivial buffer overflow in
login to get a shell.

During the competition, we had to use a server in Korea to brute force
this quickly enough.
