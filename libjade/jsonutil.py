#coding:utf8

from utils import *
from filesys import *

# import json
# import simplejson as json
import cjson as json

def json_encode(obj):
    return json.encode(obj)
    
def json_decode(s):
    return json.decode(s)
    
def json_dump(obj, fp):
    fwrite(json_encode(obj), fp)
    
def json_load(fp, encoding=sys_encoding):
    return json_decode(fread(fp).decode(encoding))

# another more friendly version
def json_export(obj, is_unicode=False):
    import simplejson
    if not is_unicode:
        s=simplejson.dumps(obj, encoding='utf8', skipkeys=False, indent=4, ensure_ascii=False)
    else:
        s=simplejson.dumps(obj, skipkeys=False, indent=4, ensure_ascii=False)
    return s
    
# alias
jencode=json_encode
jdecode=json_decode
jwrite=json_dump
jread=json_load
jexport=json_export

if __name__=='__main__':
    o={'1':1, 'a':'a你好', 'b':u'a你好'}
    print o
    print jencode(o)
    print jdecode(jencode(o))
    print jdecode('{"1":1}')
    jwrite(o, 'test.json')
    print jread('test.json')
    
    s=jexport(o)
    print s
    s=s.encode('utf8')
    print repr(s)
    
    s=jexport(o, 1)
    print s
    s=s.encode('gbk')
    print repr(s)
    
    # s=u'a你好'
    # print s, repr(s)
    # s=s.decode('utf8')
    # print s, repr(s)
    # s=s.decode('utf8')
    # print s, repr(s)
    
    

