#!/usr/bin/python
#coding:utf8

from libjade import *

a='hi, this / is jadesoul\'s computer, the char is \\. haha'
a={'k/ey':a, 'k2/a':{'j/2':'aaa"asd//as/d'}}
print a
print repr(a)
jwrite(a, 'a.json')
print fread('a.json')
print jread('a.json')

if __name__=='__main__':
	pass

