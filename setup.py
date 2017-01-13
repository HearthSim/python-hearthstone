#!/usr/bin/env python

import hearthstone
from setuptools import setup, find_packages


CLASSIFIERS = [
	"Development Status :: 5 - Production/Stable",
	"Intended Audience :: Developers",
	"License :: OSI Approved :: MIT License",
	"Programming Language :: Python",
	"Programming Language :: Python :: 3",
	"Programming Language :: Python :: 3.4",
	"Programming Language :: Python :: 3.5",
	"Programming Language :: Python :: 3.6",
	"Topic :: Games/Entertainment :: Simulation",
]

setup(
	name="hearthstone",
	version=hearthstone.__version__,
	packages=find_packages(),
	package_data={"": ["CardDefs.xml", "Strings/*/*.txt"]},
	include_package_data=True,
	author=hearthstone.__author__,
	author_email=hearthstone.__email__,
	description="CardDefs.xml parser and Hearthstone enums for Python applications",
	classifiers=CLASSIFIERS,
	download_url="https://github.com/HearthSim/python-hearthstone/tarball/master",
	license="MIT",
	url="https://github.com/HearthSim/python-hearthstone",
	zip_safe=True,
)
