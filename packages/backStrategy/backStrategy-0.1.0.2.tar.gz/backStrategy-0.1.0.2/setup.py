#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author   : Kevin
# @Time     : 2022/12/12

import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='backStrategy',
    version='0.1.0.2',
    author='Kevin',
    author_email='1782552261@qq.com',
    description='读取数据更新,接口更新',
    long_description=long_description,
    url='https://gitee.com/Jason520deng/back-strategy',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

