#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import sys
from setuptools import find_packages, setup

NAME = 'create_and_validate_acm_cert'
DESCRIPTION = 'Creates an ACM certificate with DNS validation, creates the validation records directly in Route 53'
URL = 'https://github.com/dylburger/create-and-validate-acm-certificate'
AUTHOR = 'dylburger'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = None

REQUIRED = [
    'boto3',
    'requests',
    'tldextract',
]

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

about = {}
if not VERSION:
    with open(os.path.join(here, NAME, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION

setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=('tests',)),
    install_requires=REQUIRED,
    include_package_data=True,
    license='MIT',
)