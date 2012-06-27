#coding:utf8

from os import system
from timeutil import now

def run_cmds(cmds):
	for cmd in cmds.strip().split('\n'):
		print now(), '- run cmd:', cmd
		run(cmd)

def run(cmd):
	print 'RUN @', now(), '- CMD:', cmd
	system(cmd)
		
if __name__=='__main__':
	pass

