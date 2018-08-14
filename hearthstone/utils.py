from datetime import datetime

from .enums import CardClass, CardSet, Rarity, ZodiacYear


try:
	from lxml import etree as ElementTree  # noqa
except ImportError:
	from xml.etree import ElementTree  # noqa


CARDCLASS_HERO_MAP = {
	CardClass.DRUID: "HERO_06",
	CardClass.HUNTER: "HERO_05",
	CardClass.MAGE: "HERO_08",
	CardClass.PALADIN: "HERO_04",
	CardClass.PRIEST: "HERO_09",
	CardClass.ROGUE: "HERO_03",
	CardClass.SHAMAN: "HERO_02",
	CardClass.WARLOCK: "HERO_07",
	CardClass.WARRIOR: "HERO_01",
	CardClass.WHIZBANG: "BOT_914h",
}


SECRET_COSTS = {
	CardClass.HUNTER: 2,
	CardClass.MAGE: 3,
	CardClass.PALADIN: 1,
	CardClass.ROGUE: 2,
	CardClass.WARRIOR: 0,
}


CRAFTING_COSTS = {
	Rarity.COMMON: (40, 400),
	Rarity.RARE: (100, 800),
	Rarity.EPIC: (400, 1600),
	Rarity.LEGENDARY: (1600, 3200),
}

DISENCHANT_COSTS = {
	Rarity.COMMON: (5, 50),
	Rarity.RARE: (20, 100),
	Rarity.EPIC: (100, 400),
	Rarity.LEGENDARY: (400, 1600),
}


STANDARD_SETS = {
	ZodiacYear.PRE_STANDARD: [
		CardSet.CORE, CardSet.EXPERT1, CardSet.REWARD, CardSet.PROMO,
		CardSet.NAXX, CardSet.GVG, CardSet.BRM, CardSet.TGT, CardSet.LOE,
	],
	ZodiacYear.KRAKEN: [
		CardSet.CORE, CardSet.EXPERT1,
		CardSet.BRM, CardSet.TGT, CardSet.LOE, CardSet.OG, CardSet.OG_RESERVE,
		CardSet.KARA, CardSet.KARA_RESERVE, CardSet.GANGS, CardSet.GANGS_RESERVE,
	],
	ZodiacYear.MAMMOTH: [
		CardSet.CORE, CardSet.EXPERT1,
		CardSet.OG, CardSet.OG_RESERVE, CardSet.KARA, CardSet.KARA_RESERVE,
		CardSet.GANGS, CardSet.GANGS_RESERVE, CardSet.UNGORO, CardSet.ICECROWN,
		CardSet.LOOTAPALOOZA,
	],
	ZodiacYear.RAVEN: [
		CardSet.CORE, CardSet.EXPERT1,
		CardSet.UNGORO, CardSet.ICECROWN, CardSet.LOOTAPALOOZA, CardSet.GILNEAS,
		CardSet.BOOMSDAY,
	]
}


try:
	_EPOCH = datetime.fromtimestamp(0)
except OSError:
	# https://bugs.python.org/issue29097 (Windows-only)
	_EPOCH = datetime.fromtimestamp(86400)


ZODIAC_ROTATION_DATES = {
	ZodiacYear.PRE_STANDARD: _EPOCH,
	ZodiacYear.KRAKEN: datetime(2016, 4, 26),
	ZodiacYear.MAMMOTH: datetime(2017, 4, 7),
	ZodiacYear.RAVEN: datetime(2018, 4, 12),
}


# QuestController.cs
QUEST_REWARDS = {
	"UNG_940": "UNG_940t8",
	"UNG_954": "UNG_954t1",
	"UNG_934": "UNG_934t1",
	"UNG_829": "UNG_829t1",
	"UNG_028": "UNG_028t",
	"UNG_067": "UNG_067t1",
	"UNG_116": "UNG_116t",
	"UNG_920": "UNG_920t1",
	"UNG_942": "UNG_942t",
}


# GameplayStringTextBuilder.cs

SPELLSTONE_STRINGS = {
	"LOOT_043": "GAMEPLAY_AMETHYST_SPELLSTONE_%d",
	"LOOT_051": "GAMEPLAY_JASPER_SPELLSTONE_%d",
	"LOOT_064": "GAMEPLAY_SAPPHIRE_SPELLSTONE_%d",
	"LOOT_091": "GAMEPLAY_PEARL_SPELLSTONE_%d",
	"LOOT_103": "GAMEPLAY_RUBY_SPELLSTONE_%d",
	"LOOT_503": "GAMEPLAY_ONYX_SPELLSTONE_%d",
	"LOOT_507": "GAMEPLAY_DIAMOND_SPELLSTONE_%d",
	"LOOT_526d": "GAMEPLAY_LOOT_526d_DARKNESS_%d",
}


UPGRADABLE_CARDS_MAP = {
	# Fatespinner
	43430: 42615,
	43431: 42615,
	# Unidentified Elixier
	45751: 45759,
	45753: 45759,
	45756: 45759,
	45757: 45759,
	# Unidentified Shield
	45770: 45775,
	45771: 45775,
	45773: 45775,
	45774: 45775,
	# Unidentified Maul
	45777: 45782,
	45778: 45782,
	45779: 45782,
	45780: 45782,
	# Lesser Jasper Spellstone
	43289: 43288,
	43290: 43288,
	# Lesser Pearl Spellstone
	43380: 43382,
	43381: 43382,
	# Lesser Ruby Spellstone
	43411: 43414,
	43412: 43414,
	# Lesser Amethyst Spellstone
	43275: 43272,
	43276: 43272,
	# Lesser Emerald Spellstone
	43361: 43363,
	43362: 43363,
	# Lesser Onyx Spellstone
	46295: 46296,
	46297: 46296,
	# Lesser Diamond Spellstone
	46306: 46307,
	46308: 46307,
	# Lesser Mithril Spellstone
	46063: 45519,
	46064: 45519,
	# Lesser Sapphire Spellstone
	43332: 43331,
	43333: 43331,
	# Duskhaven Hunter
	46597: 46596,
	# Pumpkin Peasant
	46600: 46598,
	# Swift Messenger
	46993: 46992,
	# Spellshifter
	46995: 46994,
	# Gilnean Royal Guard
	46602: 46601
}


def get_initial_dbf_id(dbf_id):
	return UPGRADABLE_CARDS_MAP.get(dbf_id, dbf_id)
