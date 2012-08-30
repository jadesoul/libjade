#coding:utf8

import sqlite3 as _sqlite
from database_base import database_base

class sqlite_database(database_base):
	'''this is the sqlite database'''
	def __init__(self, conf={'file': ':memory:'}):
		'''Constructor, file tell the path of the sqlite db file, 
		default, use memory if not given'''
		database_base.__init__(self)
		self.file=conf['file']
		self.conn=None
		
	def connect(self):
		'''connect to the file'''
		if self.conn: return
		
		try:
			self.conn=_sqlite.connect(self.file)
		except _sqlite.Error, e:
			print "sqlite error %s: %s" % (e.args, e.message)
			raise e
			
	def close(self):
		'close the connection'
		if not self.conn: return
		self.conn.commit()
		self.conn.close()
		self.conn=None

	def get_cursor(self):
		'''get nomal cursor, fields accessed by number, faster'''
		return self.get_conn().cursor()
	
	def get_dict_cursor(self):
		'''get dict cursor, fields accessed by name, slower
		not implemented yet'''
		raise NotImplementedError
		
if __name__=='__main__':

	print '-----------------------------------------------test sqlite in memory'
	
	db=sqlite_database()
	print db.run('create table gb( id int, name varchar(10))')
	print db.insert('gb', '(id, name)', '(1, "jadesoul")')
	print db.table('gb')
	print db.run('drop table gb')
	
	print '-----------------------------------------------test sqlite in filesystem'
	db=sqlite_database({'file': '/tmp/example.db'})
	print db.run('create table gb( id int, name varchar(10), primary key(id))')
	print db.insert('gb', '(id, name)', '(1, "jadesoul")')
	print db.table('gb')
	print db.run('drop table gb')
