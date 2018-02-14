from hearthstone import cardxml


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
