# coding: utf-8

from setuptools import setup, find_packages

setup(
    name = "mambo-unifi-api",
    version = "1.0.5",
    packages = find_packages('src'),
    package_dir = {"": "src"},
    install_requires = [
        'requests>=2.21.0,<3',
        'trafaret>=1.2.0<1.3',
    ],
    author='Nelson Fonseca',
    author_email='nelson.fonseca@mambowifi.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Information Technology',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
)
