import subprocess
import pyshark

f = pyshark.FileCapture('hackpad.pcap', display_filter='http')
print('done parsing')
secret = '3ed2e01c1d1248125c67ac637384a22d997d9369c74c82abba4cc3b1bfc65f026c957ff0feef61b161cfe3373c2d9b905639aa3688659566d9acc93bb72080f7e5ebd643808a0e50e1fc3d16246afcf688dfedf02ad4ae84fd92c5c53bbd98f08b21d838a3261874c4ee3ce8fbcb96628d5706499dd985ec0c13573eeee03766f7010a867edfed92c33233b17a9730eb4a82a6db51fa6124bfc48ef99d669e21740d12656f597e691bbcbaa67abe1a09f02afc37140b167533c7536ab2ecd4ed37572fc9154d23aa7d8c92b84b774702632ed2737a569e4dfbe01338fcbb2a77ddd6990ce169bb4f48e1ca96d30eced23b6fe5b875ca6481056848be0fbc26bcbffdfe966da4221103408f459ec1ef12c72068bc1b96df045d3fa12cc2a9dcd162ffdf876b3bc3a3ed2373559bcbe3f470a8c695bf54796bfe471cd34b463e9876212df912deef882b657954d7dada47'

for i in xrange(8+256,8+256*1000,2): # blargh
    c = f[i]['urlencoded-form']
    s = f[i+1]['data-text-lines']
    if 'Internal Server Error' in str(s):
        continue
    print(i)
    print(c)
    print(s)

# from pwn import xor; print(xor(data,16,prev_block))

'''
3ed2e01c1d1248125c67ac637384a22d In cryptography,
997d9369c74c82abba4cc3b1bfc65f02  a padding oracl
6c957ff0feef61b161cfe3373c2d9b90 e attack is an a
5639aa3688659566d9acc93bb72080f7 ttack which is p
e5ebd643808a0e50e1fc3d16246afcf6 erformed using t
88dfedf02ad4ae84fd92c5c53bbd98f0 he padding of a 
8b21d838a3261874c4ee3ce8fbcb9662 
8d5706499dd985ec0c13573eeee03766        hitcon{H4
f7010a867edfed92c33233b17a9730eb cked by a de1ici
4a82a6db51fa6124bfc48ef99d669e21 0us pudding '3'}
740d12656f597e691bbcbaa67abe1a09 
f02afc37140b167533c7536ab2ecd4ed 
37572fc9154d23aa7d8c92b84b774702 
632ed2737a569e4dfbe01338fcbb2a77 
ddd6990ce169bb4f48e1ca96d30eced2 
3b6fe5b875ca6481056848be0fbc26bc panded) to be co
bffdfe966da4221103408f459ec1ef12 mpatible with th
c72068bc1b96df045d3fa12cc2a9dcd1 
62ffdf876b3bc3a3ed2373559bcbe3f4 -
70a8c695bf54796bfe471cd34b463e98 -
76212df912deef882b657954d7dada47 ----------------

Flag: hitcon{H4cked by a de1ici0us pudding '3'}

Wikipedia text:
In cryptography,
 a padding oracl
e attack is an a
ttack which is p
erformed using t
he padding of a 
cryptographic me
ssage. In crypto
graphy, variable
-length plaintex
t messages often
 have to be padd
ed (expanded) to be compatible with the underlying cryptographic primitive. 
'''
