"""
This is a file to descrive the Python module distribution and
helps with installation.

More info on various arguments here:
https://docs.python.org/3.6/distutils/setupscript.html
"""
from setuptools import setup, find_packages


setup(
    name='pidgin',
    version='0.0.1',
    description='Gen3 pidgin service',
    url='https://github.com/uc-cdis/pidgin',
    license='Apache',
    packages=find_packages(),
)
