#coding:utf8

from os import system as run
import sys

def require(module):
	cmd='sudo apt-get install python-pip ; pip install %s' % module
	print cmd
	run(cmd)

def include(path):
	sys.path.append(path)


if __name__=='__main__':
	require('DBUtils')


