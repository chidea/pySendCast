#!/usr/bin/env python3

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

long_description = open('README.md').read()
if type(long_description) is bytes:
  long_description = long_description.decode()

setup(
    name='pySendCast',
    version='0.1.2',
    author='Ch.Idea',
    author_email='sbw228@gmail.com',
    description='A pure Python cross-platform program to send and receive data over local area network(LAN) with on-the-fly gzip streaming and broadcasting',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/chidea/pySendCast',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Communications :: File Sharing',
        'Topic :: System :: Networking',
        'Natural Language :: English',
    ],
    entry_points={
      'console_scripts': [
        'sendcast=pySendCast.__main__:main',
      ]
    },
)
