## Miro - Cryptography Challenge

Miro was a cryptography challenge in which a Python script, `client.py`, and 
PCAP, `miro.pcap` are given.

`client.py` allowed us to connect to a maze game, where the maze was the same
every time and there was a single path. At first, we could move `down` and 
`right`, but once we tried to move `left`, it gave an error. Examining 
`client.py`, we noticed the following section of code.

```python
while 1:
    data = recv_until(tls_client, "Input : ")
    print data
    #message
    user_input = raw_input()
    
    if user_input == "u":
        print "Sorry.. Not support function.."
        exit()
    elif user_input == "d": 
        tls_client.send("6423e47152f145ee5bd1c014fc916e1746d66e8f5796606fd85b9b22ad333101\n")
    elif user_input == "r":
        tls_client.send("34660cfdd38bb91960d799d90e89abe49c1978bad73c16c6ce239bc6e3714796\n")
    elif user_input == "l":
        print "Sorry.. Not support function.."
        exit()
    else:
        print "Invalid input!"
        exit()   
```

The client script didn't just send the character representing the move we 
wanted to make - it sent under TLSv1.2 a 64-byte hash that represented the 
move. 

The main issue was that the up and left moves weren't implemented, and we 
didn't know the hashes that were to be sent for them. 

Looking at the PCAP, we saw that it contained data being sent under TLSv1.2.
A reasonable guess given the context of the problem was that the PCAP was a
capture of a game which included the `left` and `up` moves via the hashes that
represent them.

We extracted the public certificate from the network capture as `public.der`
using Wireshark's 'Export Packet Bytes...' feature on the packet containing
the certificate.

Information could then be extracted using openssl.

```
$ openssl x509 -inform-DER -in public.der -text
$ openssl x509 -inform DER -in public.der -modulus -noout
```

* RSA-1025
* Public modulus `N = 0x1C20BDC017E3CAA3C579B40D439E2ECD70F12C4D7F2764784C95A3FDDBA00981BA9CE5B227ADE47B0A7A0A8ACABA4541AB95C52F6B6DE3DF9EC090C6C356445B21BE437ABE10214D0B4A398A96743BBF70C864687FB2EC929F01D6EDAB2D987FE09799AD2204A2704F33061DBF9C2E03B332F0BA1A446644C864A06CD586D480B`
* Public exponent `e = 65537`

Our goal was to be able to reconstruct a valid private certificate to get the
data encrypted under TLSv1.2. To do this, we needed to recover `p` and `q`. 

Fermat factorization was a good initial approach. 

We adapted the Fermat factorization code from [a Stack Overflow post](https://stackoverflow.com/questions/20464561/fermat-factorisation-with-python/20465181#20465181) 
and ran it with the `N` that we had.

```python
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
```

We received the following values for `p` and `q`:
* `p = 17777324810733646969488445787976391269105128850805128551409042425916175469483806303918279424710789334026260880628723893508382860291986009694703181381742497`
* `q = 17777324810733646969488445787976391269105128850805128551409042425916175469168770593916088768472336728042727873643069063316671869732507795155086000807594027`

Then to craft our own private RSA certificate, we used 
[rsatool](https://github.com/ius/rsatool) and saved the result as `private.pem`.

```
$ python rsatool.py -p 17777324810733646969488445787976391269105128850805128551409042425916175469483806303918279424710789334026260880628723893508382860291986009694703181381742497 -q 17777324810733646969488445787976391269105128850805128551409042425916175469168770593916088768472336728042727873643069063316671869732507795155086000807594027 -o private.pem
```

Once we had a private key, we could then use Wireshark again to decrypt the 
data. We used the RSA keys list under the SSL Protocol in Preferences. However,
the data didn't seem to visibly change/be affected, so we added in a SSL debug
file to look into the issue. Examining the SSL debug file, `debug.txt`, we 
could see the traffic in plaintext. 

From `debug.txt` we recovered the two hashes for `up` and `left`. `left` came
first in the PCAP as it was the first of the two that was used in the maze.

* `left: 27692894751dba96ab78121842b9c74b6191fd8c838669a395f65f3db45c03e2`
* `up: 9de133535f4a9fe7de66372047d49865d7cdea654909f63a193842f36038d362`

`client.py` was then modified to `client_solve.py` so that the maze game could
be played with the `left` and `up` moves enabled.

```python
while 1:
    data = recv_until(tls_client, "Input : ")
    print data
    #message
    user_input = raw_input()
    
    if user_input == "u":
        tls_client.send("9de133535f4a9fe7de66372047d49865d7cdea654909f63a193842f36038d362\n")
    elif user_input == "d": 
        tls_client.send("6423e47152f145ee5bd1c014fc916e1746d66e8f5796606fd85b9b22ad333101\n")
    elif user_input == "r":
        tls_client.send("34660cfdd38bb91960d799d90e89abe49c1978bad73c16c6ce239bc6e3714796\n")
    elif user_input == "l":
        tls_client.send("27692894751dba96ab78121842b9c74b6191fd8c838669a395f65f3db45c03e2\n")
    else:
        print "Invalid input!"
        exit()    
```

Once we got through the maze, we were given the flag:

**C4n_y0u_d3crypt_th3_P4ck3t??**
