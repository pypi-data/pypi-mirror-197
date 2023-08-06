from distutils.core import  setup
import setuptools
packages = ['mrn_wsb']# 唯一的包名，自己取名
setup(name='mrn_wsb',
	version='1.0',
	author='gdxy',
    packages=packages, 
    package_dir={'requests': 'requests'},)
