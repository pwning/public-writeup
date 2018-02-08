## Useless - Misc Challenge

We were given a URL that didn't seem to do anything other than just a login. We checked the common directories that are mistakenly pushed, such as `.git`. Once we found that there was a `.git` directory, we used the tool named `GitTools` to download and extract the contents of the repository.

```markdown
## algorithm for session cookie  

### Basic
- general user >> username + user IP  
- **admin**        >> admin + 127.0.0.1

### example
- username : `codegate`, IP : `211.224.255.84`
- `codegate211.224.255.84` >> (encrypt) >> setting cookie
```

There was a readme file that explains how the session cookie is made, along with the `enc.py` that generated the encrypted contents. When we encrypted `admin127.0.0.1` string and set the cookie, we were able to retrieve the flag page.

```
7e787c68293431367f6d63236f36694a
```

We, then, were told to encrypt the following string and the result was the flag.

```
It's_reaLLy_n0nsen5_th4t_I_5p3nt_M0ney_more_7h4n_My_6udg3t.
=> 1678766808377c204d4a062d550c536f3d783868306d262550154b6129702f485378396821494c52171e695d4f16493c79783f681f4e1c411b045e0b227b2443
```

