#coding:utf8

import cjson
import json
import simplejson
from utils import *

# jsonmodule=simplejson
# jsonmodule=json
jsonmodule=cjson

def json_encode(obj):
	return jsonmodule.encode(obj)
	

def json_decode(obj):
	return jsonmodule.decode(obj)
	

def jsonwrite(obj, fp):
	fwrite(json_encode(obj), fp)
	
def jsonread(fp, encoding=sys_encoding):
	return json_decode(fread(fp).decode(encoding))
	
# another more friendly version
def jsonencode(obj, is_unicode=False):
	if not is_unicode:
		s=simplejson.dumps(obj, encoding='utf8', skipkeys=False, indent=4, ensure_ascii=False)
	else:
		s=simplejson.dumps(obj, skipkeys=False, indent=4, ensure_ascii=False)
	return s
	
def jsondump(obj, is_unicode=False):
	s=jsonencode(obj, is_unicode)
	print s
	
def jsonexport(obj, is_unicode=False):
	return jsonencode(obj, is_unicode)
	
if __name__=='__main__':
	pass

