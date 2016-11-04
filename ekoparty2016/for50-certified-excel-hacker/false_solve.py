#!/usr/bin/env python

import base64
import sha

answer = ""

# VBA code runs 1 to 16777216 but VBA loops include the 16777216
for i in range(1,16777217):
	answer = base64.b64encode(sha.new(answer).digest())

print "EKO{" + answer.replace("=", "") + "}"

# Result is EKO{DCEUslnl7DeiLWSdCLi0l1fxdc8}