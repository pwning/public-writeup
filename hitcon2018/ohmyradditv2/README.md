# Oh My Raddit V2

This problem was an interesting one. Once the first part had been solved, we could "sign" any queries we want for the server. From what the front-end is doing, we were able to determine that the server could do a few things. The first thing it could do was redirect the user to another site. This was via the "u" command. Another thing it could do was directly serve a file of its own. This was performed via the "f" command. Finally, it could be used to fetch the top posts, limited by a certain value. This was done by "l".

This is exciting, because it means that we can fetch the source from the problem, including the main `app.py`. Since this is a python application, we can also fetch `requirements.txt`, which gives the versions of the frameworks being used. Both of those are available here. Now, glancing through this code, we immediately notice that we have what appeaars to be sql injection through the `limit` field. 

Consider the following line of code `for i in db.select('posts', limit=limit, order='ups desc')`. Now, any ORM worth their salt would sanitize this, or constrain `limit` to be an integer only. However, `web.py`'s is not a good ORM, and we can actually inject anything we want in their. Including `SELECT LOAD EXTENSION 'blah'`. 

This seems like a smoking gun, but as it turns out, there's not much we can do with it. I'll save you the gritty details, but after reading through the source for it several times, we concluded that the only way to use this was to have a valid ELF `.so` (including extension) on the filesystem directly for it to pull. Unlike windows systems, on linux we need the file local. 

With no upload primitive, and no way to commandeer another `.so` for our purposes, we were stuck. However, it turns out that perhaps this injection was not what we thought it to be.

If we look at `requirements.txt` again, we notice that `web.py` is pinned to version `0.38` (one version below latest). As it turns out, this version had a nasty bug, detailed [here](https://securityetalii.es/2014/11/08/remote-code-execution-in-web-py-framework/). The short version is, any property of the selector that uses variable substitution has a remote code execution vulnerability due to the use of an eval. Although not explicitly mentioned in the writeup, we see from `https://github.com/webpy/webpy/blob/webpy-0.38/web/db.py#L696` that limit is indeed vulnerable as well. This means that (using the helpful wrapper provided by the writeup) we can get command execution on our server. Here is the command we run

```python
${(lambda getthem=([x for x in ().__class__.__base__.__subclasses__() if x.__name__=='catch_warnings'][0]()._module.__builtins__):getthem['__import__']('os').system('<your command here>'))()}
```

As our limit statement. Although we weren't able to get a reverse shell working, we could run individual commands with this and eventually found the `print_flag` script in the root. With this, we can get the flag! 
