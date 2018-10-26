# Oh My Raddit

## Description

This is based on a real world case. If you get the crypto point, it can be sovled in 10 minutes!

[13.115.255.46](http://13.115.255.46/)

## Solution

All of the links on the page are of the form

```
<a href="?s=8c762b8f22036dbbdda56facf732ffa71c3a372e4530241246449a55e25888cf98164f49a25f54a84ea0640e3adaf107cc67c8f2e688e8adf18895d89bfae58e33ae2e67609b509afb0e52f2f8b2145e">50 million Facebook accounts owned</a>
```

where the `s` parameter is different hex strings.  By inspecting many of the links on the page, we find that the length is always divisible by 16 characters.  If we try modifying a single character of the paramter, we tend to get the default response (serve `/`) if we edit any of the last 16 characters or so, and error responses if we modify earlier characters.  This indicates that the parameter is probably encrypted and ends with padding bytes that we are breaking.  If we try deleting a prefix of the parameter, then we get the default response if we delete anything other than a multiple of 16 characters.  This indicates that we're probably dealing with a block cipher with a block size of 64 bits.

Looking for patterns in the `s` parameter, we note that there is one suffix of 16 characters that is much more common than any other; specifically, `3ca92540eb2d0a42` appears as a suffix for 18 of the 105 links on the page.  This is consistent with a PKCS#7-style padding scheme with the cipher running in ECB mode, since then the encrypted form of the block `08 08 08 08 08 08 08 08` should appear about an eighth of the time in a large collection of strings.

We guessed that the server was using DES and used hashcat to crack the key since the key space is small (as the hint tells us that it can only be things that Python considers lower-case).  Two members of the team did this, and got two different keys: `ldgonaro` and `` ldfnn`rn ``.  This is because the lowest bit is ignored, which gives us 256 possible keys.

When we got to this point, the server had been down for multiple hours with no sign of coming back soon, so one of our team members just submitted all 256 possibilities until we ended up with the correct flag, `megnnaro`.

If the server had been up, we could instead inspect `s` using one of our recovered keys (since they can be used to correctly encrypt and decrypt `s`).  We find three different forms for `s`:

1. `m=r&u=some-uid-here&t=some-title-here` (for the links to outside pages)
2. `m=p&l=10` (for listing the top n results)
3. `m=d&f=path-to-file` (for file downloads)

Using the third option, we can give a path to any file we want, so we can locate and download the server's python file.  By requesting `/proc/self/cmdline`, we get back `python\x00app.py\x00`; and by requesting `app.py`, we get:

```
# coding: UTF-8
import os
import web
import urllib
import urlparse
from Crypto.Cipher import DES

web.config.debug = False
ENCRPYTION_KEY = 'megnnaro'


urls = (
    '/', 'index'
)
app = web.application(urls, globals())
db = web.database(dbn='sqlite', db='db.db')


def encrypt(s):
    length = DES.block_size - (len(s) % DES.block_size)
    s = s + chr(length)*length

    cipher = DES.new(ENCRPYTION_KEY, DES.MODE_ECB)
    return cipher.encrypt(s).encode('hex')

def decrypt(s):
    try:
        data = s.decode('hex')
        cipher = DES.new(ENCRPYTION_KEY, DES.MODE_ECB)

        data = cipher.decrypt(data)
        data = data[:-ord(data[-1])]
        return dict(urlparse.parse_qsl(data))
    except Exception as e:
        print e.message
        return {}

def get_posts(limit=None):
    records = []
    for i in db.select('posts', limit=limit, order='ups desc'):
        tmp = {
            'm': 'r',
            't': i.title.encode('utf-8', 'ignore'),
            'u': i.id,
        }
        tmp['param'] = encrypt(urllib.urlencode(tmp))
        tmp['ups'] = i.ups
        if i.file:
            tmp['file'] = encrypt(urllib.urlencode({'m': 'd', 'f': i.file}))
        else:
            tmp['file'] = ''

        records.append( tmp )
    return records

def get_urls():
    urls = []
    for i in [10, 100, 1000]:
        data = {
            'm': 'p',
            'l': i
        }
        urls.append( encrypt(urllib.urlencode(data)) )
    return urls

class index:
    def GET(self):
        s = web.input().get('s')
        if not s:
            return web.template.frender('templates/index.html')(get_posts(), get_urls())
        else:
            s = decrypt(s)
            method = s.get('m', '')
            if method and method not in list('rdp'):
                return 'param error'
            if method == 'r':
                uid = s.get('u')
                record = db.select('posts', where='id=$id', vars={'id': uid}).first()
                if record:
                    raise web.seeother(record.url)
                else:
                    return 'not found'
            elif method == 'd':
                file = s.get('f')
                if not os.path.exists(file):
                    return 'not found'
                name = os.path.basename(file)
                web.header('Content-Disposition', 'attachment; filename=%s' % name)
                web.header('Content-Type', 'application/pdf')
                with open(file, 'rb') as fp:
                    data = fp.read()
                return data
            elif method == 'p':
                limit = s.get('l')
                return web.template.frender('templates/index.html')(get_posts(limit), get_urls())
            else:
                return web.template.frender('templates/index.html')(get_posts(), get_urls())


if __name__ == "__main__":
    app.run()
```

Which indeed contains the correct encryption key, `megnnaro`.