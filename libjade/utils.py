#coding:utf8

import string
import math
import os
import sys
from dbg import *

#try to import PyQuery
try:
	from pyquery import PyQuery as Q
	#from lxml import etree
except:
	pass

'''
# usage example:
d = Q(url='http://google.com/', parser='html')
d = Q(filename=path_to_html_file, parser='xml') # html_fragments
'''

#try to prepare for pyx
try:
	import pyximport
	pyximport.install()
except:
	pass
	
#os detection
# from platform import system as os_type
#system default encoding
# sys_encoding='gbk' if os_type()=='Windows' else 'utf8'

windows=(os.name=='nt')
linux=not windows

#system default encoding
sys_encoding='gbk' if windows else 'utf8'

def mkdict(s, domain, warn=False):
	ret={}
	for i in s.strip().split():
		if warn:
			ret[i]=domain[i]
		else:
			try:
				ret[i]=domain[i]
			except:
				pass
	return ret
	
#other 
def format_tab(s):
	ls=s.split('\n')
	ls=[l for l in ls if len(l.strip())>0]
	for i, l in enumerate(ls):
		l=l.strip()
		if len(l)<10: ls[i-1]+='\t'+l; ls[i]=''
	ls=[l for l in ls if len(l.strip())>0]
	print  '\n'.join(['\t'.join(l.split()) for l in ls])


def uni(s):
	'''自动转化字符串为unicode'''
	if is_unicode(s): return s
	return s.decode(sys_encoding)
	
def _sys(s):
	'''自动转化成系统编码'''
	if is_unicode(s): return s.encode(sys_encoding)
	try:
		s=s.decode('utf8')
	except:
		try:
			s=s.decode('gbk')
		except:
			pass
	assert is_unicode(s)
	return s.encode(sys_encoding)

def utf8(s):
	'''如果是unicode则转化utf8编码，否则直接返回'''
	if is_unicode(s): return s.encode('utf8')
	return s
	
def gbk(s):
	'''如果是unicode则转化gbk编码，否则直接返回'''
	if is_unicode(s): return s.encode('gbk')
	return s
	
def include(pth):
	sys.path.append(pth)

def u8(s):
	'''自动在utf8和unicode之间切换'''
	if type(s) is unicode:
		return s.encode('utf8')
	else:
		return s.decode('utf8')
		
def gb(s):
	'''自动在utf8和gbk之间切换'''
	if type(s) is unicode:
		return s.encode('gbk')
	else:
		return s.decode('gbk')
		
def average(*lst):
	l=len(lst)
	if l==0:
		return 0
	else:
		return 1.0*sum(lst)/l
		
if __name__=='__main__':
	print 'windows=', windows
	print 'linux=', linux
	print utf8('你')
	print utf8(u'你')
	print _sys('你')
	print _sys(u'你')
	print _sys(u'你'.encode('utf8'))
	
