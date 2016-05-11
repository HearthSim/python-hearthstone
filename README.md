## python-hearthstone

A Hearthstone Python library containing:

* A CardDefs.xml parser (`hearthstone.cardxml`)
* A Power.log parser (`hearthstone.hslog`)
* A DbfXml parser (`hearthstone.dbf`)
* Hearthstone enums as IntEnum (`hearthstone.enums`)


The project is versioned as `$major.$minor.$build`, where `$build`
represents the latest Hearthstone build the library is compatible with.


### Requirements

* Python 3.4+
* (optional) python-dateutil for `hearthstone.hslog`


### Installation

* To install from source: `./bootstrap && ./setup.py install`
* To install from PyPI: `pip install hearthstone`


### License

This project is licensed under the MIT license. The full license text is
available in the LICENSE file.

The CardDefs.xml file distributed on PyPI contains Hearthstone data that
is copyright © Blizzard Entertainment.


### Community

This is a [HearthSim](https://hearthsim.info) project. All development
happens on our IRC channel `#hearthsim` on [Freenode](https://freenode.net).
