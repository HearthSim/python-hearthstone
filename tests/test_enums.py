from datetime import datetime

from hearthstone import enums
from hearthstone.enums import CardClass, Locale, get_localized_name


def test_zodiac_dates():
	assert enums.ZodiacYear.as_of_date(datetime(2014, 1, 1)) == enums.ZodiacYear.PRE_STANDARD
	assert enums.ZodiacYear.as_of_date(datetime(2016, 1, 1)) == enums.ZodiacYear.PRE_STANDARD
	assert enums.ZodiacYear.as_of_date(datetime(2016, 6, 1)) == enums.ZodiacYear.KRAKEN
	assert enums.ZodiacYear.as_of_date(datetime(2017, 1, 1)) == enums.ZodiacYear.KRAKEN
	assert enums.ZodiacYear.as_of_date(datetime(2017, 5, 1)) == enums.ZodiacYear.MAMMOTH
	assert enums.ZodiacYear.as_of_date(datetime(2018, 5, 1)) == enums.ZodiacYear.RAVEN


def test_cardclass():
	playable_cards = [
		enums.CardClass.DEATHKNIGHT,
		enums.CardClass.DEMONHUNTER,
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

	assert gt.GT_RANKED.as_bnet(format=enums.FormatType.FT_CLASSIC) == bgt.BGT_RANKED_CLASSIC
	assert gt.GT_RANKED.as_bnet(format=enums.FormatType.FT_STANDARD) == bgt.BGT_RANKED_STANDARD
	assert gt.GT_RANKED.as_bnet(format=enums.FormatType.FT_WILD) == bgt.BGT_RANKED_WILD
	assert gt.GT_CASUAL.as_bnet(format=enums.FormatType.FT_CLASSIC) == bgt.BGT_CASUAL_CLASSIC
	assert gt.GT_CASUAL.as_bnet(format=enums.FormatType.FT_STANDARD) == bgt.BGT_CASUAL_STANDARD
	assert gt.GT_CASUAL.as_bnet(format=enums.FormatType.FT_WILD) == bgt.BGT_CASUAL_WILD

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


class TestCardSet:
	def test_name_global(self):
		assert enums.CardSet.NAXX.name_global == "GLOBAL_CARD_SET_NAXX"
		assert enums.CardSet.THE_SUNKEN_CITY.name_global == "GLOBAL_CARD_SET_TSC"


class TestMultiClassGroup:
	def test_card_classes(self):
		assert enums.MultiClassGroup.GRIMY_GOONS.card_classes == [
			enums.CardClass.HUNTER,
			enums.CardClass.WARRIOR,
			enums.CardClass.PALADIN,
		]
		assert enums.MultiClassGroup.INVALID.card_classes == []


def test_get_localized_name():
	d = {
		locale.name: get_localized_name(CardClass.DRUID, locale.name) for locale in Locale
		if not locale.unused
	}

	assert d == {
		"deDE": "Druide",
		"enUS": "Druid",
		"esES": "Druida",
		"esMX": "Druida",
		"frFR": "Druide",
		"itIT": "Druido",
		"jaJP": "ドルイド",
		"koKR": "드루이드",
		"plPL": "Druid",
		"ptBR": "Druida",
		"ruRU": "Друид",
		"thTH": "ดรูอิด",
		"zhCN": "德鲁伊",
		"zhTW": "德魯伊"
	}
