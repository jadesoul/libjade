#coding:utf8

import smtplib 
from email.mime.text import MIMEText 
from email.mime.multipart import MIMEMultipart 
from email.mime.application import MIMEApplication 

class BaseMail: 
	def __init__(self, smtp, bSmtpAuth, sender, pwd):
		self.bSmtpAuth = bSmtpAuth 
		self.smtp   = smtp 
		self.sender = sender 
		self.pwd	= pwd 

	def _parserSend(self, sSubject, sContent, lsPlugin): 
		return sSubject, sContent, lsPlugin   
	 
	def send ( self, sSubject, sContent, lsTo, lsCc = [], lsPlugin = [] ): 
		mit = MIMEMultipart() 
		mit['from'] = self.sender 
		mit['to'] = ','.join( lsTo ) 
		if lsCc: mit['cc'] = ','.join( lsCc ) 

		codeSubject, codeContent, codePlugin = self._parserSend(sSubject, sContent, lsPlugin) 
		mit.attach( MIMEText( codeContent, 'html', 'utf-8' ) ) 
		mit['subject'] = codeSubject 
		for plugin in codePlugin: 
			mitFile = MIMEApplication( plugin['content'], ) 
			mitFile.add_header( 'content-disposition', 'attachment', filename=plugin['subject'] ) 
			mit.attach( mitFile ) 
			 
		server = smtplib.SMTP( self.smtp ) 
		#server.set_debuglevel(smtplib.SMTP.debuglevel) 
		if self.bSmtpAuth: server.docmd( "EHLO server" ) 
		server.starttls() 
		server.login(self.sender, self.pwd)
		server.sendmail(self.sender, lsTo , mit.as_string())
		server.close()

class GMail( BaseMail ): 
	def __init__( self, sender, pwd ): 
		BaseMail.__init__( self, 'smtp.gmail.com', True, sender, pwd ) 
		self.__strcode = 'utf-8' 
		 
	def _parserSend(self, sSubject, sContent, lsPlugin): 
		for i in lsPlugin: 
			i['subject'] = i['subject'].encode(self.__strcode)		  
		return sSubject.encode(self.__strcode), sContent.encode(self.__strcode), lsPlugin 

class Com63Mail( BaseMail ): 
	def __init__( self, sender, pwd ): 
		BaseMail.__init__( self, 'smtp.163.com', False, sender, pwd ) 
		self.__strcode = 'utf-8' 
		 
	def _parserSend(self, sSubject, sContent, lsPlugin): 
		for i in lsPlugin: 
			i['subject'] =  i['subject'].encode('gbk')
		return sSubject, sContent.encode(self.__strcode), lsPlugin 
	 

if __name__=="__main__" :
	sSubject = u'python3000邮件发送测试' 
	sContent = u'<font color="#FF0066">热门评论</color>' 
	lsPlugin = [{'subject' : u'附1abc.txt', 'content' : u'内容1abc'}, {'subject' : u'附2abc.txt', 'content' : u'内容2abc'}] 
	gmail = GMail( 'x@gmail.com' , 'password' ) 
	lsTo=['xxx@gmail.com']
	lsCc=[]
	gmail.send(sSubject, sContent, lsTo, lsCc, lsPlugin)
	print 'gmail send'  
	 
	sSubject = u'python3000邮件发送测试' 
	sContent = u'<font color="#FF0066">热门评论</color>' 
	lsPlugin = [{'subject' : u'附1abc.txt', 'content' : u'内容1abc'}, {'subject' : u'附2abc.txt', 'content' : u'内容2abc'}] 
	com163 = Com63Mail( 'x@163.com' , 'password' ) 
	lsTo = ['xxx@163.com'] 
	lsCc = [] 
	com163.send(sSubject, sContent, lsTo, lsCc, lsPlugin) 
	print 'com163 send'  

