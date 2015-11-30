## Nick Les' Dimes - Web 200 Problem

### Description

This challenge is a website running a stripped-down and modified version of ["Mellivora"](https://github.com/Nakiami/mellivora), which not coincidentally also powers 9447CTF. We're instructed to gain access to the admin account.

### Solution

Most functionality of Mellivora has been gutted. While poking around what was left, we made a couple of observations about the password reset system:

1. It still works in the CTF challenge version of Mellivora.
2. You can reset a user's password given their email, site UID, and the generated reset token that is emailed to that address.
3. The password reset token used by the CTF challenge looks like a MD5 hash, which is at odds with the real Mellivora's use of SHA256.

Guessing that this reset token system was modified to be something insecure, we found that any password reset token is just the MD5 hash of the corresponding user's name. (The real Mellivora uses a SHA256 hash of random data). This means that we can trigger a password reset for a user knowing only their username, email address, and UID---and without access to the email account.

The site reveals the admin user as username=admin, email=blackhole@9447.plumbing, and UID=1 on the json version of the scoreboard. We can initiate a password reset of the admin account by requesting a reset for blackhole@9447.plumbing, and then navigating to `http://nicklesndimes-wq3mhu8l.9447.plumbing/reset_password?action=choose_password&auth_key=<md5("admin")>&id=1`. This allows us to change the admin's password to one of our choice.

However, attempting to log in as the admin fails with an error about an IP whitelist. We can't spoof the source IP address of a TCP connection; but we can totally spoof a `X-Forwarded-For` HTTP header, which makes sense to try since the CTF challenge is behind CloudFlare. (Crash course: CloudFlare is a service that sits between a webapp and its clients, and the `X-Forwarded-For` header is one way for proxies like CloudFlare to inform a webapp about the originating client IP address. It works kinda like email received-from headers, especially in that you can't trust all of them). As it turns out, setting `X-Forwarded-For:<ip addr of nicklesndimes-wq3mhu8l.9447.plumbing>` does the trick; using a Chrome plugin to set that header, and having already reset the admin password, we can log in as the admin account and retrive the flag.
