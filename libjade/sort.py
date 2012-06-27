#coding:utf8

#sort dict
def vsorted(d):
	return sorted(d.items(), key=lambda x: x[1])

def rvsorted(d):
	return sorted(d.items(), key=lambda x: x[1],  reverse=True)
	
def ksorted(d):
	return sorted(d.items(), key=lambda x: x[0])

def rksorted(d):
	return sorted(d.items(), key=lambda x: x[0],  reverse=True)

#utils
def unique(lst):
	return list(set(lst))
	
def reversed(lst):
	return lst[::-1]

if __name__=='__main__':
	pass

