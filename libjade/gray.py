#coding:utf8

'''
格雷码生成器

格雷码的编码与二进制的编码存在十分有趣的对应关系，每一个十进制数对应的格雷码相对于上一个格雷码发生变化的那一位的位置正好是十进制数对应的二进制形式的最后一个1的位置
'''

def get_last_1_pos(i):
	'''
	获取十进制数i的二进制形式的最后一个1相对于二进制末尾的位置
	
	如果i<=0则返回-1
	'''
	if i<=0: return -1
	pos=0
	while i%2==0:
		i/=2
		pos+=1
	return pos
		
def gray_code_generator(N):
	'''
	二进制格雷码生成器
	N为编码宽度，也就是有多少位
	返回为数组，每一位为0或1
	'''
	assert N>0
	i=0
	A=[0]*N
	while 1:
		yield A
		i+=1
		p=get_last_1_pos(i)
		if p==N:
			break
		# print A, p, i, T
		A[p] ^= 1	#取反等价于异或上1
		
if __name__=='__main__':
	for i in gray_code_generator(2):
		print i

