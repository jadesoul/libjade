#coding:utf8

import sys, urllib, urllib2, re, socket, urlparse
from urlparse import urlsplit, urlunsplit, urlunparse, urljoin, urldefrag
from urlnorm import norm as normalize_url
from os.path import dirname

re_host=re.compile("^(http|https|ftp)://(([\w\-]+\.)+[\w\-]+|localhost)/?")

#
def get_host_name():
	return socket.gethostname()

def get_host_ips():
	return socket.gethostbyaddr(get_host_name())[-1]

def get_host_ip():
	return get_host_ips()[0]

def get_ip_by_host(host, ex=False):
	if not ex:
		return socket.gethostbyname(host)
	else:
		return socket.gethostbyname_ex(host)

def get_real_url(url, headers={}):
	req=urllib2.Request(url)
	req.headers.update(headers)
	f=urllib2.urlopen(req)
	real_url=f.geturl()
	f.close()
	return real_url
	
def get_real_url_and_host(url, headers={}):
	req=urllib2.Request(url)
	req.headers.update(headers)
	f=urllib2.urlopen(req)
	real_url=f.geturl()
	f.close()
	real_host=req.get_host()
	return real_url, real_host
	
def get_html_by_url(url, headers={}):
	req=urllib2.Request(url)
	req.headers.update(headers)
	f=urllib2.urlopen(req)
	real_url=f.geturl()
	html=f.read()
	f.close()
	real_host=req.get_host()
	return html, real_url, real_host
	
def webopen(url, headers={}):
	# print 'DEBUG: headers=', headers
	req=urllib2.Request(url)
	req.headers.update(headers)
	# req.headers.update({})
	fsock=urllib2.urlopen(req)
	real_url=fsock.geturl()
	content_type=fsock.headers.get('content-type', '')
	if content_type: 
		pos=content_type.find(';')
		if pos!=-1: content_type=content_type[:pos].strip()
	# print 'DEBUG: content=', fsock.read()
	return real_url, content_type, fsock
	
def sockclose(fsock):
	try: fsock.close()
	except: pass
	
def sockreadonce(fsock):
	data=''
	try: data=fsock.read()
	except: sockclose(fsock)
	return data
	
def datasave(data, fp):
	f=open(fp, 'wb')
	f.write(data)
	f.close()
	
def post(url, params={}, headers={'User-agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1'}):
	req=urllib2.Request(url, urllib.urlencode(params))
	req.headers.update(headers)
	f=urllib2.urlopen(req)
	# real_url=f.geturl()
	html=f.read()
	f.close()
	# real_host=req.get_host()
	return html#, real_url, real_host
	
def post_data(url, data='', headers={'User-agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1'}):
	req=urllib2.Request(url)
	req.data=data
	req.headers.update(headers)
	f=urllib2.urlopen(req)
	# real_url=f.geturl()
	html=f.read()
	f.close()
	# real_host=req.get_host()
	return html#, real_url, real_host
	
def parse_url(url):
	'''
	usage:
		url='http://www.abc.com/a/b/c.html?a=1&b=2#tag'
		protcal, netloc, host, port, user, pwd, path, query, anchor=parse_url(url)
	'''
	p=urlsplit(url)
	return p.scheme, p.netloc, p.hostname, p.port, p.username, p.password, p.path, p.query, p.fragment
	
def get_host_by_url_v1(url):
	m=re_host.findall(url)
	if len(m)!=1: return None
	return m[0][1]
	
def get_host_by_url_v2(url):
	protcal, netloc, host, port, user, pwd, path, query, anchor=parse_url(url)
	return host

def get_host_by_url_v3(url):
	req=urllib2.Request(url)
	return req.get_host()
	
get_host_by_url=get_host_by_url_v2

def get_html_by_host(host_name):
	url="http://"+host_name
	return get_html_by_url(url)

def get_data_by_url(url):
	re = urllib2.Request(url)
	f=urllib2.urlopen(re)  
	data=f.read()
	f.close()
	return data

def save_file_from_url(fn, url, mode='wb'):
	f=open(fn, mode)
	f.write(get_data_by_url(url))
	f.close()
	
def urlencode(s):
	return urllib.quote(s)
	
def urldecode(s):
	return urllib.unquote(s)
	
