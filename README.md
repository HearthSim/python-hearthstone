# python-hearthstone

[![Build Status](https://api.travis-ci.org/HearthSim/python-hearthstone.svg?branch=master)](https://travis-ci.org/HearthSim/python-hearthstone)
[![PyPI](https://img.shields.io/pypi/v/hearthstone.svg)](https://pypi.org/project/hearthstone/)

A Hearthstone Python library containing:

* A CardDefs.xml parser (`hearthstone.cardxml`)
* A DbfXml parser (`hearthstone.dbf`)
* Hearthstone enums as IntEnum (`hearthstone.enums`)

The log parser previously in `hearthstone.hslog` has moved to the
[python-hslog project](https://github.com/HearthSim/python-hslog).

The CardDefs.xml data for the latest build is available in the
[python-hearthstone-data repository](https://github.com/HearthSim/python-hearthstone-data)
or on PyPI with `pip install hearthstone_data`.


## Requirements

* Python 3.6+
* lxml

## Installation

* To install from PyPI: `pip install hearthstone`


## License

This project is licensed under the MIT license. The full license text is
available in the LICENSE file.


## Community

This is a [HearthSim](https://hearthsim.info) project.
Join the HearthSim Developer community [on Discord](https://discord.gg/hearthsim-devs).
