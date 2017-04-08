try:
	from lxml import etree as ElementTree  # noqa
except ImportError:
	from xml.etree import ElementTree  # noqa
from .enums import CardClass, Rarity


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
