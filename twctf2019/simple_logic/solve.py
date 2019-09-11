s = '''
Pair 1: plain=029abc13947b5373b86a1dc1d423807a enc=b36b6b62a7e685bd1158744662c5d04a
Pair 2: plain=eeb83b72d3336a80a853bf9c61d6f254 enc=614d86b5b6653cdc8f33368c41e99254
Pair 3: plain=7a0e5ffc7208f978b81475201fbeb3a0 enc=292a7ff7f12b4e21db00e593246be5a0
Pair 4: plain=c464714f5cdce458f32608f8b5e2002e enc=64f930da37d494c634fa22a609342ffe
Pair 5: plain=f944aaccf6779a65e8ba74795da3c41d enc=aa3825e62d053fb0eb8e7e2621dabfe7
Pair 6: plain=552682756304d662fa18e624b09b2ac5 enc=f2ffdf4beb933681844c70190ecf60bf
'''.strip().split('\n')

def conv(x):
    z = ''
    for i in x:
        z += '{:04b}'.format(int(i, 16))
    return [int(i) for i in z]

s = [
[conv(i.split("plain=")[1].split()[0]), conv(i.split("enc=")[1])] for i in s
]

rounds = 765
bits = 128

def xor(x, y):
    return [i^j for i,j in zip(x,y)]

def add(x, y):
    carry = 0
    z = [0]*len(x)
    for i in range(len(x))[::-1]:
        a = x[i]
        b = y[i]
        z[i] = carry ^ a ^ b
        carry = int(carry + a + b >= 2)
    return z

def sub(x, y):
    y = [1-i for i in y]
    return add(add(x, y), [0]*127+[1])

flag = conv('43713622de24d04b9c05395bb753d437')

def solve(key, i):
    #print("try", key, i)
    for k in s:
        #print(k[0][-i:], k[1][-i:])
        kk = k[0][-i:]
        for l in range(rounds):
            kk = xor(add(kk, key), key)
        if kk != k[1][-i:]:
            return
    if i == 128:
        print("yay!", key)
        flag2 = flag[:]
        for l in range(rounds):
            flag2 = sub(xor(flag2, key), key)
        #print(flag2)
        flag_final = ''
        for l in range(0, len(flag2), 8):
            x = 0
            for j in range(8):
                x *= 2 
                x += flag2[l+j]
            flag_final += '{:02x}'.format(x)
        print('TWCTF{{{}}}'.format(flag_final))
    solve([0]+key, i+1)
    solve([1]+key, i+1)

solve([0], 1)
solve([1], 1)
