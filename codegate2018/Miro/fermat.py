def isqrt(n):
    x = n
    y = (x + n // x) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x

def fermat(n, verbose=False):
    a = isqrt(n)
    b2 = a*a - n
    b = isqrt(n)
    count = 0
    while b*b != b2:
        if verbose:
            print('Trying: a=%s b2=%s b=%s' % (a, b2, b))
        a = a + 1
        b2 = a*a - n
        b = isqrt(b2)
        count += 1
    p = a+b
    q = a-b
    print('a=',a)
    print('b=',b)
    print('p=',p)
    print('q=',q)
    print('pq=',p*q)
    return p,q

fermat(0x1C20BDC017E3CAA3C579B40D439E2ECD70F12C4D7F2764784C95A3FDDBA00981BA9CE5B227ADE47B0A7A0A8ACABA4541AB95C52F6B6DE3DF9EC090C6C356445B21BE437ABE10214D0B4A398A96743BBF70C864687FB2EC929F01D6EDAB2D987FE09799AD2204A2704F33061DBF9C2E03B332F0BA1A446644C864A06CD586D480B, False)
