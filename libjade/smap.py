#coding:utf8

import os, sys, re

def expr_var(name, val, exargs):
	return '%s=%s\n' % (name, val)
	
def print_var(name, val, exargs):
	print 'the %s is %s' % (name, val)
	
def smap(s, func, domain, exargs=[], rstr=True, glue=''):
	r=[]
	for i in s.split():
		ret=func(i, domain[i], exargs)
		if ret!=None:
			r.append(ret)
	return glue.join(r) if rstr else r
	
	
def smap_var(s, domain):
	return smap(s, expr_var, domain)
	
r_varible_in_str=re.compile(r'(\$[a-zA-Z_][a-zA-Z0-9_]*)')
r_slash_dollar=re.compile(r'\\\$')

def expands(s, domain):
	'''
	expand varibles in a string like linux shell
	example:
		expands('$a, $b, $c', locals())
	'''
	# print s
	parts=r_varible_in_str.split(s)
	# print parts
	for i, part in enumerate(parts):
		l=len(part)
		if l==0:
			pass
		elif l==1 and part=='$':
			pass
		elif l>=2 and part[:2]=='$$':
			parts[i]=part[1:]
		elif part[0]=='$' and r_varible_in_str.match(part):
			if len(part)>1:
				vn=part[1:]
				# print vn
				if vn in domain:
					val=domain[vn]
					parts[i]='%s' % val
				else:
					parts[i]=''
		else:
			parts[i]=part.replace('$$', '$')
	return ''.join(parts)
	
def smap_dict(s, domain):
	dct={}
	for i in s.split():
		if i in domain:
			dct[i]=domain[i]
	return dct
	
	
if __name__=='__main__':
	a=1
	b=2
	c=b
	s='this time a=$a, $d b=$b and c=$c'
	for i in r_varible_in_str.findall(s):
		print i
	print expands(s, locals())
	

