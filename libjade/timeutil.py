#coding:utf8

import datetime, time

from time import sleep

global_time_seeds={}


'''
usage:
    time_gap(1)
    ...code...
    print time_gap(1)
    print time_gap(1, 'now')
    print time_gap(1, reset=False)
'''

def time_init(seed=0):
    global global_time_seeds
    global_time_seeds[seed]=time.time()

def time_gap(msg=None, seed=0, reset=True):
    global global_time_seeds
    now=time.time()
    if not seed in global_time_seeds:
        time_init(seed)
        return 0
    else:
        last=global_time_seeds[seed]
        if reset:
            global_time_seeds[seed]=now
        if not msg:
            return '%0.3fs' % (now-last)
        else:
            return '%s: %0.3fs' % (msg, now-last)
        
def time_diff(seed1, seed2):
    global global_time_seeds
    return global_time_seeds[seed2]-global_time_seeds[seed1]
    
def time_elapse(seed=0):
    global global_time_seeds
    now=time.time()
    last=global_time_seeds[seed]
    return now-last
    
def time_update(seed=0):
    global global_time_seeds
    global_time_seeds[seed]=time.time()
    
def now():
    return datetime.datetime.now()
    
def nowfn():
    return str(now()).replace(' ', '_').replace('.', '_').replace(':', '-')
    
    
if __name__=='__main__':
    print nowfn()
    time_init()
    print 1
    print time_gap('aa')

