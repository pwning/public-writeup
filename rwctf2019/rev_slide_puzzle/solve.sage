data = bytearray(open('verify_resp.bin', 'rb').read())
s = data[0]
r = []
for p in range(s):
    r.append(data[p*s+1:p*s+s+1])
l = [ord(c) for c in data[s*s+1:].decode('utf8')]

soln = Matrix(r)\Matrix(l).T
print bytearray(c[0] for  c in list(soln))

# rwctf{wr1te-0nce~DEBUG+ev3ry|wh3re}
