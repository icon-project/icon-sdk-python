# -*- coding: utf-8 -*-
# Copyright 2018 ICON Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from os import environ, path

from setuptools import setup, find_packages

version = environ.get('VERSION')

if version is None:
    with open(path.join('.', 'VERSION')) as version_file:
        version = version_file.read().strip()

with open("README.md", 'r') as f:
    long_description = f.read()

with open("requirements.txt") as requirements:
    requires = list(requirements)

setup(
    name='iconsdk',
    version=version,
    description='ICON SDK for Python is a collection of libraries which allow you to interact '
                'with a local or remote Loopchain node, using an HTTP connection. ',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='ICON foundation',
    author_email='foo@icon.foundation',
    url='https://github.com/icon-project/icon-sdk-python',
    packages=find_packages(exclude=['tests*']),
    test_suite='tests',
    tests_require=[
        'secp256k1==0.13.2'
    ],
    install_requires=requires,
    license='Apache License 2.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6'
    ]
)
