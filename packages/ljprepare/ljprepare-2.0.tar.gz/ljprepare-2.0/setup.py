from distutils.core import  setup
import setuptools
packages = ['ljprepare']# 唯一的包名，自己取名
setup(name='ljprepare',
	version='2.0',
	author='lj',
    packages=packages,
    package_dir={'requests': 'requests'},)