#coding:utf8

import MySQLdb as _mysql
import sqlite3 as _sqllite
#import pymssql as _mssql

from DBUtils.PooledDB import PooledDB as pooled

class db_base:
	self.conn=None
	self.cursor=None

	def connect(self):
		'connect to the host'
		raise NotImplementedError
	
	def close(self):
		'close the connection'
		raise NotImplementedError

	def refresh(self):
		self.close()
		self.connect()
	
	def get_connection(self):
		'a proxy to get connection, useful for pooling connection implementation'
		return self.conn	
	
	def get_cursor(self):
		'get nomal cursor, fields accessed by number, faster'
		raise NotImplementedError
	
	def get_dict_cursor(self):
		'get dict cursor, fields accessed by name, slower'
		raise NotImplementedError

	def run(self, sql):
		cursor=self.get_cursor()
		cursor.execute(sql)
		rc=0
		if sql.strip()[:6].lower()=='insert': 
			try: rc=self.conn.insert_id()
			except: rc='not support insert_id()'
		else: rc=cursor.rowcount
		cursor.close()
		return rc
	
	def insert(self, table, cols, vals):
		'insert into table cols vals'
		sql="insert into %s %s values %s" % (table, cols, vals)
		return self.run(sql)
		
	def update(self, table, set, where):
		'update table set ... where ...'
		sql="update %s set %s where %s" % (table, set, where)
		return self.run(sql)
	
	def delete(self, table, where):
		'delete from table where ...'
		sql="delete from %s where %s" % (table, where)
		return self.run(sql)
	
	def select(self, cols, table, where):
		'select cols from table where ...'
		sql="select %s from %s where %s" % (cols, table, where)
		return self.all(sql)
	
	def drop(self, table):
		'drop table'
		self.run("drop table "+table)
	
	def table(self, table):
		'select * from table'
		return self.all("select * from "+table)
	
	def count(self, sql):
		'return the count influenced by the opertion sql'
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
		cursor.close ()
		return rows
	
	def all_dict(self, sql):
		'''return all record, accessed by col name'''
		cursor=self.get_dict_cursor()
		cursor.execute(sql)
		rows=cursor.fetchall()
		cursor.close()
		return rows
	
class pooled_base:
	
	self.pool=None
	self.max_conn_cnt=0

	def init_pool(self, **kwargs):
		raise NotImplementedError 

class sqllite(db_base):
	'''this is the sqllite database'''
	
	self.file=None

	def __init__(self, file=':memory:'):
		'''
		Constructor, file tell the path of the sqllite db file, 
		default, use memory if not given
		'''
		self.file=file

	def connect(self):
		'connect to the file'
		if self.conn: return
		self.conn=_sqlite.connect(self.file)
	
	def close(self):
		'close the connection'
		if not self.conn: return
		self.conn.commit()
		self.conn.close()
		self.conn=None

	def get_cursor(self):
		'get nomal cursor, fields accessed by number, faster'
		self.check_conn()
		return self.conn.cursor()
	
	def get_dict_cursor(self):
		'get dict cursor, fields accessed by name, slower'
		'not implemented yet'
		raise NotImplementedError 	

	
class mysql(base):
	'mysql database'

	self.host='localhost'
	self.port=3306
	self.user='root'
	self.pwd=''
	self.dbname='test'
	self.charset='utf8'

	def __init__(self, host='localhost', user='root', pwd='', dbname='test', port=3306, charset='utf8'):
		'Constructor'
		self.host=host
		self.port=port
		self.user=user
		self.pwd=pwd
		self.dbname=dbname
		self.charset=charset
		
	def connect(self):
		'connect to the host'
		if self.conn: return
		try:
			self.conn=_mysql.connect(host = self.host, user = self.user, passwd = self.pwd, db = self.dbname)
			self.use_charset(self.charset)
			self.use_db(self.dbname)
		except _mysql.Error, e:
			print "mysql error %d: %s" % (e.args[0], e.args[1])
			raise e
		
	def close(self):
		if not self.conn: return
		self.conn.commit()
		self.conn.close()
		self.conn=None
			
		
	def get_cursor(self):
		self.check_conn()
		return self.conn.cursor()
	
	def get_dict_cursor(self):
		self.check_conn()
		return self.conn.cursor(MySQLdb.cursors.DictCursor)
	
	#--------------------------------------------------
	#	db specific functions
	#--------------------------------------------------
	
	def get_version(self):
		cursor = self.get_cursor()
		cursor.execute("SELECT VERSION()")
		row = cursor.fetchone()
		v="server version:"+ row[0]
		cursor.close()
		return v

	def use_charset(self, charset):
		return self.run("SET NAMES '"+charset+"'");
		
	def use_db(self, dbname):
		if dbname!=self.dbname:
			self.dbname=dbname
			return self.run("use "+self.dbname)
	
	def drop_db(self, dbname):
		return self.run("drop database "+dbname)
		
	def addslashes(self, s):
		return MySQLdb.escape_string(s)
		
def get_db(dburl="mysql://root:gbsoft@localhost:3306/dbname"):
	'''
	db generator
	'''
	s=dburl
	pos=dburl.find("://")
	if pos==-1: raise Exception("bad dburl: "+dburl)
	type=s[:pos]
	r=s[pos+3:]
	if type=='access' or type=='sqllite':
		file=r
	else:
		r=r.split("@")
		if len(r)!=2: raise Exception("bad dburl: "+dburl)
		l=r[0].split(":")
		if len(l)!=2: raise Exception("bad dburl: "+dburl)
		user=l[0]
		pwd=l[1]
		t=r[1].split("/")
		if len(t)!=2: raise Exception("bad dburl: "+dburl)
		db=t[1]
		r=t[0].split(":")
		host=r[0]
		port=int(r[1]) if len(r)==2 else None
	if type=="mysql":
		return mysql(host, user, pwd, db, port)
	elif type=="sqlserver":
		import sqlserver
		return sqlserver.sqlserver(host, user, pwd, db)
	elif type=="sqllite":
		import sqllite
		return sqllite.sqllite(file)
	elif type=="access":
		import access
		return access.access(file)
	elif type=="postprogress":
		return None
	else:
		raise Exception("bad db type")

def get_pooled_db():
	pass

if __name__=='__main__':
#	conn = sqlite3.connect('/tmp/example')
	db=sqllite(r"sqllite.db")
	print db.run('drop table gb')
	print db.run('create table gb( id int, name varchar(10))')
	print db.insert('gb', '(id, name)', '(1, "jadesoul")')
	print db.table('gb')
