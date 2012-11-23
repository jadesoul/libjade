#coding:utf8

import smtplib
import mimetypes
import email
from email.mime.text import MIMEText 
from email.MIMEImage import MIMEImage
from email.mime.multipart import MIMEMultipart 
from email.mime.application import MIMEApplication 
from email.mime.base import MIMEBase
 
# python 2.3.*: email.Utils email.Encoders
from email.utils import COMMASPACE,formatdate
from email import encoders

import os

class MailServer:
	def __init__(this, host='', port=25, user='', passwd='', encoding='utf8', auth=False):
		this.host=host
		this.port=port
		this.user=user
		this.passwd=passwd
		this.encoding=encoding
		this.auth=auth
		
class GMailServer(MailServer):
	def __init__(this, sender, passwd):
		MailServer.__init__(this, 
			host='smtp.gmail.com',
			port=25,
			user=sender,
			passwd=passwd,
			encoding='utf8',
			auth=True
		)

class Com163MailServer(MailServer):
	def __init__(this, sender, passwd):
		MailServer.__init__(this, 
			host='smtp.163.com',
			port=25,
			user=sender,
			passwd=passwd,
			# encoding='gbk',
			encoding='utf8',
			auth=False
		)
		
class QQMailServer(MailServer):
	def __init__(this, sender, passwd):
		MailServer.__init__(this, 
			host='smtp.qq.com',
			port=25,
			user=sender,
			passwd=passwd,
			# encoding='gbk',
			encoding='utf8',
			auth=False
		)
		
class Mail(object):
	def __init__(this, server=MailServer(), from_addr='', to_addrs=[], subject='', content='', html=False, send_cc=[]):
		this.server=server
		
		# TODO: check email format
		assert type(from_addr)==str
		this.from_addr=from_addr
		
		# if send to one address, to_addrs can be str
		if type(to_addrs)==str: to_addrs=[to_addrs]
		assert type(to_addrs) is list
		this.to_addrs=to_addrs
		
		# if cc to one address, send_cc can be str
		if type(send_cc)==str: send_cc=[send_cc]
		assert type(send_cc) is list
		this.send_cc=send_cc
		
		this.subject=subject
		
		# the content to send
		this.content=content
		
		# specify if the format of the content
		# is html or text
		this.html=html
		
		this.attachments=[]	# path of the attached files
		
	def attach(this, fp):
		this.attachments.append(fp)
			
	def send(this):		
		msg=MIMEMultipart('related')
		msg['From']=this.from_addr
		msg['To']=COMMASPACE.join(this.to_addrs)
		msg['Subject']=this.subject
		msg['Date']=formatdate(localtime=True) 
		msg.preamble='This is a multi-part message in MIME format.'
		
		alt=MIMEMultipart('alternative')
		msg.attach(alt)
	
		# for content
		alt.attach(MIMEText(this.content, 'html' if this.html else 'plain', this.server.encoding))
		
		# for attachments
		for fp in this.attachments:
			part=MIMEBase('application', 'octet-stream')
			f=open(fp, 'rb')
			part.set_payload(f.read())
			f.close()
			encoders.encode_base64(part) 
			part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(fp)) 
			msg.attach(part)
		
		# begin send mail
		smtp=smtplib.SMTP(this.server.host)
		smtp.set_debuglevel(1)	# for debug
		if this.server.auth:
			smtp.docmd('EHLO server') 
			smtp.starttls()
		smtp.login(this.server.user, this.server.passwd)
		
		smtp.sendmail(this.from_addr, this.to_addrs, msg.as_string())
		smtp.close()	# or smtp.quit()
	
if __name__=='__main__':
	# mail=Mail(GMailServer('asdasdasd', ''), 'asdasdasd@gmail.com', 'asdasdasd@gmail.com', '一个a email from me<h1>hello, 测试2</h1>', 'i send this email by code你好<h1>hello, 测试2</h1>', 1)
	mail=Mail(Com163MailServer('asdasdasd', ''), 'asdasdasd@163.com', ['hokix@live.com', 'asdasdasd@163.com'], 'a email from me<h1>hello, 你好</h1>', 'i send this email by my program 你好<h1>hello, 测试2</h1><img src="https://its.pku.edu.cn/Pic_Files/v2/pku_title.jpg"/>', 1)
	# mail=Mail(QQMailServer('asdasdasd', ''), 'asdasdasd@qq.com', 'asdasdasd@163.com', '一个a email from me', 'i send this email by code你好')
	mail.attach(ur'G:\照片\jadesoul.jpg')
	mail.send()

