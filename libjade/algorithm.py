#coding:utf8

import math

def max_sub_seq_sum(l):
	begin=0
	now_begin=0
	n=len(l)
	end=0
	max_sum=0
	b=0
	for i in range(n):
		if b>0:
			b+=l[i]
		else:
			b=l[i]
			now_begin=i
		if b>max_sum:
			max_sum=b
			begin=now_begin
			end=i
			
	return max_sum, begin, end

if __name__=="__main__":
	print max_sub_seq_sum([-2, 11, -4, 13, -5, -2])	