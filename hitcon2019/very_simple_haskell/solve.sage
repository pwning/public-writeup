"""
The general idea of this solution is that we can figure out what the value
of the cipher applied to the 6 unknown bytes are by computing is symbolically,
then factor that value (since it must be considerably less than the modulus
as 739**48 < n) and use those factors to determine which bits were set in the
flag.
"""


# data from the program directly
n = 134896036104102133446208954973118530800743044711419303630456535295204304771800100892609593430702833309387082353959992161865438523195671760946142657809228938824313865760630832980160727407084204864544706387890655083179518455155520501821681606874346463698215916627632418223019328444607858743434475109717014763667
k = 131
primes = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,139,149,151,157,163,167,173,179,181,191,193,197,199,211,223,227,229,233,239,241,251,257,263,269,271,277,281,283,293,307,311,313,317,331,337,347,349,353,359,367,373,379,383,389,397,401,409,419,421,431,433,439,443,449,457,461,463,467,479,487,491,499,503,509,521,523,541,547,557,563,569,571,577,587,593,599,601,607,613,617,619,631,641,643,647,653,659,661,673,677,683,691,701,709,719,727,733,739]


# translation of functions from haskell
def padz(data, v):
    return [0]*(v - len(data)%v) + data

def getbits(data):
    return [int(x) for y in data for x in bin(ord(y))[2:].zfill(8)]

# translation of calc to make it work with symbolic ring
def calc(data):
    print(len(data))
    r = 1
    for i in range(0, len(data), k):
        r *= r
        cur = data[i:i+k]
        print(cur)
        for p,c in zip(primes, cur):
            r *= p^c
    return r

# create variables for every bit in the unknown part of the flag
B = [var('b{}'.format(i)) for i in range(6*8)]

# encrypt "the flag is hitcon{AAAAAA}", where the As are replaced with
# the symbolic variables above
def symbdo():
    flag = getbits("the flag is hitcon{AAAAAA}")
    flag[19*8:25*8] = B
    flag = flag[::-1]
    orilen = len(flag)
    orilenbits = [int(x) for x in bin(orilen)[2:].zfill(8)]
    efbits = padz(flag, k)
    eolb = padz(orilenbits, k)
    finalbits = eolb + efbits
    #print(finalbits)
    return calc(finalbits[::-1])
print(symbdo())

# the coefficient on the symbolic result of the thing above
coeff = 196343079570631903630614540529360323005081185987320100876699077314479005836109084998724735326468163197091649081159093170849156586048615787727773128093050437777213767514255145357073132580052497932216286530053784414973898393481188310640808256125241882185337468741409253395602654349801709400829108359354382234844665472543678853005068269933791974159151401915545659950920365324003874059712001207015686993257069245502475774566009157229764256818553445529015759922019843583046496096714252889706498924742671189065649481699929344420509587182135467240668651423977755571330362819481562364586579938457450847390625
# the given output
target = 84329776255618646348016649734028295037597157542985867506958273359305624184282146866144159754298613694885173220275408231387000884549683819822991588176788392625802461171856762214917805903544785532328453620624644896107723229373581460638987146506975123149045044762903664396325969329482406959546962473688947985096
# figure out what the symbolic factor attatched to the coefficient must be
target *= inverse_mod(coeff, n)
target %= n

# we know that the target can be directly factorable into the primes that
# come about as the result of the flag characters
wow = dict(factor(target))

# the big symbolic factor on the output of symbdo
lol = "347^(2*b47)*337^(2*b46)*331^(2*b45)*317^(2*b44)*313^(2*b43)*311^(2*b42)*307^(2*b41)*293^(2*b40)*283^(2*b39)*281^(2*b38)*277^(2*b37)*271^(2*b36)*269^(2*b35)*263^(2*b34)*257^(2*b33)*251^(2*b32)*241^(2*b31)*239^(2*b30)*233^(2*b29)*229^(2*b28)*227^(2*b27)*223^(2*b26)*211^(2*b25)*199^(2*b24)*197^(2*b23)*193^(2*b22)*191^(2*b21)*181^(2*b20)*179^(2*b19)*173^(2*b18)*167^(2*b17)*163^(2*b16)*157^(2*b15)*151^(2*b14)*149^(2*b13)*139^(2*b12)*137^(2*b11)*131^(2*b10)*127^(2*b9)*113^(2*b8)*109^(2*b7)*107^(2*b6)*103^(2*b5)*101^(2*b4)*97^(2*b3)*89^(2*b2)*83^(2*b1)*79^(2*b0)"
xd = lol.split(")*")
ans = [0]*48
# check for every factor in the symbolic expression, if the prime is found
# in the target, then we know that the corresponding symbolic variable
# was a '1' and not a zero, so mark accordingly in the answer
for xp in xd:
    base = int(xp.split("^")[0])
    num = xp.split("*")[-1][1:]
    if base in wow:
        ans[int(num)] = 1

# transform the binary matrix to an ascii flag
binaryflag = "".join(str(x) for x in ans)

realflag = hex(int(binaryflag, 2))[2:].decode('hex')
print("hitcon{" + realflag + "}")
