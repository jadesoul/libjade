#coding:utf8

import getopt

from sys import argv, exit
from filesys import splitdir
from dbg import cerr, clog

argc=len(argv)
app_path=argv[0]
app_dir, app_name=splitdir(app_path)
app=app_name

def show_usage(help_txt):
	global argc, argv, app
	cerr(('Usage: %s '+help_txt) % app)
	
def setup_app(main_func, min_params=0, help_txt=''):
	global argc, argv, app
	required_args=min_params+1
	
	if argc>=2 and argv[1] in ['-h', '--help']:
		show_usage(help_txt)
		exit()
			
	if argc>=required_args:
		args=argv[1:required_args] if required_args!=1 else argv[1:]
		main_func(*args)
	else:
		show_usage(help_txt)
		cerr('Error: need at least %d arguments' % min_params)
		exit()
	
if __name__=='__main__':
	print argv, argc, app_path, app_dir, app_name, app
	
