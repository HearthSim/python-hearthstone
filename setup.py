#!/usr/bin/env python

import hearthstone
from setuptools import setup


setup(
	version=hearthstone.__version__,
	package_data={"": ["CardDefs.xml", "Strings/*/*.txt"]},
)
