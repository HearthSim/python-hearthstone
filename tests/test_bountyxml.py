from hearthstone import bountyxml


def test_bountyxml_load():
	bounty_db, _ = bountyxml.load()

	assert bounty_db

	assert bounty_db[68].boss_name == "Elris Gloomstalker"
	assert bounty_db[58].region_name == "The Barrens"
