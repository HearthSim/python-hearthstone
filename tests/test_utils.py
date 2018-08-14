from hearthstone import cardxml
from hearthstone.utils import UPGRADABLE_CARDS_MAP


def test_upgradable_card_map():
	cardid_db, _ = cardxml.load()

	for upgraded, original in UPGRADABLE_CARDS_MAP.items():
		assert cardid_db[original]
		assert cardid_db[original].collectible
		assert cardid_db[upgraded]
		assert not cardid_db[upgraded].collectible
