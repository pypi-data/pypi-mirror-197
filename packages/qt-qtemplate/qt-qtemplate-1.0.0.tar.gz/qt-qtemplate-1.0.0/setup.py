#!/usr/bin/python3
# -*- coding: utf-8 -*-
# python .\setup.py sdist
# twine upload --repository pypi dist/*
from qtemplate import VERSION
from pkg_resources import parse_requirements
from setuptools import setup

readme = open('README.md', 'r').read()
with open('requirements.txt') as handle:
    requirements = [str(req) for req in parse_requirements(handle)]

setup(
    name='qt-qtemplate',
    version=VERSION,
    description='Simple but powerful QT template language for PySide6.',
    author='Michael Shepanski',
    author_email='michael.shepanski@gmail.com',
    url='https://github.com/pkkid/python-qtemplate',
    packages=['qtemplate'],
    install_requires=requirements,
    python_requires='>=3.7',
    long_description=readme,
    keywords=['pyside6', 'qt', 'template'],
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
    ]
)
