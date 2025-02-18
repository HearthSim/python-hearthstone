from datetime import datetime

from ..enums import CardClass, CardSet, Race, Rarity, ZodiacYear


try:
	from lxml import etree as ElementTree  # noqa
except ImportError:
	from xml.etree import ElementTree  # noqa


CARDCLASS_HERO_MAP = {
	CardClass.DEATHKNIGHT: "HERO_11",
	CardClass.DEMONHUNTER: "HERO_10",
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


# In the past, card names used to be predictably GLOBAL_CARD_SET_%CARDSET%. However in
# recent expansion, it uses a custom 3 letter set code instead.
CARDSET_GLOBAL_STRING_MAP = {
	CardSet.DRAGONS: "GLOBAL_CARD_SET_DRG",
	CardSet.YEAR_OF_THE_DRAGON: "GLOBAL_CARD_SET_YOD",
	CardSet.DEMON_HUNTER_INITIATE: "GLOBAL_CARD_SET_DHI",
	CardSet.BLACK_TEMPLE: "GLOBAL_CARD_SET_BT",
	CardSet.SCHOLOMANCE: "GLOBAL_CARD_SET_SCH",
	CardSet.DARKMOON_FAIRE: "GLOBAL_CARD_SET_DMF",
	CardSet.THE_BARRENS: "GLOBAL_CARD_SET_BAR",
	CardSet.STORMWIND: "GLOBAL_CARD_SET_SW",
	CardSet.ALTERAC_VALLEY: "GLOBAL_CARD_SET_AV",
	CardSet.THE_SUNKEN_CITY: "GLOBAL_CARD_SET_TSC",
	CardSet.WILD_WEST: "GLOBAL_CARD_SET_WST",
}


# The following dictionary is a consequence of Hearthstone adding multi-race cards.
#
# Before patch 25.0 Hearthstone only supported a single Race tag per card. However, in order
# to support an arbitrary number of Races per card the game developer has introduced a set
# of flag tags, that only exist to signify cards belonging to a specific race.
#
# For example, a card Wisp would be an "Undead Dragon" if it had the tags
# 2534 and 2523 set. However, in practice, one of these is still encoded using the Race tag,
# so likely such a card would have RACE = 11 (UNDEAD) and 2523 = 1 (DRAGON).
#
# If a new race is introduced, you're expected to add the tag here. You can find out the
# mapping by running patch processing and looking at the RaceTagMap.xml in the output
# directory.
CARDRACE_TAG_MAP = {
	Race.BLOODELF: 2524,
	Race.DRAENEI: 2525,
	Race.DWARF: 2526,
	Race.GNOME: 2527,
	Race.GOBLIN: 2528,
	Race.HUMAN: 2529,
	Race.NIGHTELF: 2530,
	Race.ORC: 2531,
	Race.TAUREN: 2532,
	Race.TROLL: 2533,
	Race.UNDEAD: 2534,
	Race.WORGEN: 2535,
	Race.GOBLIN2: None,
	Race.MURLOC: 2536,
	Race.DEMON: 2537,
	Race.SCOURGE: 2538,
	Race.MECHANICAL: 2539,
	Race.ELEMENTAL: 2540,
	Race.OGRE: 2541,
	Race.BEAST: 2542,
	Race.TOTEM: 2543,
	Race.NERUBIAN: 2544,
	Race.PIRATE: 2522,
	Race.DRAGON: 2523,
	Race.BLANK: None,
	Race.ALL: None,
	Race.EGG: 2545,
	Race.QUILBOAR: 2546,
	Race.CENTAUR: 2547,
	Race.FURBOLG: 2548,
	Race.HIGHELF: 2549,
	Race.TREANT: 2550,
	Race.OWLKIN: 2551,
	Race.HALFORC: 2552,
	Race.LOCK: None,
	Race.NAGA: 2553,
	Race.OLDGOD: 2554,
	Race.PANDAREN: 2555,
	Race.GRONN: 2556,
	Race.CELESTIAL: 2584,
	Race.GNOLL: 2585,
	Race.GOLEM: 2586,
	Race.HARPY: 2587,
	Race.VULPERA: 2588,
	# See comment at start of dictionary for how to identify the value for newly added races
}
REVERSE_CARDRACE_TAG_MAP = {v: k for k, v in CARDRACE_TAG_MAP.items()}


SECRET_COSTS = {
	CardClass.HUNTER: 2,
	CardClass.MAGE: 3,
	CardClass.PALADIN: 1,
	CardClass.ROGUE: 2,
	CardClass.WARRIOR: 0,
}

VISITING_TOURISTS = {
	CardClass.DEATHKNIGHT: ["VAC_503"],
	CardClass.DRUID: ["VAC_340"],
	CardClass.HUNTER: ["VAC_957", "WORK_013"],
	CardClass.MAGE: ["VAC_519"],
	CardClass.PALADIN: ["VAC_424"],
	CardClass.PRIEST: ["VAC_501"],
	CardClass.ROGUE: ["VAC_507", "WORK_063"],
	CardClass.SHAMAN: ["VAC_437"],
	CardClass.WARLOCK: ["VAC_336"],
	CardClass.WARRIOR: ["VAC_413"],
	CardClass.DEMONHUNTER: ["VAC_450"],
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
		CardSet.BASIC, CardSet.EXPERT1, CardSet.REWARD, CardSet.PROMO,
		CardSet.NAXX, CardSet.GVG, CardSet.BRM, CardSet.TGT, CardSet.LOE,
	],
	ZodiacYear.KRAKEN: [
		CardSet.BASIC, CardSet.EXPERT1,
		CardSet.BRM, CardSet.TGT, CardSet.LOE, CardSet.OG, CardSet.OG_RESERVE,
		CardSet.KARA, CardSet.KARA_RESERVE, CardSet.GANGS, CardSet.GANGS_RESERVE,
	],
	ZodiacYear.MAMMOTH: [
		CardSet.BASIC, CardSet.EXPERT1,
		CardSet.OG, CardSet.OG_RESERVE, CardSet.KARA, CardSet.KARA_RESERVE,
		CardSet.GANGS, CardSet.GANGS_RESERVE, CardSet.UNGORO, CardSet.ICECROWN,
		CardSet.LOOTAPALOOZA,
	],
	ZodiacYear.RAVEN: [
		CardSet.BASIC, CardSet.EXPERT1,
		CardSet.UNGORO, CardSet.ICECROWN, CardSet.LOOTAPALOOZA, CardSet.GILNEAS,
		CardSet.BOOMSDAY, CardSet.TROLL,
	],
	ZodiacYear.DRAGON: [
		CardSet.BASIC, CardSet.EXPERT1,
		CardSet.GILNEAS, CardSet.BOOMSDAY, CardSet.TROLL, CardSet.DALARAN, CardSet.ULDUM,
		CardSet.WILD_EVENT, CardSet.DRAGONS, CardSet.YEAR_OF_THE_DRAGON,
		CardSet.BLACK_TEMPLE, CardSet.DEMON_HUNTER_INITIATE,
	],
	ZodiacYear.PHOENIX: [
		CardSet.BASIC, CardSet.EXPERT1,
		CardSet.DALARAN, CardSet.ULDUM, CardSet.WILD_EVENT, CardSet.DRAGONS,
		CardSet.YEAR_OF_THE_DRAGON, CardSet.BLACK_TEMPLE, CardSet.DEMON_HUNTER_INITIATE,
		CardSet.SCHOLOMANCE, CardSet.DARKMOON_FAIRE,
	],
	ZodiacYear.GRYPHON: [
		CardSet.CORE,
		CardSet.BLACK_TEMPLE, CardSet.SCHOLOMANCE, CardSet.DARKMOON_FAIRE,
		CardSet.THE_BARRENS, CardSet.WAILING_CAVERNS, CardSet.STORMWIND,
		CardSet.ALTERAC_VALLEY,
	],
	ZodiacYear.HYDRA: [
		CardSet.CORE,
		CardSet.THE_BARRENS, CardSet.WAILING_CAVERNS, CardSet.STORMWIND,
		CardSet.ALTERAC_VALLEY, CardSet.THE_SUNKEN_CITY, CardSet.REVENDRETH,
		CardSet.RETURN_OF_THE_LICH_KING, CardSet.PATH_OF_ARTHAS,
		CardSet.BATTLE_OF_THE_BANDS,
	],
	ZodiacYear.WOLF: [
		CardSet.CORE,
		CardSet.THE_SUNKEN_CITY, CardSet.REVENDRETH, CardSet.RETURN_OF_THE_LICH_KING,
		CardSet.PATH_OF_ARTHAS, CardSet.BATTLE_OF_THE_BANDS, CardSet.TITANS,
		CardSet.WILD_WEST, CardSet.WHIZBANGS_WORKSHOP, CardSet.EVENT,
	],
	ZodiacYear.PEGASUS: [
		CardSet.CORE,
		CardSet.BATTLE_OF_THE_BANDS, CardSet.TITANS, CardSet.WILD_WEST,
		CardSet.EVENT, CardSet.WHIZBANGS_WORKSHOP, CardSet.ISLAND_VACATION,
		CardSet.SPACE, CardSet.EVENT, CardSet.EMERALD_DREAM
	],
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
	ZodiacYear.PHOENIX: datetime(2020, 4, 7),
	ZodiacYear.GRYPHON: datetime(2021, 3, 30),
	ZodiacYear.HYDRA: datetime(2022, 4, 12),
	ZodiacYear.WOLF: datetime(2023, 4, 11),
	ZodiacYear.PEGASUS: datetime(2024, 3, 19),
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
	# Galakrond
	"DRG_600t2": "DRG_600",
	"DRG_600t3": "DRG_600",
	"DRG_610t2": "DRG_610",
	"DRG_610t3": "DRG_610",
	"DRG_620t2": "DRG_620",
	"DRG_620t3": "DRG_620",
	"DRG_650t2": "DRG_650",
	"DRG_650t3": "DRG_650",
	"DRG_660t2": "DRG_660",
	"DRG_660t3": "DRG_660",
	# Corrupted Card
	"DMF_061t": "DMF_061",  # Faire Arborist
	"DMF_730t": "DMF_730",  # Moontouched Amulet
	"DMF_083t": "DMF_083",  # Dancing Cobra
	"DMF_101t": "DMF_101",  # Firework Elemental
	"DMF_054t": "DMF_054",  # Insight
	"DMF_184t": "DMF_184",  # Fairground Fool
	"DMF_517a": "DMF_517",  # Sweet Tooth
	"DMF_703t": "DMF_703",  # Pit Master
	"DMF_526a": "DMF_526",  # Stage Dive
	"DMF_073t": "DMF_073",  # Darkmoon Dirigible
	"DMF_082t": "DMF_082",  # Darkmoon Statue
	"DMF_174t": "DMF_174",  # Circus Medic
	"DMF_163t": "DMF_163",  # Carnival Clown
	# Cascading Disaster
	"DMF_117t2": "DMF_117",
	"DMF_117t": "DMF_117",
	"DMF_078t": "DMF_078",  # Strongman
	"DMF_186a": "DMF_186",  # Auspicious Spirits
	"DMF_118t": "DMF_118",  # Tickatus
	"DMF_247t": "DMF_247",  # Insatiable Felhound
	"DMF_248t": "DMF_248",  # Felsteel Executioner
	"DMF_064t": "DMF_064",  # Carousel Gryphon
	"DMF_124t": "DMF_124",  # Horrendous Growth
	"DMF_090t": "DMF_090",  # Don't Feed the Animals
	"DMF_105t": "DMF_105",  # Ring Toss
	"DMF_701t": "DMF_701",  # Dunk Tank
	"DMF_080t": "DMF_080",  # Fleethoof Pearltusk
	"DMF_244t": "DMF_244",  # Day at the Faire
	# Tame Beast
	"BAR_034t": "BAR_034",
	"BAR_034t2": "BAR_034",
	# Chain Lightning
	"BAR_044t": "BAR_044",
	"BAR_044t2": "BAR_044",
	# Flurry
	"BAR_305t": "BAR_305",
	"BAR_305t2": "BAR_305",
	# Condemn
	"BAR_314t": "BAR_314",
	"BAR_314t2": "BAR_314",
	# Wicked Stab
	"BAR_319t": "BAR_319",
	"BAR_319t2": "BAR_319",
	# Living Seed
	"BAR_536t": "BAR_536",
	"BAR_536t2": "BAR_536",
	# Conviction
	"BAR_880t": "BAR_880",
	"BAR_880t2": "BAR_880",
	# Conditioning
	"BAR_842t": "BAR_842",
	"BAR_842t2": "BAR_842",
	# Fury
	"BAR_891t": "BAR_891",
	"BAR_891t2": "BAR_891",
	# Imp Swarm
	"BAR_914t": "BAR_914",
	"BAR_914t2": "BAR_914",
	# Harmonic / Dissonant cards
	"ETC_314t": "ETC_314",  # Harmonic Pop
	"ETC_379t": "ETC_379",  # Harmonic Mood
	"ETC_427t": "ETC_427",  # Harmonic Metal
	"ETC_506t": "ETC_506",  # Harmonic Disco
	"ETC_717t": "ETC_717",  # Harmonic Hip Hop
	# Remixed Dispense-o-bot
	"JAM_000t": "JAM_000",  # Chilling Dispense-o-bot
	"JAM_000t2": "JAM_000",  # Merch Dispense-o-bot
	"JAM_000t3": "JAM_000",  # Money Dispense-o-bot
	"JAM_000t4": "JAM_000",  # Mystery Dispense-o-bot
	# Remixed Totemcarver
	"JAM_012t": "JAM_012",  # Loud Totemcarver
	"JAM_012t2": "JAM_012",  # Bluesy Totemcarver
	"JAM_012t3": "JAM_012",  # Blazing Totemcarver
	"JAM_012t4": "JAM_012",  # Karaoke Totemcarver
	# Remixed Tuning Fork
	"JAM_015t": "JAM_015",  # Sharpened Tuning Fork
	"JAM_015t2": "JAM_015",  # Reinforced Tuning Fork
	"JAM_015t3": "JAM_015",  # Curved Tuning Fork
	"JAM_015t4": "JAM_015",  # Backup Tuning Fork
	# Remixed Rhapsody
	"JAM_018t": "JAM_018",  # Angsty Rhapsody
	"JAM_018t2": "JAM_018",  # Resounding Rhapsody
	"JAM_018t3": "JAM_018",  # Emotional Rhapsody
	"JAM_018t4": "JAM_018",  # Wailing Rhapsody
	# Remixed Musician
	"JAM_033t": "JAM_033",  # Cathedral Musician
	"JAM_033t2": "JAM_033",  # Tropical Musician
	"JAM_033t3": "JAM_033",  # Romantic Musician
	"JAM_033t4": "JAM_033",  # Noise Musician
	# Lesser Opal Spellstone
	"TOY_645t": "TOY_645",
	"TOY_645t1": "TOY_645",
	# Lesser Spinel Spellstone
	"TOY_825t": "TOY_825",
	"TOY_825t2": "TOY_825",
	# Blossoms
	"TTN_950t3": "TTN_950",  # Forest Seedlings
	"TTN_930t": "TTN_930",  # Frost Lotus Seedling
	# Zilliax Deluxe 3000
	"TOY_330t5": "TOY_330",
	"TOY_330t6": "TOY_330",
	"TOY_330t7": "TOY_330",
	"TOY_330t8": "TOY_330",
	"TOY_330t9": "TOY_330",
	"TOY_330t10": "TOY_330",
	"TOY_330t11": "TOY_330",
	"TOY_330t12": "TOY_330",
}


