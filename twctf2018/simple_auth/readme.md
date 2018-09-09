## Simple Auth - Web

### Description

    http://simpleauth.chal.ctf.westerns.tokyo/

Warmup web challenge. Provide a password that matches the hash to win.

### Solution

`parse_str` is called directly on the query, which lets us set whatever variables we like in the php program. So just set the `hashed_password` variable to be equal to the hash and we are done.

    http://simpleauth.chal.ctf.westerns.tokyo/?action=auth&hashed_password=c019f6e5cd8aa0bbbcc6e994a54c757e

    TWCTF{d0_n0t_use_parse_str_without_result_param}
