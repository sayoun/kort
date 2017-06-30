#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import re
from setuptools import setup, find_packages

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

name = 'kort'

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.md')).read()


with open(os.path.join(here, name, '__init__.py')) as v_file:
    version = re.compile(r".*__version__ = '(.*?)'",
                         re.S).match(v_file.read()).group(1)

requires = ['Flask', 'SQLAlchemy', 'pyyaml']

setup(name=name,
      version=version,
      description='Kort is a simple python URL-Shortener API',
      classifiers=['Development Status :: 4 - Beta',
                   'Intended Audience :: Developers',
                   'License :: Other/Proprietary License',
                   'Operating System :: Unix',
                   'Programming Language :: Python :: 3.4',
                   'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
                   ],
      author='sayoun',
      author_email='sayoun@protonmail.com',
      url='https://github.com/sayoun/kort',
      license='Proprietary',
      install_requires=requires,
      tests_require=requires,
      packages=find_packages(),
      include_package_data=True,
      entry_points="""\
[console_scripts]
kort = kort.bin.cli:main
""",
      )
