from Crypto.Util.number import bytes_to_long, isPrime, long_to_bytes
from tqdm import tqdm
from multiprocessing import Pool

assert (3/2)*2 == 3, "py3"


ct = 5602276430032875007249509644314357293319755912603737631044802989314683039473469151600643674831915676677562504743413434940280819915470852112137937963496770923674944514657123370759858913638782767380945111493317828235741160391407042689991007589804877919105123960837253705596164618906554015382923343311865102111160
p = 6722156186149423473586056936189163112345526308304739592548269432948561498704906497631759731744824085311511299618196491816929603296108414569727189748975204102209646335725406551943711581704258725226874414399572244863268492324353927787818836752142254189928999592648333789131233670456465647924867060170327150559233

def encrypt(m):
    return pow(m, 1 << 64, p)


def legendre(a, p):
    return pow(a, (p - 1) // 2, p)

def tonelli(n, p):
    assert legendre(n, p) == 1, "not a square (mod p)"
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1
    if s == 1:
        return pow(n, (p + 1) // 4, p)
    for z in range(2, p):
        if p - 1 == legendre(z, p):
            break
    c = pow(z, q, p)
    r = pow(n, (q + 1) // 2, p)
    t = pow(n, q, p)
    m = s
    t2 = 0
    while (t - 1) % p != 0:
        t2 = (t * t) % p
        for i in range(1, m):
            if (t2 - 1) % p == 0:
                break
            t2 = (t2 * t2) % p
        b = pow(c, 1 << (m - i - 1), p)
        r = (r * b) % p
        c = (b * b) % p
        t = (t * c) % p
        m = i
    return r

m = ct
for i in tqdm(range(64)):
    m = tonelli(m, p)

assert encrypt(m) == ct

k = p-1
for i in range(29):
    x = k
    try:
        k = tonelli(x, p)
    except AssertionError:
        break

assert encrypt(k) == 1
