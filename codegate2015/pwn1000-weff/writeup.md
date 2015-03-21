# Weff - Pwn 1000 problem

## Overview

Weff was a caching HTTP proxy server. It supports two protocols,
`http://` and `file://` (limited only to files in
`/home/weff_webserver/webserver`). Responses are cached in a binary
tree. Cache entries are keyed by a hash of the request URI and contain
the response, as well as the creation time of the cache entry. When a
cache entry is looked up, if its age is greater than 30 seconds, the
cache entry is deleted and a cache miss happens.

The server is a fork/accept service, so addresses did not change across
connections. It also supported up to 1024 HTTP requests per connection,
which was useful for triggering the vulnerability multiple times.

We were given a 32-bit Linux binary (with PIE, NX, and full RELRO) as
well as a copy of the libc from the system.

## Vulnerabilities

There were a couple of bugs in this program. First, the cache entries
are looked up only by the hash of the URI, which are easy to collide -
the full URI is not checked. More interestingly, there is a
use-after-free in the cache expiry code. The code for deleting a cache
entry look like:

```c
typedef struct cache_entry {
  unsigned int hash;
  char *response;
  time_t creation_time;
  size_t response_len;
  struct cache_entry *left;
  struct cache_entry *right;
} cache_entry;

...

cache_entry *cache_delete(cache_entry *root, unsigned int hash) {
  if (!root) return NULL;

  if (root->hash > hash) {
    root->left = cache_delete(root->left, hash);
    return root;
  }

  if (root->hash < hash) {
    root->right = cache_delete(root->right, hash);
    return root;
  }

  cache_entry *new_root = root->right;
  if (root->right) {
    if (root->left) {
      cache_entry *left_most = get_left_most(root->right);
      root->hash = left_most->hash;
      free(root->response);
      root->response = left_most->response;
      root->response_len = left_most->response_len;
      root->time = left_most->response_len;
      root->right = cache_delete(root->right, left_most->hash);
      return root;
    }
  } else {
    new_root = root->left;
  }

  free(root->response);
  memset(root, 0, sizeof(*root));
  free(root);
  return new_root;
}
```

The function takes the root of a binary tree and potentially returns a new root
(when cache entry being deleted is at the root of the tree). The correct way to
call this code looks something like:

```c
cache_root = cache_delete(cache_root, hash);
```

But the program fails to assign assign the return value of `cache_delete` back
to `cache_root`. Thus, when the cache entry at the root of the binary
tree expires and is looked up, `cache_root` would point to freed memory.

## Exploitation

The HTTP request is parsed into a `request` struct, which contains a lot
of strings in the heap. After triggering the free as described above, we
can a controlled string allocated at `cache_root` by sending a request
with a 24 byte header. Unfortunately, there were no opportunities to
place controlled data with null bytes on the heap, so we were limited to
strings for our fake `cache_entry`.

### Leaking addresses

The bug gives a pretty easy arbitrary read. To read `ptr`, we can make
`cache_root` point to a fake `cache_entry` so that
`cache_root->hash = request_uri_hash`, `cache_root->response = ptr`, and
`cache_root->response_len = len_to_read`.
Even better, since the program never directly derefrences `response` and
instead just passes it to the read syscall, we do not need to worry
about `ptr` or `len_to_read` being valid.

Using this, we can brute force the binary base address by looking for a
page with a known string a a specific offset. Since the binary is
32-bit, this only takes a couple hundred guesses. By using an invalid
protocol, the code which updates the cache is short-circuited, so none
of the invalid pointers in the fake `cache_entry` get dereferenced.

Using the same technique, we can leak the libc base.

### Getting a shell

Now that we have some interesting addresses, we need to figure out a way
to use this bug to write something interesting to get code execution.
Unfortunately, without doing pretty advanced heap feng shui, the ability
to control `cache_root` (with no null bytes) gives us pretty limited
capabilities.

The two main primitives we use are:

1. We can forge the left/right pointers in `cache_root` and use this to
   write a new `cache_entry` into for example,
   `cache_root->right->right`. This is useful because we control the
   first 4 bytes of the new `cache_entry` (the URI hash).  However, this
   write will only happen if `cache_root->right->right` is 0 to begin
   with.
2. In `cache_delete`, when deleting a `cache_entry` with both a left and
   right subtree, fields of the `cache_entry` are overwritten with
   values from the leftmost child of the right subtree.

Given these, we chose to overwrite `free_hook` (which is called on every
`free`) with `system`. Initially, `(cache_entry *) free_hook` has a 0 for all
fields.

We cannot achive this with the first primitive alone, since it only ever writes
heap pointers, which won't be executable. Thus, we want to set things up so
that we can use the second primitive. To do this, we need `free_hook` to be a
node in the tree with both right and left subtrees.  In addition, the leftmost
child of the right subtree should have a tag of `system`, so that `system` will
be written to `free_hook`.

Here is the tree structure that we want to create (the hashes are in parentheses):

```
         root
          /
     free_hook (0)
      /         \
 whatever     (system)

```

Since the `free_hook` node's `left` and `right` pointers are 0, we can use the
first primitive to set these to the two children.

To link `free_hook` into the tree, we can use our control of the `cache_root`
node. On the same request, we force the URI hash to 0. Since the `free_hook`
node's hash is 0 (and so is its `creation_time`), the node will be deleted,
which writes `system` over `free_hook`. All that remains is to place a shell
command into a header, and it will be "freed" (executed) when the request is
destroyed.

```
proxy_stuff_hm
```
