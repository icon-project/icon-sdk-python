import os
from setuptools import setup, find_packages

with open(os.path.join('.', 'VERSION')) as version_file:
    version = version_file.read().strip()

with open("README.md", 'r') as f:
    long_description = f.read()

with open("requirements.txt") as requirements:
    requires = list(requirements)

setup(
    name='iconsdk',
    version=version,
    description='ICON SDK for Python is a collection of libraries which allow you to interact '
                'with a local or remote ICON node using an HTTP connection.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='ICON Foundation',
    author_email='foo@icon.foundation',
    url='https://github.com/icon-project/icon-sdk-python',
    packages=find_packages(exclude=['tests*']),
    install_requires=requires,
    python_requires='~=3.7',
    license='Apache License 2.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.7'
    ]
)
