#!/usr/bin/env python

from distutils.core import setup

requirements = []

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='aiofastgate',
    version='1.0',
    description='Python Distribution Utilities',
    author='chickenmatty',
    url='https://github.com/chickenmatty/aiofastgate',
    packages=['aiofastgate'],
    install_requires=requirements,
)
