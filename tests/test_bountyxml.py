import sys

from hearthstone import bountyxml


def test_bountyxml_load():
	bounty_db, _ = bountyxml.load()

	assert bounty_db

	assert bounty_db[68].boss_name == "Elris Gloomstalker"
	assert bounty_db[58].region_name == "The Barrens"


def test_bountyxml_load_without_hearthstone_data(monkeypatch):
	from hearthstone_data import get_bountydefs_path
	path = get_bountydefs_path()

	monkeypatch.setattr(bountyxml, "bounty_cache", {})
	monkeypatch.setitem(sys.modules, "hearthstone_data", None)

	db, _ = bountyxml.load(path=path)

	assert db
	assert db[68].boss_name == "Elris Gloomstalker"
