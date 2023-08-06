#!/usr/bin/env python

"""The setup script."""
import os
import io
from setuptools import setup, find_packages

from pavilion_cms import __author__, __email__
from pavilion_cms.__version__ import __version__


NAME = "pavilioncms-python"
DESCRIPTION = "Python Package to make use of PavilionCMS"
EMAIL = __email__
AUTHOR = __author__
REQUIRES_PYTHON = ">=3.6, <3.11"
VERSION = __version__

REQUIRED = [
    "requests>=2.28.1",
]

base_dir = os.path.abspath(os.path.dirname(__file__))

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

long_description = f"{readme} \n\n {history}"

test_requirements = REQUIRED + ['pytest>=3', ]

setup(
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    long_description=long_description,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    description=DESCRIPTION,
    install_requires=REQUIRED,
    license="MIT license",
    long_description_content_type='text/markdown',
    include_package_data=True,
    name=NAME,
    packages=find_packages(exclude=["tests", "_example"]),
    test_suite='tests',
    tests_require=test_requirements,
    version=VERSION,
    setup_requires=["wheel"],
)
