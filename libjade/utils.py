#coding:utf8

import string
import math
import os
import sys

# from pyquery import PyQuery as Q
# from lxml import etree
'''
# example:
d = Q(url='http://google.com/', parser='html')
d = Q(filename=path_to_html_file, parser='xml')#html_fragments
'''

#os detection
from platform import system as os_type
#system default encoding
sys_encoding='gbk' if os_type()=='Windows' else 'utf8'
windows=(os.name=='nt')
linux=not windows

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


def U(s):
	'''转化utf8编码的文件中的字符串为unicode'''
	return s.decode('utf8')
	
def US(s):
	'''转化utf8编码的文件中的字符串为unicode后转化成系统编码'''
	return s.decode('utf8').encode(sys_encoding)


def include(pth):
	sys.path.append(pth)

if __name__=='__main__':
	print 'windows=', windows
	print 'linux=', linux
	
	