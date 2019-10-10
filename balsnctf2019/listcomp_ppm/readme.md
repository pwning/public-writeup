# listcomp - programming challenge

## Description

listcomp consisted of three simple programming challenges, but the code had to be written as a Python list comprehension expression, and the length of the expression was often fairly limited. Although we were aware that we could have exploited the execution environment, we chose to take the programming challenge at face value.

## Solution

### Part 1

All we have to do is add up pairs of numbers, provided one line at a time. This is easy:

```
[print(sum(map(int,input().split())))for _ in range(int(input()))]
```

### Part 2

This was the really brutally hard part for us. The challenge is to solve a knapsack problem with a small bound on the cost, which can be solved using a dynamic programming approach. However, we were only allowed 200 characters to do this.

For each line of input, we update an array representing the best possible outcome for each total cost. In regular code, this looks like this:

```
n, m = map(int, input().split())
d = [0] * (m+1)
for i in range(n):
    v, c = map(int, input().split())
    d = [max(d[j], 0 if j < c else d[j-c]+v) for j in range(m+1)]

print(d[-1])
```

We converted everything into a bunch of crazy nested list comprehensions, applying some classic Python golf tricks in the process. Changing `d` each iteration was the hardest part - we initially tried `getattr/setattr` but it was too long, so we eventually settled on using `d.extend([...][d.clear():])`, which first computes the new array, then calls `d.clear()`, then extends the array.

194 bytes!

```
[([d.extend([max(d[j],0if j<c else d[j-c]+v)for v,c in[I()]for j in range(m+1)][d.clear():])for _ in[0]*n],print(d[-1]))for I in[lambda:map(int,input().split())]for n,m in[I()]for d in[[0]*-~m]]
```

### Part 3

This was a straightforward task to determine the depth of a tree given an array of parents. This is easy to do: we make an array where each entry is the depth of the corresponding node, and build it up as we read each tree node.

```
[(input(),[v.append(v[r]+1)for r in map(int,input().split()[1:])],print(max(v)))for v in[[0]]]
```

### Flag

With all of that done, we got a flag:

`Balsn{8_8_l13t_c0mp63h3ns10n_0r_A_5en8_80x_ch01l3n93}`