def get_original_card_id(card_id):
	# Transfer Student
	if str(card_id).startswith("SCH_199t"):
		return "SCH_199"
	return UPGRADABLE_CARDS_MAP.get(card_id, card_id)


# A map of card ids that have been reprinted in the Wild format.
# Generated via scripts/dump_reprints.py
COPIED_CARDS_MAP_WILD = {
	"CORE_AT_021": "AT_021",
	"CORE_AT_061": "AT_061",
	"CORE_EX1_007": "WON_357",
	"CORE_KAR_065": "KAR_065",
	"CORE_LOE_012": "LOE_012",
	"EX1_007": "WON_357",
	"EX1_320": "WON_323",
	"EX1_354": "WON_048",
	"EX1_609": "WON_018",
	"NEW1_012": "WON_031",
	"VAN_NEW1_012": "WON_031",
	"WON_003": "AT_041",
	"WON_009": "OG_313",
	"WON_010": "OG_188",
	"WON_011": "GVG_035",
	"WON_012": "AT_045",
	"WON_021": "AT_062",
	"WON_022": "LOE_105",
	"WON_023": "AT_061",
	"WON_024": "AT_063",
	"WON_025": "AT_063t",
	"WON_029": "AT_006",
	"WON_033": "GVG_123",
	"WON_035": "GVG_004",
	"WON_036": "OG_087",
	"WON_037": "OG_090",
	"WON_038": "GVG_007",
	"WON_045": "KAR_057",
	"WON_046": "CFM_639",
	"WON_049": "AT_078",
	"WON_056": "LOE_006",
	"WON_057": "KAR_204",
	"WON_058": "AT_012",
	"WON_061": "AT_014",
	"WON_062": "GVG_009",
	"WON_063": "AT_018",
	"WON_067": "CFM_691",
	"WON_070": "CFM_690",
	"WON_071": "AT_033",
	"WON_073": "BRM_008",
	"WON_075": "OG_282",
	"WON_076": "AT_036",
	"WON_081": "AT_046",
	"WON_082": "CFM_707",
	"WON_083": "KAR_021",
	"WON_084": "CFM_312",
	"WON_085": "AT_049",
	"WON_086": "CFM_310",
	"WON_093": "AT_024",
	"WON_095": "GVG_015",
	"WON_096": "LOE_023",
	"WON_097": "OG_116",
	"WON_098": "KAR_205",
	"WON_099": "AT_021",
	"WON_100": "AT_025",
	"WON_105": "OG_121",
	"WON_108": "CFM_754",
	"WON_110": "CFM_752",
	"WON_111": "OG_301",
	"WON_114": "GVG_056",
	"WON_117": "CFM_643",
	"WON_118": "CFM_715",
	"WON_124": "OG_284",
	"WON_125": "OG_283",
	"WON_127": "OG_162",
	"WON_128": "FP1_012",
	"WON_130": "CFM_649",
	"WON_131": "OG_321",
	"WON_133": "BRM_028",
	"WON_134": "OG_131",
	"WON_135": "OG_280",
	"WON_136": "CFM_902",
	"WON_137": "CFM_685",
	"WON_162": "GVG_046",
	"WON_300": "CFM_816",
	"WON_302": "OG_202",
	"WON_303": "CFM_343",
	"WON_304": "OG_293",
	"WON_305": "KAR_065",
	"WON_306": "GVG_073",
	"WON_307": "CFM_336",
	"WON_308": "CFM_760",
	"WON_309": "KAR_077",
	"WON_310": "OG_310",
	"WON_311": "LOE_017",
	"WON_312": "CFM_815",
	"WON_313": "OG_334",
	"WON_314": "GVG_011",
	"WON_315": "OG_234",
	"WON_316": "AT_028",
	"WON_317": "OG_330",
	"WON_318": "AT_034",
	"WON_320": "AT_048",
	"WON_321": "AT_050",
	"WON_322": "OG_302",
	"WON_324": "CFM_750",
	"WON_325": "GVG_050",
	"WON_326": "CFM_631",
	"WON_328": "AT_090",
	"WON_329": "BRM_034",
	"WON_330": "OG_295",
	"WON_331": "CFM_321",
	"WON_332": "CFM_852",
	"WON_333": "OG_311",
	"WON_334": "AT_079",
	"WON_335": "FP1_025",
	"WON_336": "OG_209",
	"WON_337": "KAR_091",
	"WON_338": "BRM_016",
	"WON_339": "CFM_756",
	"WON_340": "LOE_012",
	"WON_341": "AT_001",
	"WON_342": "AT_015",
	"WON_344": "AT_007",
	"WON_347": "CFM_334",
	"WON_350": "CFM_940",
	"WON_351": "CFM_325",
	"WON_365": "CFM_039",
	"WON_366": "CFM_665"
}


