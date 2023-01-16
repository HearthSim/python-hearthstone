from hearthstone import cardxml
from hearthstone.enums import GameTag, Race


def test_cardxml_load():
	cardid_db, _ = cardxml.load()
	dbf_db, _ = cardxml.load_dbf()

	assert cardid_db
	assert dbf_db

	for card_id, card in cardid_db.items():
		assert dbf_db[card.dbf_id].id == card_id

	for dbf_id, card in dbf_db.items():
		assert cardid_db[card.id].dbf_id == dbf_id

	assert cardid_db["EX1_001"].quest_reward == ""
	assert cardid_db["UNG_940"].quest_reward == "UNG_940t8"


def test_races():
	card = cardxml.CardXML("EX1_001")
	card.tags[GameTag.CARDRACE] = Race.UNDEAD
	card.tags[Race.DRAGON.race_tag] = 1
	assert card.races == [
		Race.UNDEAD,
		Race.DRAGON,
	]
