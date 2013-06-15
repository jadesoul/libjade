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

def sort_table_by_colume(table, col_id, reverse=False):
	return sorted(table, key=lambda x: x[col_id],  reverse=reverse)
	
#utils
def unique(lst):
	return list(set(lst))
	
def reversed(lst):
	return lst[::-1]


def heap_sort(A):
	def heapify(A):
		start = (len(A) - 2) / 2
		while start >= 0:
			sift_down(A, start, len(A) - 1)
			start -= 1

	def sift_down(A, start, end):
		root = start
		while root * 2 + 1 <= end:
			child = root * 2 + 1
			if child + 1 <= end and A[child] < A[child + 1]:
				child += 1
			if child <= end and A[root] < A[child]:
				A[root], A[child] = A[child], A[root]
				root = child
			else:
				return

	heapify(A)
	end = len(A) - 1
	while end > 0:
		A[end], A[0] = A[0], A[end]
		sift_down(A, 0, end - 1)
		end -= 1

if __name__ == '__main__':
	from datetime import datetime
	N=10000
	
	start=datetime.now()
	for i in xrange(N):
		T = [13, 14, 94, 33, 82, 25, 59, 94, 65, 23, 45, 27, 73, 25, 39, 10] 
		heap_sort(T)
		# print T
	print datetime.now()-start
		
	start=datetime.now()
	for i in xrange(N):
		T = [13, 14, 94, 33, 82, 25, 59, 94, 65, 23, 45, 27, 73, 25, 39, 10] 
		R=sorted(T)
		# print R
	print datetime.now()-start

	print sort_table_by_colume([(1, 2), (2, 1)], 0)
	print sort_table_by_colume([(1, 2), (2, 1)], 0, 1)
	print sort_table_by_colume([(1, 2), (2, 1)], 1)
	print sort_table_by_colume([(1, 2), (2, 1)], 1, 1)
