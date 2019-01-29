#!/usr/bin/env python

from __future__ import print_function
from pwn import *

t = remote('110.10.147.104', 15712)

answer = ''

t.sendline('G')
for _ in range(100):
	t.recvuntil('***')
	t.recvline()

	matrix = [list(map(int, t.recvline(keepends=False).split())) for _ in range(7)]

	dp = [[0] * 7 for _ in range(7)]
	for r in range(7):
		dp[r][0] = matrix[r][0]

	for c in range(1, 7):
		for r in range(7):
			dp[r][c] = matrix[r][c] + dp[r][c-1]
			if r > 0:
				dp[r][c] = min(dp[r][c], matrix[r][c] + dp[r-1][c])

		for r in range(5, -1, -1):
			dp[r][c] = min(dp[r][c], matrix[r][c] + dp[r+1][c])

	result = min(dp[r][6] for r in range(7))
	answer += chr(result)

	t.sendline(str(result))

print(answer)
print(answer.decode('base64'))

# answer = 'RkxBRyA6IGcwMG9vT09kX2owQiEhIV9fX3VuY29tZm9ydDRibGVfX3MzY3VyaXR5X19pc19fbjB0X180X19zZWN1cml0eSEhISEh'
# FLAG : g00ooOOd_j0B!!!___uncomfort4ble__s3curity__is__n0t__4__security!!!!!

