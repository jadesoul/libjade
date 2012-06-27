#coding:utf8

import struct

def unicode2bytes(us, outstr=True):
	bytes=[]
	for i in us:
		code=ord(i)
		assert code<65536
		if code<256:
			bytes.append(struct.pack('B', 0))
			bytes.append(struct.pack('B', code))
		else:
			high=code / 256
			low=code % 256
			# print high, low
			bytes.append(struct.pack('B', high))
			bytes.append(struct.pack('B', low))
	return ''.join(bytes) if outstr else bytes
			
def bytes2unicode(bytes, outstr=True):
	us=[]
	for i in range(len(bytes)/2):
		high=struct.unpack('B', bytes[i*2])[0]
		low=struct.unpack('B', bytes[i*2+1])[0]
		s='u"\\u%.2x%.2x"' % (high, low)
		us.append(eval(s))
	return ''.join(us) if outstr else us

if __name__=='__main__':
	pass

