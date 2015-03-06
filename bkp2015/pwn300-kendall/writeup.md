## Kendall - Pwning 300 Problem - Writeup by Robert Xiao (@nneonneo)

Kendall was "interesting". There were some red herrings that set us on the wrong path for quite some time.

Taking apart the binary, a few things stand out. First, there's a fairly obvious exploit that allows you to become an authenticated user, by abusing an off-by-one error in the input-reading function to overwrite the byte after the input buffer with a zero (which just so happens to be the "unauthenticated" bit). Specifically, by using the "filter" function, which accepts up to 128 bytes of input, and giving it 128 As, the input-reading function will null-terminate the 128 bytes and write the desired zero. After that we're authenticated.

Next, we see that authenticated users can renew leases. Renewing a lease calls an external program with `system` with user-controllable arguments (specifically, the start and end IP addresses of the DHCP range, the subnet mask, and the nameserver), so at first blush this looks like a command injection vulnerability. However, as it turns out, all the arguments must be strings consisting of dots or digits, which is too small of a character set to allow command injection. At this point we got pretty stuck - there's no obvious vulnerability that lets us get e.g. code exec, nor anything that lets us read the contents of `password.txt` (which we thought might contain the flag).

We noticed that the lease renewal program errors out if the nameserver is invalid. On a whim, I decided to point the nameserver to my IP address, and had Wireshark running to see what happened. To our surprise the remote server made a DNS query - this is what we were supposed to do. It makes two queries: one to `yandex.ru`, and one a little while later to `my.bank`.

Using the Python `dnslib` library, it was very trivial to start up an intercepting daemon which replaced the target's queries with our own:

    sudo python -m dnslib.intercept -i 'yandex.ru. 300 IN A <IP>' -i 'my.bank. 300 IN A <IP>'

Setting up webservers on port 80 and 443 reveal that the server tries to connect to `yandex.ru` over HTTP, and if that request succeeds, it later connects to `my.bank` over HTTPS. We couldn't convince it to accept a self-signed certificate, but looking at the headers on the request `yandex.ru` showed the User-Agent as being "Lenovo".

So clearly, we were supposed to take advantage of Lenovo's recent Superfish debacle to forge a trusted certificate! Some quick trips through `openssl` later, we had constructed a newly-minted, perfectly trustworthy certificate for `my.bank`, signed by Superfish. With an HTTPS server pointed to the new certs, we finally got our gullible victim to connect and send us the flag.
