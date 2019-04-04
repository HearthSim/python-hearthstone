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
		CardSet.BOOMSDAY, CardSet.TROLL,
	],
	ZodiacYear.DRAGON: [
		CardSet.CORE, CardSet.EXPERT1,
		CardSet.GILNEAS, CardSet.BOOMSDAY, CardSet.TROLL, CardSet.DALARAN
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
	ZodiacYear.DRAGON: datetime(2019, 4, 9),
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
	"ICC_047t": "ICC_047",
	"ICC_047t2": "ICC_047",
	# Lesser Amethyst Spellstone
	"LOOT_043t2": "LOOT_043",
	"LOOT_043t3": "LOOT_043",
	# Lesser Jasper Spellstone
	"LOOT_051t1": "LOOT_051",
	"LOOT_051t2": "LOOT_051",
	# Lesser Sapphire Spellstone
	"LOOT_064t1": "LOOT_064",
	"LOOT_064t2": "LOOT_064",
	# Lesser Emerald Spellstone
	"LOOT_080t2": "LOOT_080",
	"LOOT_080t3": "LOOT_080",
	# Lesser Pearl Spellstone
	"LOOT_091t1": "LOOT_091",
	"LOOT_091t2": "LOOT_091",
	# Lesser Ruby Spellstone
	"LOOT_103t1": "LOOT_103",
	"LOOT_103t2": "LOOT_103",
	# Lesser Mithril Spellstone
	"LOOT_203t2": "LOOT_203",
	"LOOT_203t3": "LOOT_203",
	# Unidentified Elixier
	"LOOT_278t1": "LOOT_278",
	"LOOT_278t2": "LOOT_278",
	"LOOT_278t3": "LOOT_278",
	"LOOT_278t4": "LOOT_278",
	# Unidentified Shield
	"LOOT_285t": "LOOT_285",
	"LOOT_285t2": "LOOT_285",
	"LOOT_285t3": "LOOT_285",
	"LOOT_285t4": "LOOT_285",
	# Unidentified Maul
	"LOOT_286t1": "LOOT_286",
	"LOOT_286t2": "LOOT_286",
	"LOOT_286t3": "LOOT_286",
	"LOOT_286t4": "LOOT_286",
	# Lesser Onyx Spellstone
	"LOOT_503t": "LOOT_503",
	"LOOT_503t2": "LOOT_503",
	# Lesser Diamond Spellstone
	"LOOT_507t": "LOOT_507",
	"LOOT_507t2": "LOOT_507",
	# Duskhaven Hunter
	"GIL_200t": "GIL_200",
	# Pumpkin Peasant
	"GIL_201t": "GIL_201",
	# Gilnean Royal Guard
	"GIL_202t": "GIL_202",
	# Swift Messenger
	"GIL_528t": "GIL_528",
	# Spellshifter
	"GIL_529t": "GIL_529",
	# Unidentified Contract
	"DAL_366t1": "DAL_366",
	"DAL_366t2": "DAL_366",
	"DAL_366t3": "DAL_366",
	"DAL_366t4": "DAL_366",
}


def get_original_card_id(card_id):
	return UPGRADABLE_CARDS_MAP.get(card_id, card_id)


SCHEME_CARDS = [
	"DAL_007",  # Rafaam's Scheme
	"DAL_008",  # Dr. Boom's Scheme
	"DAL_009",  # Hagatha's Scheme
	"DAL_010",  # Tagwaggle's Scheme
	"DAL_011",  # Lazul's Scheme
]
