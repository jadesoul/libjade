#coding:utf8

import os
import shutil

from os import listdir, getcwd as cwd, chdir as cd
# from os import readlink
from time import sleep
from os.path import split as splitdir, splitext, join, dirname, isfile, islink, isdir, exists

def list_all_items(root='.'):
    '''list everything in the dir'''
    return [join(root, i) for i in listdir(root)]
    
def list_all_files(root='.'):
    return filter(isfile, listall(root))
    
def list_all_dirs(root='.'):
    return filter(isdir, listall(root))
    
def list_all_links(root='.'):
    return filter(islink, listall(root))
    
def split_path(fullpath):
    '''
    split a path into 5 parts: 
        fullpath, dirpath, filename, name, ext
    usage:
        fp, dp, fn, name, ext=split(fp)
    '''
    dirpath, filename=splitdir(fullpath)
    name, ext=splitext(filename)
    return fullpath, dirpath, filename, name, ext

def file_read(path, binary=False):
    mode='r'
    if binary: mode+='b'
    f=open(path, mode)
    s=f.read()
    f.close()
    return s
    
def file_write(s, path, append=False, binary=False):
    mode='w'
    if append: mode='a'
    if binary: mode+='b'
    f=open(path, mode)
    f.write(s)
    f.close()
    
def file_append(s, path, binary=False):
    fwrite(s, path, True, binary)
    
def file_size(fn):
    return os.path.getsize(fn)

def file_copy(src, dst):
    if src==dst: return
    if not exists(src): raise Exception('src not exists')
    if isfile(src):
        if isfile(dst):
            # print 'override file:', src, '->', dst
            # print '.',
            shutil.copy2(src, dst)
            return
        elif isdir(dst):
            # print 'copy file into dir:', src, '->', dst
            # print '.',
            shutil.copy2(src, dst)
            return
        elif not exists(dst):
            # print 'copy file:', src, '->', dst
            # print '.',
            shutil.copy2(src, dst)
            return
        else: raise Exception('bad dst') # TODO: maybe dst is link 
    if not isdir(src) or src=='/': raise Exception('bad src') # TODO: maybe dst is link 
    
    spth, sname=splitdir(src)
    if sname=='': spth, sname=splitdir(spth)
    if sname=='': raise Exception('bad sname')
    if not exists(dst):
        # print 'makedirs:', dst
        # print '@',
        os.makedirs(dst)
    elif isdir(dst):
        dst=join(dst, sname)
        if not exists(dst):
            # print 'mkdir:', dst
            # print '#',
            os.mkdir(dst)
        elif isdir(dst):
            # print 'dir exists:', dst
            pass
        else:
            raise Exception('bad dst2')
    else:
        raise Exception('src is dir but dst is file or link')
        
    for fp in listall(src):
        cp(fp, dst)
    
def file_move(src, dst):
    if src==dst: return
    if not exists(src): raise Exception('src not exists')
    spth, sname=splitdir(src)
    if sname=='': spth, sname=splitdir(spth)
    if sname=='': raise Exception('bad src')
    
    dpth, dname=splitdir(dst)
    if dname=='': dpth, dname=splitdir(dpth)
    
    if spth==dpth:
        # print 'rename:', sname, dname
        os.rename(src, dst)
    else:
        cp(src, dst)
        rm(src)
        
def file_remove(dp):
    # if not exists(dp): return
    if isfile(dp):
        # print 'del file:', dp
        os.remove(dp)
        return
    elif islink(dp):
        # print 'del link:', dp
        os.remove(dp)
        return
    elif not isdir(dp): raise Exception('bad dp')
    for fp in listall(dp):
        rm(fp)
    # print 'rm dir:', dp
    sleep(0.01) # wait for the system call to finish
    os.rmdir(dp)

def make_dir(dp):
    # if exists(dp): raise Exception('already exists %s' % dp)
    os.mkdir(dp)
    
def make_dirs(dp):
    os.makedirs(dp)
    
def recursively_list_files(pth):
    all=[]
    for root, dirs, files in os.walk(pth):
        for fn in files:
            fp=join(root, fn)
            all.append(fp)
    return all

def recursively_list_dirs(pth):
    all=[]
    for root, dirs, files in os.walk(pth):
        all.append(root)
    return all

def copy_dirs_structure(src, dst):
    mds(dst)
    for root, dirs, files in os.walk(src):
        if not dirs: continue
        assert root.startswith(src)
        rp=root[len(src):]
        if rp and (rp[0]=='\\' or rp[0]=='/'): rp=rp[1:]
        rp=join(dst, rp)
        for d in dirs:
            dp=join(rp, d)
            # print dp
            md(dp)

def file_status(fp):
    '''
    get the status information of a file path
    '''
    info=os.stat(fp)
    return info.st_size, info.st_atime, info.st_mtime, info.st_ctime
    
def file_access_time(fp):
    '''get the access time of a file'''
    return os.path.getatime(fp)
    
def file_modified_time(fp):
    '''get the modified time of a file'''
    return os.path.getmtime(fp)
    
def file_created_time(fp):
    '''get the created time of a file'''
    return os.path.getctime(fp)
    
# some aliases
split=split_path

fread=file_read
fwrite=file_write
fappend=file_append
fsize=file_size
fatime=file_access_time
fmtime=file_modified_time
fctime=file_created_time

listall=list_all_items
listfiles=list_all_files
listdirs=list_all_dirs
listlinks=list_all_links

cp=file_copy
mv=file_move
rm=file_remove
md=make_dir
mds=make_dirs
rlistfiles=recursively_list_files
rlistdirs=recursively_list_dirs
clonedirs=copy_dirs_structure

if __name__=='__main__':
    print split_path(r'E:\svnprojects-local\libjade\libjade\filesys.py')