#coding:utf8
'''
Here defines a new config format, the format is a kind of json-python
mixture file, the json format is not strictly required as the python json modules
did, but as easy as the javascript style.

I'd like to call this "pyson" format, it is a easy format, For example:

a={
#commnet1
	b=1	#commnet2
	c=2
	d=['hi,%d' % i for i in range(3)]
}
b=a
c="b "

will be parsed into an python(or json) object:

{
	'a':{
		'b':1,
		'c':2,
		d:"['hi,0', 'hi,1', 'hi,2']"
	},
	'b':'a',
	'c':'b '
}

The format is like json, but we do not need to care about the commas anymore,
and simple python code (inline for/if/elif/else) can be embeded into it.
Besides, lines or part of a line begin with # symbol will be igored as comments. 
This python module "pyson" will do the pyson_decode job by a given pyson string. 
and will do the pyson_encode work by a given object.

By jadesoul v-shew @ 2011-10-27

'''
from dbg import *
from sort import *

def pyson_decode(s):
	'''
	parse a string in pyson format
	return a python object
	'''
	ls=s.split('\n')
	rs=[]
	for l in ls:
		l=l.strip()
		pos=l.find('#')
		if pos!=-1: l=l[:pos]	#remove the commnets
		if not l: continue
		pos=l.find('=')
		if pos==-1: 
			rs.append(l+',' if l=='}' else l)	#add }
			continue
		key=l[:pos].strip()	#get key and val by split =
		val=l[pos+1:].strip()
		if not key or not val:
			continue
		try:
			val=eval(val)	#if is a num or py repression
		except:
			val=eval('\'\'\''+val.replace('\\\\', '\\')+'\'\'\'')	#else assume as a str
		# no need , after {
		rs.append('"%s":%s' % (key, repr(val)+',' if val!='{' else val))
	s='{\n'+'\n'.join(rs)+'\n}'	#wrap it by a {}
	return eval(s)	#finally the obj
	
def pyson_encode(obj, d=-1):
	if (d==-1): assert is_dict(obj)
	if is_dict(obj):
		ss=[]
		if d!=-1: ss.append('{')
		for k, v in ksorted(obj):
			ss.append('\t'*(d+1)+('%s=%s' % (k, pyson_encode(v, d+1)))) 
		if d!=-1: ss.append('\t'*d+'}')
		return '\n'.join(ss)
	else:
		return repr(obj)
		
if __name__=='__main__':
	s='''
a={
#commnet1
	b=1 sada
	c=2
	d=['hi,%d' % i for i in range(3)] #commnet1
	e={
		f=1
		g=sd\ks\asdasd\asdasd\asd
	}
}
b=a
c="b "
'''
	o=pyson_decode(s)
	print o
	print pyson_encode(o)