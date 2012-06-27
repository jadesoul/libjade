#!/usr/bin/env python

from distutils.core import setup
from os import listdir

setup(
	  name='libjade',
      version='1.0',
      description='Jadesoul\'s Python Distribution Utilities',
      author='Jaden Wu',
      author_email='wslgb2006@gmail.com',
      url='http://jadesoul.sinaapp.com/',
	  license='Python Software Foundation License',
      packages=['libjade'],
	  scripts=['scripts/'+i for i in listdir('scripts')],
)
