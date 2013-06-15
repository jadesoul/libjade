#!/usr/bin/python
#coding:utf8

import multiprocessing as mp
from multiprocessing import Pool

def example_func(x):
	return x*x

def example_handle(results):
	print results

def parallel(func, data, handle=None):
	cpus=mp.cpu_count()
	# if cpus>5: cpus=cpus/2+1;
	pool=Pool(processes=cpus)
	rets=pool.map(func, data)
	if handle:
		handle(rets)
	del pool

if __name__=='__main__':
	parallel(example_func, range(10), example_handle)
