#coding:utf8
import os,sys

# global definition
hex_chars = [str(x) for x in range(10)] + [chr(x) for x in range(ord('a'),ord('a')+6)]

# bin2dec
def bin2dec(string_num):
	return str(int(string_num, 2))

# hex2dec
def hex2dec(string_num):
	return str(int(string_num.lower(), 16))

# dec2bin
def dec2bin(string_num):
	num = int(string_num)
	mid = []
	while True:
		if num == 0: break
		num, rem = divmod(num, 2)
		mid.append(hex_chars[rem])

	return ''.join([str(x) for x in mid[::-1]])

# dec2oct
def dec2oct(string_num):
	num = int(string_num)
	mid = []
	while True:
		if num == 0: break
		num, rem = divmod(num, 8)
		mid.append(hex_chars[rem])

	return ''.join([str(x) for x in mid[::-1]])
	
# dec2hex
def dec2hex(string_num):
	num = int(string_num)
	mid = []
	while True:
		if num == 0: break
		num, rem = divmod(num, 16)
		mid.append(hex_chars[rem])

	return ''.join([str(x) for x in mid[::-1]])

# hex2bin
def hex2bin(string_num):
	return dec2bin(hex2dec(string_num.lower()))

# bin2hex
def bin2hex(string_num):
	return dec2hex(bin2dec(string_num))

# hex string to binary bytes
def hex2bytes(hexstr):
	if len(hexstr)%2!=0: hexstr='0'+hexstr
	bytes=[]
	for i in xrange(0, len(hexstr), 2):
		num=int(hexstr[i:i+2], 16)
		byte=chr(num)
		bytes.append(byte)
	return ''.join(bytes)
	
# binary bytes to hex string
def bytes2hex(bytes):
	rets=[]
	for byte in bytes:
		num=ord(byte)
		hex='%02x' % num
		assert len(hex)==2
		rets.append(hex)
	return ''.join(rets)
	
secret_key=0xabcd9e7c8de5847a;
def encode_id(i):
	return i ^ 0xabcd9e7c8de5847a
	
if __name__=='__main__':
	# print dec2hex('257')
	# print dec2hex('10')
	# print dec2hex('11')
	# print dec2hex('17')
	# print dec2hex('18')
	# print repr(hex2bytes('f7ce3d7d44f3342107d884bfa90c966a498a75f314a645671bc79a118df385d0d9948484'))
	# print repr(hex2bytes('EEFF78'))
	print bytes2hex('\xee\xff\x78')
	# print bytes2hex('\xee\xffx')
	# print repr(hex2bytes('a94a8fe5ccb19ba61c4c873d391e987982fbbd3'))
	for i in range(10):
		print i, encode_id(i)