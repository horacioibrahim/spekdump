# -*- coding: utf-8 -*-
try:
    from distutils.core import setup
except ImportError:
    from setuptools import setup

import sys, os
from setuptools import find_packages
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'spekdump'))
from spekdump.version import __version__

setup(
  name='spekdump',
  version= __version__,
  author='Horacio Ibrahim',
  author_email='horacioibrahim@gmail.com',
  packages=find_packages('.'),
  package_dir={'': '.'},
  scripts=[],
  url='https://github.com/horacioibrahim/spekdump',
  license='MIT License',
  description="It's a lib to handling the spekx CSV files",
  classifiers=[
    'Development Status :: Production/Stable',
    'Intended Audience :: Developers',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Topic :: Software Development :: Libraries :: Python Modules'
  ],
  install_requires=['pymongo']
  keywords=['spekx']
)
