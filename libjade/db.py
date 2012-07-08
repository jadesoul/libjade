#coding:utf8

from os import system as run

# for MySQL
try:
	import MySQLdb as _mysql
except:
	run('sudo apt-get install pip-install; sudo pip install MySQLdb')
	import MySQLdb as _mysql

# for SQLite
import sqlite3 as _sqlite

# for MSSQL Server
# import pymssql as _mssql

# for pooling db
try:
	from DBUtils.PooledDB import PooledDB as pooled
except:
	run('sudo apt-get install pip-install; sudo pip install DBUtils')
	from DBUtils.PooledDB import PooledDB as pooled

# for parsing db url
from urlparse import urlparse as parse

def addslashes(s):
	return _mysql.escape_string(s)
		
class db_base:
	def __init__(self):
		self.conn=0
		self.cursor=0
		
	def connect(self):
		'''connect to the host'''
		raise NotImplementedError
	
	def close(self):
		'''close the connection'''
		raise NotImplementedError

	def refresh(self):
		self.close()
		self.connect()
	
	def get_conn(self):
		'''a proxy to get connection, useful for pooling connection implementation
		the default behavior is to check the connection'''
		if not self.conn: self.connect()
		return self.conn
	
	def get_cursor(self):
		'''get nomal cursor, fields accessed by number, faster'''
		raise NotImplementedError
	
	def get_dict_cursor(self):
		'''get dict cursor, fields accessed by name, slower'''
		raise NotImplementedError

	# def run(self, sql):
		# conn=self.get_conn()
		# cursor=conn.cursor()
		# cursor.execute(sql)
		# ret=None
		# if sql.strip()[:7].lower()=='insert ':
			# try:
				# insert_id=conn.insert_id()
				# ret=insert_id
			# except Exception, e:	#maybe is pool mode
				# try:
					# insert_id=conn._con._con.insert_id()
					# ret=insert_id
				# except Exception, e:
					# print 'got exception in run sql, %s, %s' % (type(e), e)
				
		# else: 
			# rowcnt=cursor.rowcount
			# ret=rowcnt
		# cursor.close()
		# return ret
	
	def run(self, sql):
		cursor=self.get_cursor()
		cursor.execute(sql)
		ret=None
		if sql.strip()[:7].lower()=='insert ':
			try:
				insert_id=cursor.connection.insert_id()
				ret=insert_id
			except Exception, e:
				print 'got exception in run sql, %s, %s' % (type(e), e)
		else:
			rowcnt=cursor.rowcount
			ret=rowcnt
		cursor.close()
		return ret
		
	def insert(self, table, cols, vals):
		'''insert into table cols vals'''
		sql="insert into %s %s values %s" % (table, cols, vals)
		return self.run(sql)
		
	def update(self, table, set, where):
		'''update table set ... where ...'''
		sql="update %s set %s where %s" % (table, set, where)
		return self.run(sql)
	
	def delete(self, table, where):
		'''delete from table where ...'''
		sql="delete from %s where %s" % (table, where)
		return self.run(sql)
	
	def select(self, cols, table, where):
		'''select cols from table where ...'''
		sql="select %s from %s where %s" % (cols, table, where)
		return self.all(sql)
	
	def drop(self, table):
		'''drop table'''
		self.run("drop table "+table)
	
	def table(self, table):
		'''select * from table'''
		return self.all("select * from "+table)
	
	def table_dict(self, table):
		'''select * from table'''
		return self.all_dict("select * from "+table)
		
	def count(self, sql):
		'''return the count influenced by the opertion sql'''
		return self.run(sql)
	
	def first(self, sql):
		'''return the first col value of the first row'''
		cursor=self.get_cursor()
		cursor.execute(sql)
		row=cursor.fetchone()
		cursor.close()
		return row[0]
	
	def one(self, sql):
		'''return only one row from record set, accessed by id'''
		cursor=self.get_cursor()
		cursor.execute(sql)
		row=cursor.fetchone()
		cursor.close()
		return row
		
	def one_dict(self, sql):
		'''return only one row from record set, accessed by col name'''
		cursor=self.get_dict_cursor()
		cursor.execute(sql)
		row=cursor.fetchone()
		cursor.close()
		return row
		
	def all(self, sql):
		'''return all record, accessed by id'''
		cursor=self.get_cursor()
		cursor.execute(sql)
		rows=cursor.fetchall()
		cursor.close()
		return rows
	
	def all_dict(self, sql):
		'''return all record, accessed by col name'''
		cursor=self.get_dict_cursor()
		cursor.execute(sql)
		rows=cursor.fetchall()
		cursor.close()
		return rows
	
class pooled_base:
	def __init__(self):
		self.pool=None
		
	def get_conn_from_pool(self):
		raise NotImplementedError

class sqlite(db_base):
	'''this is the sqlite database'''
	def __init__(self, file=':memory:'):
		'''Constructor, file tell the path of the sqlite db file, 
		default, use memory if not given'''
		db_base.__init__(self)
		self.file=file
		
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
		
