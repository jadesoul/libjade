#coding:utf8

import logging, sys

message_format='%(name)-8s %(asctime)s %(levelname)-8s %(message)s'
# time_format='%a, %d %b %Y %H:%M:%S'
time_format='[%Y-%m-%d %a %H:%M:%S]'
default_formatter=logging.Formatter(message_format, time_format)

# Logging有如下级别: DEBUG，INFO，WARNING，ERROR，CRITICAL
# 默认级别是WARNING, logging模块只会输出指定level以上的log

# logging.basicConfig(level=logging.INFO, format=message_format, datefmt=time_format, filename='log.log')
# logging.basicConfig(level=logging.ERROR, format='\t')
logging.basicConfig(level=1, format=message_format, datefmt=time_format, stream=sys.stdout)

class Logger(object):
	def __init__(self, name, level=logging.NOTSET, filepath=None, stream=sys.stdout):
		self.logger=logging.getLogger(name)
		self.logger.setLevel(level)
		if filepath: self.log_file(filepath)
		if stream: self.log_stream(stream)
		
	def log_file(self, filepath, level=logging.NOTSET, formatter=default_formatter):	
		fh=logging.FileHandler(filepath)
		fh.setLevel(level)
		fh.setFormatter(formatter)
		self.logger.addHandler(fh)
		
	def log_stream(self, stream=sys.stdout, level=logging.NOTSET, formatter=default_formatter):	
		sh=logging.StreamHandler(stream)
		sh.setLevel(level)
		sh.setFormatter(formatter)
		self.logger.addHandler(sh)
		
logger=Logger('root', 1)
# logger=Logger('DEFAULT', 1, None, sys.stderr)

def debug(s):
	logger.logger.debug(s)
	
def info(s):
	logger.logger.info(s)
	
def warn(s):
	logger.logger.warn(s)
	
def error(s):
	logger.logger.error(s)
	
def critical(s):
	logger.logger.critical(s)
	
if __name__=='__main__':
	debug('debug')
	info('info')
	warn('warn')
	error('error')
	critical('critical')
	
	
	
	
	
	
	
	
	