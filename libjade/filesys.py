#coding:utf8

import os
import shutil

from os import listdir, getcwd as cwd, chdir as cd
# from os import readlink
from time import sleep
from os.path import split as splitdir, splitext, join, dirname, isfile, islink, isdir, exists

#note that we can use join(a, *p)
def joins(parent, subs):
	for i in subs.split('/'):
		parent=join(parent, i)
	return parent
	
def listall(root='.'):
	return [join(root, i) for i in listdir(root)]
	
def listfiles(root='.'):
	return filter(isfile, listall(root))
	
def listdirs(root='.'):
	return filter(isdir, listall(root))
	
def listlinks(root='.'):
	return filter(islink, listall(root))
	
def split(fullpath):
	dirpath, filename=splitdir(fullpath)
	name, ext=splitext(filename)
	return fullpath, dirpath, filename, name, ext
	# return fp, dp, fn, name, ext

def fread(path, mode='r'):
	f=open(path, mode)
	s=f.read()
	f.close()
	return s
	
def fwrite(s, path, append=False, binary=False):
	mode='w'
	if append: mode='a'
	if binary: mode+='b'
	f=open(path, mode)
	f.write(s)
	f.close()
	
	
def fappend(s, path, binary=False):
	fwrite(s, path, True, binary)
	
def fsize(fn):
	return os.path.getsize(fn)

def cp(src, dst):
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
		else: raise Exception('bad dst')
	if not isdir(src) or src=='/': raise Exception('bad src')
	
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
	
def mv(src, dst):
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
		
def rm(dp):
	if not exists(dp): return
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
	sleep(0.01)
	os.rmdir(dp)
	
def md(dp):
	if exists(dp): raise Exception('already exists %s' % dp)
	os.mkdir(dp)
	
def mds(dp):
	os.makedirs(dp)
	
def rlistfiles(pth):
	all=[]
	for root, dirs, files in os.walk(pth):
		for rp in files:
			fp=join(root, rp)
			all.append(fp)
	return all
	
def rlistdirs(pth):
	all=[]
	for root, dirs, files in os.walk(pth):
		all.append(root)
	return all
	
def clonedirs(src, dst):
	mds(dst)
	for root, dirs, files in os.walk(src):
		if not dirs: continue
		assert root.startswith(src)
		rp=root[len(src):]
		if rp and (rp[0]=='\\' or rp[0]=='/'): rp=rp[1:]
		rp=join(dst, rp)
		for d in dirs:
			dp=join(rp, d)
			print dp
			md(dp)
			
def getstat(fp):
	'''
	get the stat info of a file path
	'''
	info=os.stat(fp)
	return info.st_size, info.st_atime, info.st_mtime, info.st_ctime
	
def fatime(fp):
	return os.path.getatime(fp)
	
def fmtime(fp):
	return os.path.getmtime(fp)
	
def fctime(fp):
	return os.path.getctime(fp)