class mysql(db_base):
	'''mysql database'''
	def __init__(self, host='localhost', user='root', passwd='', dbname='test', port=3306, charset='utf8', unix_socket=None):
		'''Constructor'''
		db_base.__init__(self)
		
		self.host=host
		self.user=user
		self.passwd=passwd
		self.dbname=dbname
		self.port=port
		self.charset=charset
		self.unix_socket=unix_socket
		
	def connect(self):
		'''connect to the host'''
		if self.conn: return
		try:
			print 'self.host=', self.host
			# print 'self.charset=', self.charset
			# print 'self.unix_socket=', self.unix_socket
			# raw_input()
			if self.unix_socket:
				self.conn=_mysql.connect(host = self.host, user = self.user, \
					passwd = self.passwd, db = self.dbname, port=self.port, \
					charset=self.charset, unix_socket=self.unix_socket)
			else:
				# print 'self.host=', self.host
				self.conn=_mysql.connect(host = self.host, user = self.user, passwd = self.passwd, db = self.dbname, port=self.port, charset=self.charset)
		except _mysql.Error, e:
			print "mysql error %s: %s" % (e.args, e.message)
			raise e
		
	def close(self):
		if not self.conn: return
		self.conn.commit()
		self.conn.close()
		self.conn=None
		
	def get_cursor(self):
		return self.get_conn().cursor()
	
	def get_dict_cursor(self):
		return self.get_conn().cursor(_mysql.cursors.DictCursor)
	
	#--------------------------------------------------
	#	db specific functions
	#--------------------------------------------------
	
	def get_version(self):
		# cursor = self.get_cursor()
		# cursor.execute("SELECT VERSION()")
		# row = cursor.fetchone()
		# v="server version:"+ row[0]
		# cursor.close()
		# return v
		return self.get_conn().get_server_info()

	def use_charset(self, charset):
		'''note: when the connection is pooled, this method may not work'''
		# return self.run("SET NAMES '"+charset+"'");
		return self.get_conn().set_character_set(charset)
		
	def use_db(self, dbname):
		'''note: when the connection is pooled, this method may not work'''
		if dbname!=self.dbname:
			self.dbname=dbname
			# return self.run("use "+dbname)
			return self.get_conn().select_db(dbname)
	
	def drop_db(self, dbname):
		return self.run("drop database "+dbname)
		
	def addslashes(self, s):
		return _mysql.escape_string(s)
		
class pooled_mysql(mysql, pooled_base):
	def __init__(self, mincached=50, maxcached=100, maxshared=0, \
			maxconnections=500, blocking=False, \
			host='localhost', user='root', passwd='', dbname='test', \
			port=3306, charset='utf8', unix_socket=None):
		'''Constructor'''
		mysql.__init__(self, host, user, passwd, dbname, port, charset, unix_socket)
		
		self.creator=_mysql
		self.mincached=mincached
		self.maxcached=maxcached
		self.maxshared=maxshared
		self.maxconnections=maxconnections
		self.blocking=blocking
		
		pooled_base.__init__(self)
		
		# init pool
		if unix_socket:
			self.pool=pooled(self.creator, self.mincached, self.maxcached, \
					self.maxshared, self.maxconnections, self.blocking, \
					host = self.host, user = self.user, passwd = self.passwd, \
					db = self.dbname, port=self.port, charset=self.charset, \
					unix_socket=self.unix_socket)
		else:
			self.pool=pooled(self.creator, self.mincached, self.maxcached, \
					self.maxshared, self.maxconnections, self.blocking, \
					host = self.host, user = self.user, passwd = self.passwd, \
					db = self.dbname, port=self.port, charset=self.charset)
					
	def get_conn_from_pool(self):
		return self.pool.connection()
		
	def get_conn(self):
		self.conn=self.get_conn_from_pool()
		return self.conn

def get_db(dburl="mysql://root:gbsoft@localhost:3306/dbname", pooled=False, unix_socket=None, charset='utf8', mincached=50, maxcached=100, maxshared=0, maxconnections=500, blocking=False):
	'''
	db generator, return a db instance from the db url
	
	db url examples:
		mysql://root:gbsoft@localhost:3306/dbname
		sqlserver://admin:gbsoft@localhost/dbname
		sqlite:///home/jadesoul/a.db
		access://E:/mydb/c.mdb
	
	only when the pooled is True, the following parameters will be considered
	'''
	info=parse(dburl)
	type=info.scheme
	
	if type=='access' or type=='sqlite':
		file=info.netloc+info.path
		if type=='sqlite': return sqlite(file)
	elif type=='mysql' or type=='sqlserver':
		host=info.hostname
		user=info.username
		passwd=info.password
		dbname=info.path[1:]
		port=info.port
		
		if type=='mysql': 
			if pooled:
				return pooled_mysql(mincached=mincached, maxcached=maxcached, maxshared=maxshared, maxconnections=maxconnections, blocking=blocking, host=host, user=user, passwd=passwd, dbname=dbname, port=port, charset=charset, unix_socket=unix_socket)
			else:
				return mysql(host=host, user=user, passwd=passwd, dbname=dbname, port=port, charset=charset, unix_socket=unix_socket)

if __name__=='__main__':
	print '-----------------------------------------------test sqlite in memory'
	db=sqlite()
	print db.run('create table gb( id int, name varchar(10))')
	print db.insert('gb', '(id, name)', '(1, "jadesoul")')
	print db.table('gb')
	print db.run('drop table gb')
	
	# print '-----------------------------------------------test sqlite in filesystem'
	# db=sqlite('/tmp/example.db')
	# print db.run('create table gb( id int, name varchar(10), primary key(id))')
	# print db.insert('gb', '(id, name)', '(1, "jadesoul")')
	# print db.table('gb')
	# print db.run('drop table gb')
	
	print '-----------------------------------------------test mysql'
	db=get_db('mysql://root:gbsoft@localhost:3306/mysql')
	print db.table('user')
	print db.table_dict('user')
	sql='select host, user from user'
	print db.all(sql)
	print db.all_dict(sql)
	print db.one(sql)
	print db.one_dict(sql)

	# print '-----------------------------------------------test pooled mysql'
	# db=get_db('mysql://root:@localhost:3306/centig_sns_filesystem', pooled=1)
	# for i in xrange(20):
		# sql='select * from vfiles where id=1'
		# print db.all(sql)
		# print db.all_dict(sql)
		# print db.one(sql)
		# print db.one_dict(sql)
	
