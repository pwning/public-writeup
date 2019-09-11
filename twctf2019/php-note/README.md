# PHP Note
### Category: Web

PHP Note consists of a single site, `http://phpnote.chal.ctf.westerns.tokyo`, which allows the user to log in and store notes.  The server also conveniently provides source at `http://phpnote.chal.ctf.westerns.tokyo/?action=source` (as shown in a comment on the page).

Pretty early on, we decided to check the headers on one of the responses to see if we could get any useful information about what was powering the server.  (Though it was clear from the source that it was PHP, knowing which version might be important.)  This gave us the following headers, among others:

```
Server: Microsoft-IIS/10.0
X-Powered-By: PHP/7.3.9
```

IIS is an interesting choice of server; quite nonstandard as far as CTF setups go.  We decided that this was probably important and decided to do some research, and eventually came across [this slideshow](https://westerns.tokyo/wctf2019-gtf/wctf2019-gtf-slides.pdf) explaining the intended solution to the problem "Gyotaku the Flag" from WCTF 2019; namely, to use Windows Defender as an oracle for determining the contents of a file by making it conditionally think that the file contains malware.  Given that PHP sessions are, by default, stored as files, this seemed like a reasonable way forward.

After understanding the attack from Gyotaku the Flag, all we had to do is adapt [the solver](https://github.com/icchy/wctf2019-gtf) to leak data in this problem.  In particular, our goal was to leak `$_SESSION["secret"]`, which is set in this bit of code:

```
// ...

if ($action === 'login') {
    if ($method === 'POST') {
        $nickname = (string)$_POST['nickname'];
        $realname = (string)$_POST['realname'];

        if (empty($realname) || strlen($realname) < 8) {
            die('invalid name');
        }

        $_SESSION['realname'] = $realname;
        if (!empty($nickname)) {
            $_SESSION['nickname'] = $nickname;
        }
        $_SESSION['secret'] = gen_secret($nickname);
    }
    redirect('index');
}

// ...
```

Ultimately, for the attack to work, we need to wrap the contents of `$_SESSION["secret"]` within the session file in an HTML tag so that we can read it from the JS that Windows Defender is going to check for malware.  Therefore, we need to have some field we control both before and after the secret.  (There are no other assignments to `$_SESSION` anywhere else in the file.)

After a bit of local testing, we found that PHP seems to serialize objects (including `$_SESSION`) with the keys in the same order in which they were set.  We also noted from the code above that the nickname is only saved to the session when it is nonempty.  Therefore, we can simply log in twice without logging out in between; the first time we provide `realname` but no `nickname` (which results in setting `realname` and `secret` but skipping `nickname`), and the second time we provide both `realname` and `nickname` (which appends `nickname` to our sesssion, resulting in the order `realname, secret, nickname`).

Now all we have to do is to run the binary search much like in the Gyotaku the Flag solution to leak the whole secret.  You can find our script to do this step (including some 1337 h4x0r shenanigans we decided to add after the fact) in `getsecret.js`.  (Below, it's running for the nickname `</body>zach`.)

![The solve script.](https://i.imgur.com/rSY0s8g.gif)

Once we have the secret, we can simply run our own PHP server locally to create a new note with `isadmin` set to `true`, and then sign it with the secret we leaked.  We can then finally send it back to the server and invoke the `getflag` method to get the flag, `TWCTF{h0pefully_I_haven't_made_a_m1stake_again}`.