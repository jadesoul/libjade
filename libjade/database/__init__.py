#coding:utf8

from sqlite_database import sqlite_database
from mysql_database import addslashes, mysql_database
from pooled_mysql_database import pooled_mysql_database

if __name__=='__main__':

	def sqlite_database_conf():
		file=''
		return locals()
		
	def mysql_database_conf():
		host='localhost'
		user='root'
		passwd='gbsoft'
		db='mysql'
		# port=3306
		charset='utf8'
		# unix_socket=''
		return locals()
		
	def database_pooling_conf():
		mincached=10
		maxcached=150
		maxconnections=150
		# maxshared=0
		# blocking=False
		# maxusage=None
		# setsession=None
		# reset=True
		# failures=None
		# ping=1
		return locals()
			
	def get_sqlite_db():
		return sqlite_database(sqlite_database_conf())
		
	def get_mysql_db():
		return mysql_database(mysql_database_conf())
		
	def get_pooled_mysql_db():
		return pooled_mysql_database(mysql_database_conf(), database_pooling_conf())
		
		
	def test_pooled_db():
		mysql_conf=mysql_database_conf()
		pool_conf=database_pooling_conf()
		pooled_db=pooled_mysql_database(mysql_conf, pool_conf)
		print pooled_db
		
		db=pooled_db
		for i in xrange(1):
			# if i%100==0: print i
			print db.conf
			print db.conn
			print db.addslashes('''a'b&p"m/ss''')
			print db.get_cursor()
			print db.conn
			
			print len(db.table('objects'))
			print len(db.table_dict('objects'))
			print db.one('select hash from objects')
			print db.first('select hash from objects')
			print db.one_dict('select stored_in_swift from objects')
			print len(db.all('select * from objects'))
			print len(db.all_dict('select * from objects'))
		
		pool=db.pool
		print pool
		c=pool.connection()
		print c
		o={}
		for i in range(10):
			x=db.get_conn()
			print i, x
			o[i]=x

	def test_pooled_db_multi_thread():
		pass
		
	

	db=get_sqlite_db()
	print db
	
	db=get_mysql_db()
	print db
	
	db=get_pooled_mysql_db()
	print db
	
	db_conf=mysql_database_conf()
	pool_conf=database_pooling_conf()
	
	db1=mysql_database(db_conf)
	db=mysql_database(db_conf)
	for i in xrange(1):
		# if i%100==0: print i
		print db.conf
		print db.conn
		print db.addslashes('''a'b&p"m/ss''')
		print db.get_cursor()
		print db.conn
		
		print len(db.table('db'))
		print len(db.table_dict('db'))
		print db.one('select db from db')
		print db.first('select db from db')
		print db.one_dict('select db from db')
		print len(db.all('select * from db'))
		print len(db.all_dict('select * from db'))
		
		
		print 'close db'
		db.close()
		print db.conn
		print db.get_conn()
		print db.get_conn()
		print db.get_dict_cursor()
		print db.conn
		print db.refresh()
		print db.conn
		
		print len(db.table('db'))
		print len(db.table_dict('db'))
		print db.one('select db from db')
		print db.first('select db from db')
		print db.one_dict('select db from db')
		print len(db.all('select * from db'))
		print len(db.all_dict('select * from db'))
		
