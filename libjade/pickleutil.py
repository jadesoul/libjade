#coding:utf8

from utils import *
from filesys import *

# import pickle # slower
import cPickle as pickle # faster

def pickle_encode(obj):
    return pickle.dumps(obj)

def pickle_decode(s):
    return pickle.loads(s)
    
def pickle_dump(obj, fp):
    with open(fp, 'wb') as f:
        pickle.dump(obj, f)
	
def pickle_load(fp):
    with open(fp, 'rb') as f:
        obj=pickle.load(f)
    return obj
    
# some aliases
pencode=pickle_encode
pdecode=pickle_decode
pwrite=pickle_dump
pread=pickle_load

if __name__=='__main__':
    s='\x17\x00\x01'
    o=pencode(s)
    print s, type(s)
    print o, type(o)
    print pdecode(o)
    print pwrite(o, 'test.pkl')
    print pwrite([1, 2], 'test.pkl')
    print pread('test.pkl')

