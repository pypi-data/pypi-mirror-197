#!/usr/bin/env python
# This shim enables editable installs
import setuptools
import site
import sys

setuptools.setup(
	name="dailyfresh",
	version="0.0.2",
	packages=setuptools.find_packages(),
	python_requires='>3'
)