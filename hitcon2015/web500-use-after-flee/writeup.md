# Use-After-FLEE (pwn, web 500)

Use-After-FLEE was a web challenge allowing you to upload and run
arbitrary PHP scripts.

## Poking around

Uploading a script that does `phpinfo()`, we see that the PHP script is
running with and `open_basedir` of `/var/www/html/:/tmp/` as well as the
following functinos in `disable_functions`:

```
exec, passthru, shell_exec, system, proc_open, popen, curl_exec,
curl_multi_exec, parse_ini_file, symlink, chgrp, chmod, chown, dl, mail,
imap_mail, apache_child_terminate, posix_kill, proc_terminate,
proc_get_status, syslog, openlog, ini_alter, ini_set, ini_restore,
putenv, apache_setenv, pcntl_alarm, pcntl_fork, pcntl_waitpid,
pcntl_wait,  pcntl_wtermsig, pcntl_wstopsig, pcntl_signal,
pcntl_signal_dispatch, pcntl_sigtimedwait, pcntl_sigprocmask,
pcntl_sigwaitinfo, pcntl_exec, pcntl_setpriority, link, readlink
```

This list looks pretty reasonable, so based on the title of the problem,
we searched for publicly known use-after-free bugs in the running
version of PHP (`5.5.9-1ubuntu4.12`). It turned out the server is
vulnerable to
[CVE-2015-6834](https://github.com/80vul/phpcodz/blob/master/research/pch-034.md).

Luckily, the service is using standard Ubuntu packages, so we can develop on an
environment with the exact same php/libc versions.

## The bug

As described in Taoguang's writeup, the bug is a use-after-free in
unserializing `SplDoublyLinkedList` objects. PHP's object serialization
allows a value to reference a previously unserialized object (see
[here](http://www.phpinternalsbook.com/classes_objects/serialization.html)
for some more details).  When an deserialized object's `__wakeup` method
is called, it can free one of its member objects by reassigning the
member. With this bug, when the member is a `SplDoublyLinkedList`, the
object is freed, but references to its elements are still accessible
from the deserialized object. Taoguang's PoC does this, then overlaps a
string with the freed object so that fake PHP objects (zvals) can be
constructed.

Here's an approximate descripton of what is going on in his PoC:

```php
class obj {
  var $ryat;
  function __wakeup() {
    $this->ryat = 1;
  }
}

$inner = 'i:1234;:i:1;';
$exploit = 'a:5:{';
$exploit .= 'i:0;i:1;';

# SplDoublyLinkedList object
$exploit .= 'i:1;C:19:"SplDoublyLinkedList":'.strlen($inner).':{'.$inner.'}';

# obj that references the SplDoublyLinkedList. When __wakeup is called,
# the SplDoublyLinkedList is freed.
$exploit .= 'i:2;O:3:"obj":1:{s:4:"ryat";R:3;}';

# references element in SplDoublyLinkedList
$exploit .= 'i:3;a:1:{i:0;R:5;}';

# overlaps the freed element
$exploit .= 'i:4;s:'.strlen($fakezval).':"'.$fakezval.'";';

$exploit .= '}';
```

## Exploitation

The techniques for exploiting this are mostly taken from [Stefan Esser's SyScan 2012 talk](http://www.slideshare.net/i0n1c/syscan-singapore-2010-returning-into-the-phpinterpreter).

At this point, we can construct arbitrary `zval`s. In PHP 5.5.9, the relevant structures are:

```c
struct _zval_struct {
  zvalue_value value;
  zend_uint refcount__gc;
  zend_uchar type;
  zend_uchar is_ref__gc;
};

// zval types
#define IS_LONG   1
#define IS_OBJECT 5
#define IS_STRING 6

typedef union _zvalue_value {
  long lval; // type = IS_LONG
  ...
  struct {
    char *val;
    int len;
  } str; // type = IS_STRING
  ...
  zend_object_value obj; // type = IS_OBJECT
} zvalue_value;

typedef struct _zend_object_value {
  zend_object_handle handle;
  const zend_object_handlers *handlers; // a table of function pointers
} zend_object_value;
```

Since we can construct arbitrary `zval`s (`_zval_struct`), the plan will
be to leak addresses, then construct a `zval` of type `IS_OBJECT` whose
handler function table points to memory that we control.

### Leaking addresses

We can already read arbitrary memory by making a string with any `val`
and `len` of our choosing. Unfortunately, the apache2 process is PIE, so
there are no known addresses to leak from. Stefan's slides give a nice
solution to this: We can construct a long, then free it using the same
`__wakeup` trick. PHP's memory cache will then write a heap address over
`lval`, leaving the `type` field intact. We can then read the long to
get a heap address.

Now that we have a heap address, we scan through it for `libphp5` addresses
using the method suggested in the slides. We spray a bunch of objects with, and
scan the heap looking for a pattern that looks like a `handlers` address
followed by a refcount of 1 and a type of `IS_OBJECT`. The `handlers` for the
object should live in `libphp5`'s data, and from there, we can compute
`libphp5`'s base address. We can then learn `libc` addresses using GOT entries
in `libphp5`.

### Getting a shell

Now that we have the address of `system`, we spray `system` on the heap,
and scan through to find the location of one of them, `system_addr`.
We'll use `system_addr - 8` as the `handlers` table for our fake object
so that `system(fake_zval)` will be executed when `del_ref` is called on
the object.  This gives 8 bytes (the `handle` field) to place a shell
command. Luckily, we are given write access to `/tmp`, so we can write a
command in `/tmp/a` and run it with exactly 8 bytes: `sh /*/a;`.

See
[exploit.php](https://github.com/pwning/public-writeup/blob/master/hitcon2015/web500-use-after-flee/exploit.php)
for the full exploit.

## Flag

Flag: `hitcon{beapentester,itisnecessarytolearnmemory-basedattack}`
