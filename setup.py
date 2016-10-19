# -*- coding: utf-8 -*-

from setuptools import setup, Extension
import numpy.distutils.misc_util
import numpy as np

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='FancySubprocesses',
    version='0.0.1',
    description='A set of functions to run parallel or series subprocesses with Python',
    long_description=readme,
    author='Salvatore Davide Porzio',
    author_email='porziodavide@gmail.com',
    url='https://github.com/sdporzio/fancy-subprocesses',
    license='MIT',
    packages=['fancySubprocesses'],
    install_requires=[
        'numpy'
    ],
    zip_safe=False)
