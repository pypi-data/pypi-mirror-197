#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    packages=find_packages(exclude=['tests*']),
    py_modules=['validator_entrypoint'],
    include_package_data=True,
)