def strip_url_query_str(url):
	pos=url.find('?')
	if pos!=-1: url=url[:pos]
	return url
	
def strip_url_anchor(url):
	pos=url.find('#')
	if pos!=-1: url=url[:pos]
	return url
	
def strip_url_tail(url):
	url=strip_url_query_str(url)
	return strip_url_anchor(url)
	
def get_file_type_by_url_old(url):
	url=strip_url_tail(url)
	pos=url.rfind('.')
	if pos==-1: return 'dir'
	else: ext=url[pos+1:]
	ext=ext.lower()
	if ext in 'gif png jpg jpeg pdf ps doc docx ppt pptx xls xlsx htm html shtml php jsp asp aspx py do txt rar zip 7z gz lzma rm mpeg mpg rmvb mov tex mp3 mp4 3gp avi vod m ps c cfm cpp cxx hpp java py php js sh h xml xslt xhtml'.split():
		return ext
	elif len(ext)>4 or url.count('/')==2:
		return 'dir'
	else:
		# print 'bad type:', ext, url
		return 'bad'
		
from mimetype import get_mimetype_by_ext
def get_file_type_by_url(url):
	url=strip_url_tail(url)
	if url.count('/')==2: return 'html'	# for only host
	pos=url.rfind('.')
	if pos==-1: return 'html'
	else: ext=url[pos+1:].lower()
	if not get_mimetype_by_ext(ext): return 'html'	#mime-type not exist
	return ext
	
def url_merge_dots(url):
	prefix=''
	suffix=''
	pos=url[:10].find('://')
	if pos!=-1:
		pos2=url[pos+3:].find('/')
		if pos2!=-1:
			prefix=url[:pos+3+pos2+1]
			url=url[pos+3+pos2+1:]
		else:
			return url
		
	pos3=url.find('?')
	pos4=url.find('#')
	
	if pos3!=-1 and pos4!=-1:
		if pos3<pos4:
			suffix=url[pos3:]
			url=url[:pos3]
		else:
			suffix=url[pos4:]
			url=url[:pos4]
	elif pos3!=-1 and pos4==-1:
		suffix=url[pos3:]
		url=url[:pos3]
	elif pos3==-1 and pos4!=-1:
		suffix=url[pos4:]
		url=url[:pos4]
	
	# print url
	parts=url.split('/')
	# print parts
	while '.' in parts:	
		del parts[parts.index('.')]
		# print 'del .', parts

	while '' in parts:	
		del parts[parts.index('')]
		# print 'del empty', parts
	
	len_old=len(parts)
	while '..' in parts:
		i=len(parts)-1
		while i>=1:
			if parts[i]=='..' and parts[i-1]!='..':
				# print 'to del:', parts[i-1], parts[i]
				del parts[i-1]
				del parts[i-1]
				i-=1
			i-=1
		if len_old==len(parts):
			break
		len_old=len(parts)
	return prefix+'/'.join(parts)+suffix
	
file_exts={
	'pdf_file'		:	'pdf|ps|ps.gz',
	'doc_file'		:	'doc|docx|xls|csv|tab',
	'picture_file'	:	'jpg|jpeg|png|gif|tiff|bmp',
	'normal_text'	:	'txt',
	'hyper_text'	:	'htm|html|shtml',
	'xml_file'		:	'xml|xslt',
	'css_file'		:	'css',
	'js_file'		:	'js',
	'zip_file'		:	'zip|gz|tar|rar|jar',
	'media_link'	:	'mp4|mp3|wma|wmv|rm|rmvb|mpeg|mpeg3|3gp|avi|ts|flv|f4v',
	'swf_link'		:	'swf|fla',
	'server_page'	:	'php|jsp|asp|aspx|py',
}

r_res=re.compile('^[^(javascript)].+?\.('+'|'.join(file_exts.values())+')([\?#].*)?$', re.I)
r_nojslink=re.compile('^[^(javascript:)].+$', re.I)
r_nomailtolink=re.compile('^[^(mailto://)].+$', re.I)
r_goodlink=re.compile('^[^(mailto://)(javascript:)].+$', re.I)

