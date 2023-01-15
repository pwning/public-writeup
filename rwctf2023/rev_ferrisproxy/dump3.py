from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_v1_5
from Crypto.Util.Padding import unpad
import os
import hashlib
from collections import defaultdict
from io import BytesIO
import struct

sentinel = os.urandom(256)

rsa0 = RSA.importKey("""-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC93GDINPM6HX2+
NN3bCznyri2rDHDVcamzA/rPDXi9Mb2hu1Ypqek4km/kf4MKDsrOU/3T5mcdx5kA
80s7mBWlGaItg/sy6dsh2XOoKVEHcZYyrbSAbkYrT9CoLLM/JlipbsalKenkW9Jl
HB0h+vwv/rAwXJ9IMSc4RQkvjn/QKuBPhcXfrfaAIKNO0L+iqUL3asFM2CF8DXZX
y8pLAxMy2PDJLtb0I/rXDWRImWlBcIWBrhg7lDA0UxWXDD1i5MmMlvxmyho1F8Br
h7ietK3XW7LWshD2ARIDgPoTZ7lZm7P9JbKSN+Uk7fay6LdkJXYszfT89Owmi7tm
fUQ41fcBAgMBAAECggEAWyGJru+Dg/Sd44t6peY4lVy3fO/GxRz+qHeTjojX2HAk
ppnGHM96q3XWkWYHHu/Ets6n+msQOcIRldwx01QHp6yrJI/CJkkLrq6yjhfu1dTW
lFK+XhsQQT/ZVq/GBdzBF+qdHLAGnV7ZmUCqVyIipGLqbPw4VC2Ltr2kUBhlDySA
A+gCnUrPyVi6O9OFcyDepKMy481gZLLijakINejYrsbdCInz2omHq12w/50tuFt1
s4XMWJN+AW0g1Hx+tTk2jDX1Wqg/htmJhjGqTj02GLJ/CJQjRodEdA7mx3HGwhis
igeZgHTdPgP1B5Z9NXwUg9Qxln72D4mGhLCGYcw8VQKBgQD6+oltv1i44BO/ROUJ
kZPTLWeoBrxP2OOli4aOSilLifeGrUQOSUtvcFHOxzy5RrhvX89f3GnklXcGyHXD
03wg0/hqL0HM1EzNLmWkJW0Ng5WRFFgfcQIKbWBK9SHhAmKzkHtZPq6NwN8MbZUF
vndxDtcSOdH0/TbMtCMYYs0MswKBgQDBqM7QxWT6qebCU4YOV+5uwnP+hAunsWkv
VW7pHgiPnZ8ARRZ9iFIqqiVRvKeeyZBEK22eOJNguz6Cqfz2451D/AHA7sXht+1D
9GCE/ebvUw+lPNQIRKkAgwQ8Dx+R6ikaUGzUKYhmWYJ5xgS9ZALZ+k4+rSjFg9jV
jFjT7xQvewKBgHo9bJI3kE77VKLkO2ndrdI9Wy9LmIyLZtVKj87d8B8Ko7TEz1Dm
AgfU/QNppvnWqB4W3DokcK8U3VRAbptidiLHG0ccnT/WZ1HIN1kroWHjpQV0kzc9
I3FQtIXNvyKItuoehPWCwiHovrqe5OZXTnWSdM47uzdH3Vj2o+FMvfJhAoGAQvus
bTGZd8oEcvqIx7VKVy0TCdmKXnpSs3iNYDxvIZ2XPXSoDst0ACXRuq/SGm4FZE7R
H4TaFP8u4+sAADVCVB16Tc1IzIXdnz+LkvRvSCAmrTSY8jMtcWvfrxZcCRBBH0Tq
H4guEZisNIp1YTySb+rP3YXvMEImYdalcsii5rkCgYEAimnWJ5aFN3TDt3h76CL3
nRQegnzekJBjXZfcrHdExkgNChWjiz+WU/FW/Z87xMxtfIEwwzzIQHxbKZhgzO/U
p2eXdqH59DvauggbiS3h4p9k2kxWTocztarvdftMW0ncmA4yCKiUQEmWD784JCyx
OupNNfr2rgViWggVBEtJUIg=
-----END PRIVATE KEY-----""")

