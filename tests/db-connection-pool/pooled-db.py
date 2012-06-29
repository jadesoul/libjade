#coding:utf8

import threading,time,datetime, MySQLdb, DBUtils
from DBUtils.PooledDB import PooledDB

pool = PooledDB(MySQLdb,100,50,100,490,False,
	host='localhost',user='root',passwd='gbsoft',db='mysql',
	charset='utf8')

class MyThread(threading.Thread, object):
	
	def __init__(self,threadName):
		self.conn = pool.connection()
		threading.Thread.__init__(self,name=threadName)

	def run(self):
		cursor=self.conn.cursor()
		print "hello--->",self.getName()
		time.sleep(10)  
	
	def __del__(self):
		self.conn.close()  
		self.conn = None   

if __name__=='__main__':
	for i in range(100):  
		obj = MyThread(str(i))  
		#obj.start() 


