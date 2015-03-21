## Owltube - Web 400 problem

Not more owls! We're given a simple video linking service with a login page, and the Python source for the server.

First thing we see is that they are storing the credentials in an encrypted cookie. The cookie is encrypted with AES in CBC mode, and the cookie includes the IV. Since we know the plaintext (it's just our login username and password), we can use a chosen-IV bitflip attack. By choosing the IV such that

    IV' = IV ^ known ^ wanted

we will cause the resulting ciphertext to decrypt to `wanted` instead of `known`. So now it's a simple matter of converting our cookie

    plaintext = '{"u": "ppp", "pw": "admin"}'

to

    wanted =    '{"u": "admin","u": "admin"}'

The login system uses your cookie as a filter for the database query, so we can login simply by omitting the password entirely. Once we logon, we see the video `THIS IS THE KEY`; the flag is the Video ID: `the_owls_are_watching_again`.
