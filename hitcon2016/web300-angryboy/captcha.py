from pwn import *
import string
import requests

# secret key
ss = ['\x84','\xcb',')','\xd7',
'4','\xf8','\x9f','\x1a',
'\x14',';','\x08','\xb1',
'w','\xfc','\x2b','\x1c']

for ii in range(16):
    if 0 <= ii <= 3:
        pref = '333'
    elif 4 <= ii <= 7:
        pref = '4444'
    elif 8 <= ii <= 12:
        pref = '55555'
    else:
        pref = '666666'
    for i in range(256):
        i = chr(i)
        s = requests.Session()
        r = s.get('http://52.196.144.8:8080/')
        prefix = r.text.split(' md5( "')[1].split('"')[0]
        x = iters.mbruteforce(lambda x: md5sumhex(prefix+x).startswith(pref), string.ascii_letters + string.digits, length = 10)
        r = s.post('http://52.196.144.8:8080/',data={'guess':ss[ii],'captcha':x,'line':str(ii)})
        if 'bad luck' in r.text:
            continue
        print(ss[ii],i,r.text)
        break

encryptedflag = '51a885f4cabb818529cd515acdf77be3b20e8e1df9d8a12658d584c0635cc31ec24acc418c05e8720fa6073706b61439'
