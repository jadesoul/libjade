#coding:utf8

import traceback

#type detect
def is_dict(dct):
	return type(dct) is dict

def is_list(lst):
	return type(lst) is list

def is_set(st):
	return type(st) is set

def is_tuple(tpl):
	return type(tpl) is tuple
	
def is_float(num):
	return type(num) is float

def is_int(num):
	return type(num) is int

def is_num(num):
	return is_float(num) or is_int(num)
	
def is_str(s):
	return type(s) is str
	
def is_unicode(s):
	return type(s) is unicode
	
#for deep copy and uicode clone
from copy import deepcopy as clone

def unicode_clone_obj(obj, encoding='utf8'):
	'''
	deep copy an object and translate all str into unicode
	'''
	if is_str(obj):
		return obj.decode(encoding)
	elif is_unicode(obj) or is_num(obj):
		return obj
	elif is_dict(obj):
		new={}
		for k in obj:
			v=unicode_clone_obj(obj[k], encoding)
			k=unicode_clone_obj(k, encoding)
			new[k]=v
		return new
	elif is_list(obj):
		return [unicode_clone_obj(i, encoding) for i in obj]
	elif is_tuple(obj):
		return tuple([unicode_clone_obj(i, encoding) for i in obj])
	elif is_set(obj):
		return set([unicode_clone_obj(i, encoding) for i in obj])
		
#alias name
uclone=unicode_clone_obj
	
#for dump
def dump(obj, prefix=''):
	if is_str(obj):
		print prefix, 'string(%d)\t:\t' % len(obj), obj
	elif is_float(obj):
		print prefix, 'float\t:\t', obj
	elif is_int(obj):
		print prefix, 'int\t:\t', obj
	elif is_unicode(obj):
		print prefix, 'unicode(%d)\t:\t' % len(obj), obj
	elif is_list(obj):
		print prefix, '['
		for ind, i in enumerate(obj):
			dump(i, prefix+'\t'+str(ind)+'\t')
		print prefix, ']'
	elif is_tuple(obj):
		print prefix, '('
		for ind, i in enumerate(obj):
			dump(i, prefix+'\t'+str(ind)+'\t')
		print prefix, ')'
	elif is_set(obj):
		print prefix, '<'
		for ind, i in enumerate(obj):
			dump(i, prefix+'\t'+str(ind)+'\t')
		print prefix, '>'
	
	elif is_dict(obj):
		print prefix, '{'
		ind=0
		for k, v in obj.items():
			dump(k, prefix+'\tk'+str(ind)+'\t')
			# print prefix, '\t\t=>'
			dump(v, prefix+'\tv'+str(ind)+'\t')
			print prefix
			ind+=1
		print prefix, '}'
	else:
		# print 'not a normal type:', type(obj)
		print prefix, obj

		
def echo(s):
	for i in s:
		print i

#dump tools
def dump_list(l):
	for i in l:
		print i		
if __name__=='__main__':
	dump(dir())

