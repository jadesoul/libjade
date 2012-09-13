#coding:utf8

from database import *

if __name__=='__main__':
	print '-----------------------------------------------test sqlite in memory'
	db=sqlite()
	print db.run('create table gb( id int, name varchar(10))')
	print db.insert('gb', '(id, name)', '(1, "jadesoul")')
	print db.table('gb')
	print db.run('drop table gb')
	
	print '-----------------------------------------------test sqlite in filesystem'
	db=sqlite('/tmp/example.db')
	print db.run('create table gb( id int, name varchar(10), primary key(id))')
	print db.insert('gb', '(id, name)', '(1, "jadesoul")')
	print db.table('gb')
	print db.run('drop table gb')
	
	print '-----------------------------------------------test mysql'
	db=get_db('mysql://root:gbsoft@192.168.1.200:3306/mysql')
	print db.table('user')
	print db.table_dict('user')
	sql='select host, user from user'
	print db.all(sql)
	print db.all_dict(sql)
	print db.one(sql)
	print db.one_dict(sql)

	print '-----------------------------------------------test pooled mysql'
	db=get_db('mysql://root:@localhost:3306/centig_sns_filesystem', pooled=1)
	for i in xrange(20):
		sql='select * from vfiles where id=1'
		print db.all(sql)
		print db.all_dict(sql)
		print db.one(sql)
		print db.one_dict(sql)
	
	
