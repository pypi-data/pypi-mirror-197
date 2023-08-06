from setuptools import setup, find_packages
setup(
name='my-ctl',
version='1.0.2',
description='myctl quick create  project',
author_email='labelnet@foxmail.com',
author='labelnet',
license='labelnet',
keywords=['my-ctl'],
packages=find_packages(),
include_package_data=True,
install_requires=['nuitka==0.6.17.5', 'requests==2.25.1', 'pytest==6.2.5', 'pyyaml==6.0', 'click==8.0.3', 'twine==3.5.0'],
python_requires='>=3.8',
entry_points="""
[console_scripts]
myctl=my_ctl:cli
"""
)