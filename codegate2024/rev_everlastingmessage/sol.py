import pickle, sys
from itertools import combinations
from tqdm import tqdm
from multiprocessing import Pool
from struct import pack

with open("invfuncs", "rb") as f:
    ds = pickle.load(f)

with open("flag_enc", "rb") as f:
    CT = f.read()

out = []

def solve(i):
    chunk = CT[i:i+5]
    chunk = int.from_bytes(chunk, "little")
    j = i // 5

    for k in range(11):
        for comb in combinations(range(40), k):
            flips = 0
            for c in comb:
                flips ^= 1 << c
            try:
                return ds[j%4][chunk^flips]
            except Exception as e:
                pass
    # no result found, shouldn't happen
    print(f"NOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO @ {i}")

if __name__ == "__main__":
    with Pool(15) as p:
        out = list(tqdm(p.imap(solve, range(int(sys.argv[1]), int(sys.argv[2]), 5))))

    result = []
    for i in tqdm(range(0, len(out), 2)):
        t = (out[i+1] << 20) + out[i]
        result.append(pack("<Q", t)[:5])

    with open(f'maybe_flage_{sys.argv[1]:09}', 'wb') as f:
        f.write(b''.join(result))
