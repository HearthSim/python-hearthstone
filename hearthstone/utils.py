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
