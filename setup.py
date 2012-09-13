#!/usr/bin/env python
from distutils import sysconfig
from distutils.core import setup
from os import listdir, getcwd
from os.path import isfile

setup(
	name='libjade',
	version='1.0',
	description='Jadesoul\'s Python Distribution Utilities',
	author='Jaden Wu',
	author_email='wslgb2006@gmail.com',
	url='http://jadesoul.sinaapp.com/',
	license='Python Software Foundation License',
	packages=['libjade', 'libjade.database'], 
	scripts=filter(isfile, ['scripts/'+i for i in listdir('scripts')]),
)
