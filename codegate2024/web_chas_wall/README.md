# Cha's Wall&emsp;<sub><sup>Web, 250 points</sup></sub>

_Writeup by [@bluepichu](https://github.com/bluepichu)_

This problem hosts a simple file upload service in PHP, protected by a WAF in Go.  The first hurdle is to get a useful PHP file uploaded to the service; this is not straightforward because the WAF

- Parses the body of all POST requests as `multipart/form-data`, and rejects any that fail to parse.
- For each part of the form data, removes all characters not matching `/[a-zA-Z0-9\.]/` from the filename, and rejects any that end in any of a long list of extensions, including `.php`.
- For each part of the form data, checks if the form body contains the string `<?php`, and rejects any that do.
- Rejects requests with headers containing `charset` or `encod` when transformed to lowercase.

Since the backend server is in PHP, the approach that came to mind to get past the filename checks was to find a parser differential of some kind between Go's multipart parser and PHP's.  The one I eventually came up with was that there are multiple ways to specify a filename in a `multipart/form-data` request:

```
--BOUNDARY
Content-Disposition: form-data; name="file"; filename=foo.php; filename*=UTF-8''foo
Content-Type: text/plain

whatever-data-here
--BOUNDARY--
```

As it turns out, Go's parser will favor the `filename*` parameter, while PHP's will favor `filename`.  As a result, Go will see the filename as `foo`, while PHP will see it as `foo.php`, allowing us to upload a file that will get executed as PHP.

The file content check is straightforward to bypass as it does not check for case, so the PHP file we upload can simply have the tag `<?PHP` instead of `<?php`.

This gets us completely past the WAF, but the issue is that the backend server will only `include` the file we upload under specific circumstances:

```
<?php
    require_once("./config.php");
    session_start();

    if (!isset($_SESSION['dir'])) {
        $_SESSION['dir'] = random_bytes(4);
    }

    $SANDBOX = getcwd() . "/uploads/" . md5("supers@f3salt!!!!@#$" . $_SESSION['dir']);
    if (!file_exists($SANDBOX)) {
        mkdir($SANDBOX);
    }

    echo "Here is your current directory : " . $SANDBOX . "<br>";

    if (is_uploaded_file($_FILES['file']['tmp_name'])) {
        $filename = basename($_FILES['file']['name']);
        if (move_uploaded_file( $_FILES['file']['tmp_name'], "$SANDBOX/" . $filename)) {
            echo "<script>alert('File upload success!');</script>";
        }
    }
    if (isset($_GET['path'])) {
        if (file_exists($_GET['path'])) {
            echo "file exists<br><code>";
            if ($_SESSION['admin'] == 1 && $_GET['passcode'] === SECRET_CODE) {
                include($_GET['path']);
            }
            echo "</code>";
        } else {
            echo "file doesn't exist";
        }
    }
    if (isset($filename)) {
        unlink("$SANDBOX/" . $filename);
    }
?>
```

There isn't any way (that I know of) to set `$_SESSION['admin']` to 1 or to obtain the `SECRET_CODE` in the `config.php` file, so we can't just include the file we uploaded.  However, the file is uploaded to a subdirectory of `/var/www/html`, so if we know its path, we can just access it directly.  However, due to the `unlink` at the end, the timing window for this is very tight.  My initial testing suggested that this would be on the order of microseconds, which is likely not a long enough time to access the file.  However, the `file_exists` check happens before checking the `$_SESSION['admin']` and `SECRET_CODE`, so if we can make the `file_exists` call slow enough, that can give us more time to access the file.

I played around with it for a while and found that repeatedly traversing directories (e.g. `/././././.`) caused it to slow down more than just having a long filename.  In the end, I was able to get it to usually spend somewhere from a few tenths of a millisecond to a few milliseconds in the `file_exists` call by making a maximum-length chain of `/.` followed by a random filename, which is long enough to win the race.

My final exploit consisted of two parts:

- `solve.py` sends a specially-crafted request to the server to uplod the PHP file.
- `spam.js` sends a request for the expected location of that file once every millisecond.

I ran `spam.js` in the backround and manually ran `solve.py` a few times until `spam.js` printed out the flag.
