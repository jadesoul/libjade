#coding:utf8
	
def freqdist(lst):
	d={}
	for i in lst:
		if not i in d:
			d[i]=1
		else:
			d[i]+=1
	return d
	
list2dict=freqdist

def keydist(dct):
	d={}
	for k in dct:
		v=dct[k]
		if not v in d:
			d[v]=[]
		d[v].append(k)
	return d

dictkey2dict=keydist

if __name__=='__main__':
	pass

