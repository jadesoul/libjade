#coding:utf8

import email
import mimetypes
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
import smtplib

def sendEmail(authInfo, fromAdd, toAdd, subject, plainText, htmlText):

	strFrom=fromAdd
	strTo=', '.join(toAdd)

	server=authInfo.get('server')
	user=authInfo.get('user')
	passwd=authInfo.get('password')

	if not (server and user and passwd) :
		print 'incomplete login info, exit now'
		return

	# �趨root��Ϣ
	msgRoot=MIMEMultipart('related')
	msgRoot['Subject']=subject
	msgRoot['From']=strFrom
	msgRoot['To']=strTo
	msgRoot.preamble='This is a multi-part message in MIME format.'

	# Encapsulate the plain and HTML versions of the message body in an
	# 'alternative' part, so message agents can decide which they want to display.
	msgAlternative=MIMEMultipart('alternative')
	msgRoot.attach(msgAlternative)

	#�趨���ı���Ϣ
	msgText=MIMEText(plainText, 'plain', 'utf-8')
	msgAlternative.attach(msgText)

	#�趨HTML��Ϣ
	msgText=MIMEText(htmlText, 'html', 'utf-8')
	msgAlternative.attach(msgText)

       #�趨����ͼƬ��Ϣ
	fp=open('test.jpg', 'rb')
	msgImage=MIMEImage(fp.read())
	fp.close()
	msgImage.add_header('Content-ID', '<image1>')
	msgRoot.attach(msgImage)

       #�����ʼ�
	smtp=smtplib.SMTP()
       #�趨���Լ������������
	smtp.set_debuglevel(1)
	smtp.connect(server)
	smtp.login(user, passwd)
	smtp.sendmail(strFrom, strTo, msgRoot.as_string())
	smtp.quit()
	return

if __name__ == '__main__' :
	authInfo={}
	authInfo['server']='smtp.somehost.com'
	authInfo['user']='username'
	authInfo['password']='password'
	fromAdd='username@somehost.com'
	toAdd=['someone@somehost.com', 'other@somehost.com']
	subject='�ʼ�����'
	plainText='��������ͨ�ı�'
	htmlText='<B>HTML�ı�</B>'
	sendEmail(authInfo, fromAdd, toAdd, subject, plainText, htmlText)


