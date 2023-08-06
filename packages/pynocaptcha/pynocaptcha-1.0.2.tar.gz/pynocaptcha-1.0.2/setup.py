#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup


with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='pynocaptcha',
    version='1.0.2',
    description='nocaptcha.io api',
    long_description='nocaptcha.io python api',
    author='esbiya',
    author_email='2995438815@qq.com',
    url='https://github.com/captcha-keepalive/pynocaptcha',
    install_requires=[],
    license='MIT',
    packages=["pynocaptcha/crackers"],
    package_dir={'pynocaptcha': 'pynocaptcha'},
    platforms=["all"],
    include_package_data=True,
    zip_safe=False,
    keywords='nocaptcha',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3'
    ],
)