def get_copied_card_id_by_format(card_id, format_type):
	"""Returns a suitable version for stat deduplication in the given FormatType."""
	if format_type == 1:
		return COPIED_CARDS_MAP_WILD.get(card_id, card_id)
	return card_id


SCHEME_CARDS = [
	"DAL_007",  # Rafaam's Scheme
	"DAL_008",  # Dr. Boom's Scheme
	"DAL_009",  # Hagatha's Scheme
	"DAL_010",  # Tagwaggle's Scheme
	"DAL_011",  # Lazul's Scheme
]

MAESTRA_DISGUISE_DBF_ID = 64674


if __name__ == "__main__":
	def _print_cs_dicts(dicts_and_names, tl_format, format):
		ret = []
		linefmt = "\t\t{ %d, %s }"
		for name, dict in dicts_and_names:
			keytype = int
			valtype = list(dict.values())[0].__class__

			lines = ",\n".join(
				linefmt % (keytype(key), valtype(value))
				for key, value in dict.items()
				if key is not None
			)
			ret.append(format % (name, lines))

		lines = "\n\n".join(ret)
		print(tl_format % (lines))

	print("using System.Collections.Generic;\n")

	_print_cs_dicts(
		[
			("TagRaceMap", REVERSE_CARDRACE_TAG_MAP)
		],
		"public static class RaceUtils {\n%s\n}",
		"\tpublic static Dictionary<int, Race> %s = new Dictionary<int, Race>() {\n%s\n\t};",
	)
