import play

f = open("code", "rb")
code = f.read()
code = bytearray(code)
f.close()

#flag = input().strip()
flag = '01234567'
flag = bytearray(flag, "utf-8")

if play.O0O0O0O00OO0O0O0O(code, flag):
    print(":)")
else:
    print(":(")
