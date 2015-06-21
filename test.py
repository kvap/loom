#!/usr/bin/env python2

from loom import Loom
from time import sleep

def longfunc(x, iters=10):
	for i in range(iters):
		sleep(0.1)
		print(x)

longfunc('begin', 3)
with Loom(parallel=True) as l:
	l(longfunc, 'alpha', 3)
	with l.spindle() as s:
		s(longfunc, 'beta 1', 3)
		s(longfunc, 'beta 2', 4)
		s(longfunc, 'beta 3', 10)
	l(longfunc, 'gamma', 10)
longfunc('end', 3)
