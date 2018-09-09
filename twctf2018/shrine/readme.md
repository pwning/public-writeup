## shrine - Web - Writeup by Artemis Tosini

### Description

We are presented with a simple flask application which renders any content we give it. However, the flask application deletes the config and self objects, and bans any use of '(' or ')' in our template. Our goal is to get app.config['FLAG'].

### Solution
Flask passes in functions and variables to the jinja template. This includes the config object, but also functions like url\_for. These functions are not deleted, and support getting \_\_globals\_\_ as an item. Therefore, we can just render the template:

    {{url_for.__globals__.current_app.config.FLAG}}

Because of URL encoding, this means going to

    http://shrine.chal.ctf.westerns.tokyo/shrine/%7B%7Burl_for.__globals__.current_app.config.FLAG%7D%7D

That gives us the flag.

    TWCTF{pray_f0r_sacred_jinja2}
