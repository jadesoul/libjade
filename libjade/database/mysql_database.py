#coding:utf8

import MySQLdb as mysql
from database_base import database_base

def addslashes(s):
	return mysql.escape_string(s)
		
class mysql_database(database_base):
	def __init__(self, conf):
		self.conf=conf
		self.conn=None
		
	def _mysql_conn_factory(self):
		conf=self.conf
		# print conf
		# raw_input()
		conn=None
		try:
			conn=mysql.connect(**conf)
			conn.autocommit(True)
		except Exception, e:
			print 'can not connect in mysql_database._mysql_conn_factory: %s' % e
		assert conn
		return conn
		
	def connect(self):
		if self.conn: return
		self.conn=self._mysql_conn_factory()
		
	def refresh(self):
		self.close()
		self.connect()
		
	def get_conn(self):
		if not self.conn:
			self.connect()
		else:
			try:
				self.conn.ping(True)	# attempt reconnection if lost
			except Exception, e:
				warn('ping failed in mysql_database.get_conn, now try refresh the connection: %s' % e)
				self.refresh()
				
		assert self.conn
		return self.conn
			
	def close(self):
		if not self.conn: return
		
		try:
			self.conn.commit()
			self.conn.close()
		except Exception, e:
			warn('failed closing connectiton in mysql_database.re_connect: %s' % e)
			# now force close
			del self.conn
		
		self.conn=None
	
	def get_cursor(self):
		return self.get_conn().cursor()
	
	def get_dict_cursor(self):
		return self.get_conn().cursor(mysql.cursors.DictCursor)
	
	def addslashes(self, s):
		return mysql.escape_string(s)
	
if __name__=='__main__':
	pass
		
		
		
		
		
