#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

from setuptools import setup, find_packages

# Python versions this package is compatible with
python_requires = '>=3.6, <4'

# Packages that this package imports. List everything apart from standard lib packages.
install_requires = [
    'sensirion-shdlc-driver~=0.1.5',
    'sensirion-driver-adapters>=2.1.8,<3.0',
    'sensirion-driver-support-types~=0.2.0',
]

# Packages required for tests and docs
extras_require = {
    'test': [
        'flake8~=3.7.8',
        'pytest~=6.2.5',
        'pytest-cov~=3.0.0',
    ],
    'docs': [
        'click==8.0.4',
        'jinja2==3.0.1',
        'sphinx~=2.2.1',
        'sphinx-rtd-theme~=0.4.3',
    ]
}

# Read version number from version.py
version_line = open("sensirion_uart_sfx6xxx/version.py", "rt").read()
result = re.search(r"^version = ['\"]([^'\"]*)['\"]", version_line, re.M)
if result:
    version_string = result.group(1)
else:
    raise RuntimeError("Unable to find version string")

# Use README.rst and CHANGELOG.rst as package description
root_path = os.path.dirname(__file__)
readme = open(os.path.join(root_path, 'README.rst')).read()
changelog = open(os.path.join(root_path, 'CHANGELOG.rst')).read()
long_description = readme.strip() + "\n\n" + changelog.strip() + "\n"

setup(
    name='sensirion_uart_sfx6xxx',
    version=version_string,
    author='Sensirion',
    author_email='info@sensirion.com',
    description='SHDLC driver for the Sensirion SFX6XXX sensor family',
    license='BSD',
    keywords="""Sensirion SFX6XXX
        SHDLC
        UART
        SFC6000
        SFC6000D-5slm
        SFC6000D-50slm
        SFC6000D-20slm
        SFM6000
        SFM6000D-20slm
        SFM6000D-50slm
        SFM6000D-5slm""",
    url='https://sensirion.github.io/python-uart-sfx6xxx/',
    packages=find_packages(exclude=['tests', 'tests.*']),
    long_description=long_description,
    python_requires=python_requires,
    install_requires=install_requires,
    extras_require=extras_require,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
