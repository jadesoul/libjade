#coding:utf8

def join_host_path(host, path, protocal="http"):
	if path[0]!="/": host=host+"/"
	return protocal+"://"+host+path 

def get_nice_url(url, host=""):
	low_url=url.lower()
	if not low_url.startswith("http://"):
		#相对路径
		if url.startswith("#") \
			or low_url.startswith("mailto:") \
			or low_url.startswith("javascript:") \
			or url.find("://")!=-1 \
			or url.strip()=="": return None  #ignore ftp, https
		#print host, url
		url=join_host_path(host, url)
		#print url
	#绝对路径
	pos=url.find("#")
	if pos!=-1:
		url=url[:pos]
			
	low_url=url.lower()
	
	#排除后缀
	if low_url.endswith(".pdf") \
		or low_url.endswith(".jpg") or low_url.endswith(".jpeg") or low_url.endswith(".png") or low_url.endswith(".gif")\
		or low_url.endswith(".zip") or low_url.endswith(".rar") or low_url.endswith(".gzip") or low_url.endswith(".tar") or low_url.endswith(".jar")\
		or low_url.endswith(".gz") or low_url.endswith(".7z") or low_url.endswith(".exe") or low_url.endswith(".dll")\
		or low_url.endswith(".xml") or low_url.endswith(".js") or low_url.endswith(".css") \
		or low_url.endswith(".ppt") or low_url.endswith(".pptx") \
		or low_url.endswith(".xls") \
		or low_url.endswith(".doc") or low_url.endswith(".docx"): return None
	return url

		
# def urlencode(url):
	# gbk=unicode(url).encode('gbk')
	# return repr(gbk).replace(r'\x','%')[1:-1].replace(' ', '%20')

if __name__=='__main__':
	pass

