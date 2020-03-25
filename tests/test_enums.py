from datetime import datetime

from hearthstone import enums


def test_zodiac_dates():
	assert enums.ZodiacYear.as_of_date(datetime(2014, 1, 1)) == enums.ZodiacYear.PRE_STANDARD
	assert enums.ZodiacYear.as_of_date(datetime(2016, 1, 1)) == enums.ZodiacYear.PRE_STANDARD
	assert enums.ZodiacYear.as_of_date(datetime(2016, 6, 1)) == enums.ZodiacYear.KRAKEN
	assert enums.ZodiacYear.as_of_date(datetime(2017, 1, 1)) == enums.ZodiacYear.KRAKEN
	assert enums.ZodiacYear.as_of_date(datetime(2017, 5, 1)) == enums.ZodiacYear.MAMMOTH
	assert enums.ZodiacYear.as_of_date(datetime(2018, 5, 1)) == enums.ZodiacYear.RAVEN


def test_cardclass():
	playable_cards = [
		enums.CardClass.DEMON_HUNTER,
		enums.CardClass.DRUID,
		enums.CardClass.HUNTER,
		enums.CardClass.MAGE,
		enums.CardClass.PALADIN,
		enums.CardClass.PRIEST,
		enums.CardClass.ROGUE,
		enums.CardClass.SHAMAN,
		enums.CardClass.WARLOCK,
		enums.CardClass.WARRIOR
	]

	for c in playable_cards:
		assert c.is_playable

	for c in enums.CardClass:
		if c not in playable_cards:
			assert not c.is_playable


def test_gametype():
	gt = enums.GameType
	bgt = enums.BnetGameType

	assert gt.GT_RANKED.as_bnet(wild=False) == bgt.BGT_RANKED_STANDARD
	assert gt.GT_RANKED.as_bnet(wild=True) == bgt.BGT_RANKED_WILD
	assert gt.GT_CASUAL.as_bnet(wild=False) == bgt.BGT_CASUAL_STANDARD
	assert gt.GT_CASUAL.as_bnet(wild=True) == bgt.BGT_CASUAL_WILD

	assert gt.GT_VS_AI.as_bnet() == bgt.BGT_VS_AI
	assert gt.GT_VS_FRIEND.as_bnet() == bgt.BGT_FRIENDS

	assert gt.GT_FSG_BRAWL_VS_FRIEND.is_fireside
	assert gt.GT_FSG_BRAWL.is_fireside
	assert gt.GT_FSG_BRAWL_1P_VS_AI.is_fireside
	assert gt.GT_FSG_BRAWL_2P_COOP.is_fireside
	assert not gt.GT_RANKED.is_fireside

	assert gt.GT_TAVERNBRAWL.is_tavern_brawl
	assert gt.GT_TB_1P_VS_AI.is_tavern_brawl
	assert gt.GT_TB_2P_COOP.is_tavern_brawl
	assert not gt.GT_RANKED.is_tavern_brawl
