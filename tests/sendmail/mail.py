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

class _163MailServer(MailServer):
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
	def __init__(this, server=MailServer(), send_from='', send_to=[], subject='', content='', html=False, send_cc=[]):
		this.server=server
		
		# TODO: check email format
		assert type(send_from)==str
		this.send_from=send_from
		
		# if send to one address, send_to can be str
		if type(send_to)==str: send_to=[send_to]
		assert type(send_to) is list
		this.send_to=send_to
		
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
		send_from=this.send_from
		send_to=COMMASPACE.join(this.send_to)
		
		msg=MIMEMultipart('related')
		msg['From']=send_from
		msg['To']=send_to
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
		
		smtp.sendmail(send_from, send_to, msg.as_string())
		smtp.close()	# or smtp.quit()
	
if __name__=='__main__':
	# mail=Mail(GMailServer('wslgb2006', ''), 'wslgb2006@gmail.com', 'wslgb2006@gmail.com', '一个a email from me<h1>hello, 测试2</h1>', 'i send this email by code你好<h1>hello, 测试2</h1>', 1)
	mail=Mail(_163MailServer('wslgb2006', ''), 'wslgb2006@163.com', 'wslgb2006@163.com', '一个a email from me<h1>hello, 测试2</h1>', 'i send this email by code你好<h1>hello, 测试2</h1>', 1)
	# mail=Mail(QQMailServer('wslgb2006', ''), 'wslgb2006@qq.com', 'wslgb2006@163.com', '一个a email from me', 'i send this email by code你好')
	mail.attach(r'E:\svnprojects-linux\edusns_proj\edusns_swift_dev\data\test\b.gif')
	mail.attach(r'E:\svnprojects-linux\edusns_proj\edusns_swift_dev\data\test\test.txt')
	mail.attach(r'E:\svnprojects-linux\edusns_proj\edusns_swift_dev\data\test\test.txt')
	mail.send()

