from hearthstone import bountyxml


def test_bountyxml_load():
	bounty_db, _ = bountyxml.load()

	assert bounty_db

	assert bounty_db[47].boss_name == "Cap'n Hogger"
	assert bounty_db[58].region_name == "The Barrens"
