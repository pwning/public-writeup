#!/usr/bin/env python
import angr
import subprocess
import shlex

for i in xrange(1, 102):
    prob = 'prob%d' % i
    cmd = 'objdump -d %s | grep "<puts@plt>" | tail -n +2 | head -1' % prob
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    stdout, stderr = p.communicate()
    addr = int(stdout.split(":")[0].replace(' ', ''), 16)

    project = angr.Project("./%s" % prob)

    argv1 = angr.claripy.BVS("argv1",100*8)
    initial_state = project.factory.path(args=["./%s" % prob,argv1])

    pg = project.factory.path_group(initial_state)

    pg.explore(find=addr)

    found = pg.found[0]
    solution = found.state.se.any_str(argv1)

    solution = solution[:solution.find("\x00")]

    print '%03d: %s' % (i, solution)