def nice_url(page, urls):
	#将当前页面的所有链接进行优化: 对相对链接补全，展开，根目录链接转换
	page=page.strip()
	site_host=get_host_by_url(page)
	# print 'site_host:', site_host
	page=strip_url_tail(page)
	type=get_file_type_by_url(page)
	if type=='dir':
		parent_url=page+'/' if page[-1]!='/' else page
	else:
		parent_url=page[:page.rfind('/')+1]

	root_url=page[:page.find(site_host)]+site_host
	urls=[l if l.startswith('http://') or l.startswith('ftp://') or l.startswith('https://') else (root_url+l if l[0]=='/' else parent_url+l) for l in urls]
	urls=[strip_url_anchor(url_merge_dots(l)) for l in urls]
	return urls
	
def base_url(url):
	protocal, netloc, path, params, query, anchor=urlparse.urlparse(url)
	path=dirname(path)
	tpl=protocal, netloc, path, params, query, anchor
	return urlunparse(tpl)
	
def expand_urls(page, urls):
	'''
	expand all urls in the page
	'''
	parent=base_url(page.strip())
	# print 'parent=', parent
	urls=[urljoin(parent, url.strip()) for url in urls]
	rets=[]
	for url in urls:
		try:
			nurl=normalize_url(url)
		except Exception, e:
			print 'error when normalize_url %s : %s', (url, e)
			continue
		rets.append(nurl)
	return rets
	
def one_nice_url(page, url):
	return nice_url(page, [url])[0]

def fix_url(url, charset='utf-8'):
	'''Sometimes you get an URL by a user that just isn't a real
	URL because it contains unsafe characters like ' ' and so on.  This
	function can fix some of the problems in a similar way browsers
	handle data entered by the user:

	>>> url_fix(u'http://de.wikipedia.org/wiki/Elf (Begriffsklärung)')
	'http://de.wikipedia.org/wiki/Elf%20%28Begriffskl%C3%A4rung%29'

	:param charset: The target charset for the URL if the url was
		    given as unicode string.
	'''
	if isinstance(url, unicode): url =url.encode(charset, 'ignore')
	scheme, netloc, path, qs, anchor = urlparse.urlsplit(url)
	path = urllib.quote(path, '/%')
	qs = urllib.quote_plus(qs, ':&=')
	return urlparse.urlunsplit((scheme, netloc, path, qs, anchor))
    
if __name__=='__main__':
	url='http://a.a//../../asd/kk/../../../asd.asd/./ss/./././hsadk...$?1=1#kasjdl-qw'
	print url_merge_dots(url)
	print normalize_url(url)
	
	page='http://jadesoul-home'
	urls=u'''
		http://jadesoul-home/index.php
		http://jadesoul-home/?p=30
		a.html
		a/b/c/d.txt
		a/b/../c/d.txt
		http://a.a//../../asd/kk/../../../asd.asd/./ss/./././hsadk...$?1=1#kasjdl-qw
		https://www.abc.com./a.txt
		http://www.abc.com:80/a.txt
		https://www.abc.com.:8080/a.txt
		ftp://www.abc.com:21/a.txt
		ftp://www.abc.com:21/a.txt
		ftp://www.abc.com:21/ a.txt
	'''.strip().split('\n')
	print '----------------------------------nice_url'
	for i in nice_url(page, urls):
		print i
	print '----------------------------------expand_urls'
	for i in expand_urls(page, urls):
		print i
	print
	
	# protcal, netloc, host, port, user, pwd, path, query, anchor=parse_url(url)
	print parse_url('http://www.ABC.com/a/b/c.html 1?a=1&b=2#tag')
	print parse_url('https://www.ABC.com:8080/a/b/c.html 1?a=1&b=2#tag')
	print parse_url('smtp://www.ABC.com:8080/a/b/c.html 1?a=1&b=2#tag')
	print parse_url('http://jadesoul:123@jadesoul-dev:8090/a/b/c.html?a=1&b=2#tag')
	print parse_url('ftp://jadesoul:123@jadesoul-dev:8090/a/b/c.html?a=1&b=2#tag')
	print parse_url('ssh://jadesoul:123@jadesoul-dev:8090/a/b/c.html?a=1&b=2#tag')
	
    # print parse_url('https://www.ABC.com:8080/a/b/c.html 1?a=1&b=2#tag')
