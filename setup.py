# -*- coding: utf-8 -*-

from setuptools import setup, Extension

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='subprocessPlus',
    version='0.0.1',
    description='A set of functions to run improved parallel or series subprocesses with Python',
    long_description=readme,
    author='Salvatore Davide Porzio',
    author_email='porziodavide@gmail.com',
    url='https://github.com/sdporzio/fancy-subprocesses',
    license='GPL-3.0',
    packages=['subprocPlus'],
    zip_safe=False)
