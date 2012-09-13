#coding:utf8

import hashlib
from timeutil import time_init, time_gap, now
# md5
def md5(t):
	return hashlib.md5(t).hexdigest()
	
def md5_bin(t):
	return hashlib.md5(t).digest()
	
# sha1
def sha1(t):
	return hashlib.sha1(t).hexdigest()
	
def sha1_bin(t):
	return hashlib.sha1(t).digest()
	
if __name__=='__main__':
	a = "a test string"
	print hashlib.md5(a).hexdigest()
	print hashlib.sha1(a).hexdigest()
	print hashlib.sha224(a).hexdigest()
	print hashlib.sha256(a).hexdigest()
	print hashlib.sha384(a).hexdigest()
	print hashlib.sha512(a).hexdigest()
	
	ss=[str(i) for i in xrange(5000000)]
	s=''.join(ss)
	print now()
	time_init()
	print md5(s)
	print time_gap('md5')
	print sha1(s)
	print time_gap('sha1')
