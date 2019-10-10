from pwn import *

r = remote("aab2596ac4a422a9f803ed317089c399b818bb72.balsnctf.com", 30731)
prefix = r.recvline().split('(')[1].split(' + ???')[0]
print(prefix)
p = iters.mbruteforce(lambda x: int(hashlib.sha256(prefix+x).hexdigest()[:5],16) <= 3, '123456789', length=20)
r.sendline(p)

def recv_challenge():
    print(r.recvuntil('Challenge '))
    print(r.recvline())
    contract = r.recvline()
    print(contract)
    contract = contract[4:]
    contract = contract[contract.index('60806040'):]
    print(contract)
    return contract

def solve_0(contract):
    # call a single function
    print(contract[110:110+8])
    return contract[110:110+8]

def solve_1(contract):
    # find the function that will let us win, and call it
    win = contract.index('5b6001600080') // 2
    win = '{:04x}'.format(win)
    print(win)
    win = (contract.index('61' + win))//2 - 5
    win = '{:04x}'.format(win)
    print(win)
    win = (contract.index('61' + win + '57'))//2 - 4
    win = '{:04x}'.format(win)
    print(win)
    win = (contract.index('61' + win + '57'))//2 - 5
    print(contract[win*2:win*2+8])
    return contract[win*2:win*2+8]

def solve_2(contract):
    # find what data we need to pass to the function
    sol = contract[112:112+8]
    t = contract.index('540392505081905550') + len('540392505081905550')
    print(t)
    target = int(contract[t:t+2],16)
    print(target)
    l = target - 0x60 + 1
    target = (1 << 256) - (int(contract[t+2:t+2+l*2],16) - 0x64 + 1)
    print(target)
    print('{:064x}'.format(target))
    sol += '{:064x}'.format(target)
    print(sol)
    return sol


contract = recv_challenge()
sol = solve_0(contract)
r.sendline(sol)

contract = recv_challenge()
sol = solve_1(contract)
r.sendline(sol)

contract = recv_challenge()
sol = solve_2(contract)
r.sendline(sol)

for k in range(7):
    contract = recv_challenge()
    if len(contract) < 474:
        sol = solve_0(contract)
    elif len(contract) < 700:
        sol = solve_2(contract)
    else:
        sol = solve_1(contract)
    r.sendline(sol)

r.interactive()
