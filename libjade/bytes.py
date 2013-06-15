#coding:utf8

'''
智能转换 bytes 为 kb/mb/gb/tb/pb...
'''

import math

def friendly_bytes(bytes, lst=['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB']):
	if bytes<=0: return '0 %s' % lst[0]
	i = int(math.floor(	# 舍弃小数点，取小
		math.log(bytes, 1024)	# 求对数(对数：若 a**b = N 则 b 叫做以 a 为底 N 的对数)
		))

	if i >= len(lst):
		i = len(lst) - 1
		
	if i==0:
		fmt='%d'
	else:
		fmt='%.2f'
	l=bytes/math.pow(1024, i)
	s=fmt % l
	return '%s %s' % (s, lst[i])

if __name__=='__main__':
	lst = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB']
	s=0
	for i in range(20):
		s=10*s+i
		print s, '=', friendly_bytes(s, lst)

