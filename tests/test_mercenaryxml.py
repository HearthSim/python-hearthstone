import sys

from hearthstone import mercenaryxml
from hearthstone.enums import Rarity


def test_mercenaryxml_load():
	mercenary_db, _ = mercenaryxml.load()

	assert mercenary_db

	assert mercenary_db[3].name == "Kurtrus Ashfallen"
	assert mercenary_db[3].collectible
	assert mercenary_db[3].rarity == Rarity.RARE

	assert mercenary_db[231].name == "Toki"
	assert not mercenary_db[231].collectible
	assert mercenary_db[231].rarity == Rarity.LEGENDARY


def test_mercenaryxml_load_without_hearthstone_data(monkeypatch):
	from hearthstone_data import get_mercenarydefs_path
	path = get_mercenarydefs_path()

	monkeypatch.setattr(mercenaryxml, "mercenary_cache", {})
	monkeypatch.setitem(sys.modules, "hearthstone_data", None)

	db, _ = mercenaryxml.load(path=path)

	assert db
	assert db[3].name == "Kurtrus Ashfallen"
