import os.path
from collections import OrderedDict
from io import BytesIO
from hearthstone.dbf import Dbf


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_resource(path):
	return os.path.join(BASE_DIR, "res", path)


def test_dbf():
	path = get_resource("DECK_RULESET_RULE_SUBSET.xml")

	dbf = Dbf.load(path)
	assert dbf.name == "DECK_RULESET_RULE_SUBSET"
	assert dbf.source_fingerprint == "ziY6RY+E/zCQ496Av7HKSCR+zls="
	assert dbf.columns == OrderedDict([
		("DECK_RULESET_RULE_ID", "Int"),
		("SUBSET_ID", "Int"),
	])
	assert dbf.records == [
		{"DECK_RULESET_RULE_ID": 5, "SUBSET_ID": 6},
		{"DECK_RULESET_RULE_ID": 15, "SUBSET_ID": 6},
	]

	dbf2 = Dbf()
	dbf2.populate(BytesIO(dbf.to_xml()))
	assert dbf2.source_fingerprint == dbf.source_fingerprint
	assert dbf2.columns == dbf.columns

	for r1, r2 in zip(dbf.records, dbf2.records):
		assert r1 == r2
