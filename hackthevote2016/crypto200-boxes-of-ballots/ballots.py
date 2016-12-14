import socket
import json
import string

conn = socket.socket()
conn.connect(('boxesofballots.pwn.republican', 9001))

def get_enc(data):
	j = {
		"data": data,
		"op":"enc"
	}
	conn.send(json.dumps(j) + '\n')
	return json.loads(conn.recv(1000))['data']

sol = ''
for i in range(32):
	base = 'A' * (15 - (i % 16))
	desired = get_enc(base)
	examining = (i // 16 + 1) * 32
	for c in string.printable:
		if get_enc(base + sol + c)[:examining] == desired[:examining]:
			sol += c
			print(sol)
			break
	else:
		raise Exception("no satisfying flag byte")