rsa1 = RSA.importKey("""-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDbfWw2tfpbGVCl
+zLy7pVH2vDgfiVj3d+ykCZd5+MOFCFgI8z5LKkG8iBv/D1/wAaQTBSUNDF9kIKX
PvYYC5L2OuWyqD0ulIxn48kA7QENaKywkIm3LIQ1b/1VU+kksDRJJ5i5NgnzhYMB
yOxvRP75X3tNeVKKr2y9e3XosPEJAmNFe/07VRMGQOkYZmadHjEuJBP4/Hoo6oCy
slwAXQQlqOLloF8dVB2tdDCCarw8Sx+e+naJAItnaIM8uUZtFqF0V6KBddPgvpS+
OlsWv/0g28Nvb69CRGXvOUdW1QAxHhfmyZbacccfljJOLVw68wWw36g8bGAEalKp
gLGY/Ag3AgMBAAECggEADbfJC6JUA12RrM4GYSiIK/WDGITJ0XQMhxx7SWM0zax0
aY3TQb+I0OZRIK6jKVjXEC2xG5InhbGCd/F3cAlJJhqIQKJDMKYYIGYcKfKmHjBs
mpxt/wTJPo3BR5P2/lQE8I2I/gpilNXDWlk0bb/iL7PIAQ+UGRbdtPoCZIiqh+WA
qElaJ4LHXgKBXUpozfEtUa383IcwsQdB1BSwMOnJ5YFrplhx6fTgJ6noFB4eLp7h
SCSR2018r11UAANqWbc7a40TtLpWUmh3AExCeQACI1RloTSCRWYsXrxFMH6ZGDvE
K+Q9LS+jtkPCtOrbr+j8FU0Dgxh/5P0I2xR4hcgAAQKBgQDkcnwcaWRZv0uFxAtj
q3pVelWuu3uapwroO9asmeWsmL3LQeW22X5CNy1gYOlhyG6FqfMLOmzhCicFYX45
6EiDJpyX/LVcSDmzmTDwI25uEunhyhVATJWqwaITdLrJf8KDqqO8bvUHc/wB//2T
OTWpUB542DZJ2A8aServjR6ErwKBgQD19l+5xCHLOldtV56hbAQnhhl8lUAL/mBq
wXNrDNeqmDYFJ3kkHWk5raXUQR41qAubhKnLUJ4qj6FIBcRmsrTMITMWZ9/GzJhK
mNU+nync2IlSS7g3Vyee3wz1Fd2dRA3NwZ9JVK+xTSKgw1a/VXKcfC+iYnXmVIxa
3cCIZ9Um+QKBgQDE34Dj/1OzIG+WbPgfwiTgS1hSCFKiWfjFYORFxS8wykUuSLEO
Hmt35xNc7sfSNChDWs4QzB4O5m/wbC+a+fqbxAfJ18f4KmpHw+pv2SkPBY+3vS8J
Rbbp/IuP1tYuVsMsMz9+YeUasjLpClLesLv1GQ3ZuQM4KlIBptgn7+bwEwKBgQC1
ZDk8etShWClZziCC03JM46ywIDHXpoXctUY1UIdMnGxaaL4CUF5l1xZQ7qUk1QWa
b7/43T+IC9zZjMdHJcwILwPKJlj197TobsX1JNRutpKvSoBU78WceMrJhJKnhKTZ
dU3PetEHZOeAwA6dlJqtpThL/WkNsJTB/oAbGNgtoQKBgG4ytUXXwp61VHm/3Pon
9d6z5o02AQVCppJRcJwehbAm14813G/jPfjwM+KZ2ikhs+eW1peWhBrCo+M5/u5T
bxeDm9cbLMewkYNIdvUxtaBb+fJtIBAngAL2HEhqBdUFoQI+lr+F802UO2aM8Sg+
n82S/+EJZomQ7hhO7qnLtxkI
-----END PRIVATE KEY-----""")

pkcs0 = PKCS1_v1_5.new(rsa0)
pkcs1 = PKCS1_v1_5.new(rsa1)

def parse(mid, dstport, data, key):
    while len(data) >= 20:
        plen, iv = struct.unpack(">I16s", data[:20])
        assert plen % 16 == 0
        if len(data) < 20 + plen:
            break
        pkt = data[20:20+plen]
        del data[:20+plen]
        cipher = AES.new(key, mode=AES.MODE_CBC, iv=iv)
        r = unpad(cipher.decrypt(pkt), 16)
        print(mid, dstport, r.hex(), sep="\t")

class MuxStream:
    def __init__(self):
        self.c2s = bytearray()
        self.s2c = bytearray()
        self.key = None

    def add(self, mid, dstport, data):
        if dstport == 8888:
            self.c2s += data
        else:
            self.s2c += data

        if self.key is None and len(self.c2s) >= 290 and len(self.s2c) >= 290:
            kex0 = self.s2c[2:258]
            kex1 = self.c2s[2:258]
            key0 = pkcs0.decrypt(kex0, sentinel)
            assert key0 != sentinel
            key1 = pkcs1.decrypt(kex1, sentinel)
            assert key1 != sentinel
            self.key = bytes([a^b for a,b in zip(key0, key1)])
            assert hashlib.sha256(self.key).digest() == self.s2c[258:290]
            assert hashlib.sha256(self.key).digest() == self.c2s[258:290]
            self.s2c = self.s2c[290:]
            self.c2s = self.c2s[290:]

        if self.key is not None:
            if dstport == 8888:
                parse(mid, dstport, self.c2s, self.key)
            else:
                parse(mid, dstport, self.s2c, self.key)

streams = defaultdict(MuxStream)

for row in open("dump2.txt"):
    stream, dstport, cmd, mid, data = row.split("\t")
    dstport = int(dstport)
    cmd = int(cmd)
    mid = int(mid)
    data = bytes.fromhex(data)
    if cmd == 1:
        streams[mid].add(mid, dstport, data)
