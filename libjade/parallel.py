#!/usr/bin/python
#coding:utf8

from multiprocessing import Pool

def example_func(x):
	return x*x

def example_handle(results):
	print results

def parallel(func, data, handle=None):
	pool=Pool()
	rets=pool.map(func, data)
	if handle:
		handle(rets)
	del pool

if __name__=='__main__':
	parallel(example_func, range(10), example_handle)
