#!/usr/bin/env python
from distutils import sysconfig
from distutils.core import setup
from os import listdir, getcwd

# generate pth file
f=open('libjade.pth', 'w')
f.write(getcwd())
f.close()

# setup
site_packages_path=sysconfig.get_python_lib()
setup(
	name='libjade',
	version='1.0',
	description='Jadesoul\'s Python Distribution Utilities',
	author='Jaden Wu',
	author_email='wslgb2006@gmail.com',
	url='http://jadesoul.sinaapp.com/',
	license='Python Software Foundation License',
	# packages=['libjade'], # install a pth file instead of a package for debug
	scripts=['scripts/'+i for i in listdir('scripts')],
	data_files=[(site_packages_path, ["libjade.pth"])]
)
