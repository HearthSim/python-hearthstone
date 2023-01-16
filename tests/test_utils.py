from hearthstone import cardxml
from hearthstone.enums import Race
from hearthstone.utils import CARDRACE_TAG_MAP, UPGRADABLE_CARDS_MAP


def test_upgradable_card_map():
	cardid_db, _ = cardxml.load()

	for upgraded, original in UPGRADABLE_CARDS_MAP.items():
		assert cardid_db[original]
		assert cardid_db[original].collectible
		assert cardid_db[upgraded]
		assert not cardid_db[upgraded].collectible


def test_race_tag_map():
	for race in Race:
		if race != Race.INVALID:
			assert race in CARDRACE_TAG_MAP, \
				"%s is missing from utils.CARDRACE_TAG_MAP" % race
