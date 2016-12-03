from xml.etree import ElementTree
from .enums import (
	CardClass, CardType, CardSet, Faction, GameTag, MultiClassGroup,
	Race, Rarity, PlayReq
)


def prop(tag, cast=int):
	def _func(self):
		value = self.tags.get(tag, 0)
		try:
			return cast(value)
		except ValueError:
			# The enum value is most likely just missing
			return value
	return property(_func)


def _locstring(tag):
	def _func(self):
		value = self.tags.get(tag, {})
		if self.locale in value:
			return value[self.locale]
		return value.get("enUS", "")
	return property(_func)


def _build_tag_dict(xml, xpath):
	"""
	Given an Entity XML element and an XPath, return the XPath as dict of tags
	"""
	tags = {}
	for e in xml.findall(xpath):
		tag = int(e.attrib["enumID"])
		try:
			tag = GameTag(tag)
		except ValueError:
			pass
		tags[tag] = _unpack_tag_xml(e)

	return tags


def _unpack_tag_xml(element):
	"""
	Unpack a single tag element into its value.
	"""
	type = element.attrib.get("type", "Int")

	if type == "Card":
		return element.attrib["value"]

	if type == "String":
		return element.text

	if type == "LocString":
		ret = {}
		for e in element:
			ret[e.tag] = e.text
		return ret

	value = int(element.attrib["value"])
	if type == "Bool":
		return bool(value)

	return value


class CardXML(object):
	def __init__(self, locale="enUS"):
		self.locale = locale

		self.dbf_id = 0
		self.tags = {}
		self.referenced_tags = {}
		self.master_power = None
		self.hero_power = None
		self.texture = ""
		self.requirements = {}
		self.entourage = {}

	def load_xml(self, xml):
		self.xml = xml

		self.id = self.xml.attrib["CardID"]
		self.dbf_id = int(self.xml.attrib.get("ID", 0))

		self.tags = _build_tag_dict(xml, "./Tag")
		self.referenced_tags = _build_tag_dict(xml, "./ReferencedTag")

		e = self.xml.findall("MasterPower")
		self.master_power = e and e[0].text or None

		e = self.xml.findall("HeroPower")
		self.hero_power = e and e[0].attrib["cardID"] or None

		e = self.xml.findall("Texture")
		self.texture = e and e[0].text or ""

		e = self.xml.findall("Power[PlayRequirement]/PlayRequirement")
		self.requirements = {}
		for t in e:
			reqid = int(t.attrib["reqID"])
			try:
				req = PlayReq(reqid)
			except ValueError:
				req = reqid
			self.requirements[req] = int(t.attrib["param"] or 0)

		self.entourage = [t.attrib["cardID"] for t in xml.findall("EntourageCard")]

	def __str__(self):
		return self.name

	def __repr__(self):
		return "<%s: %r>" % (self.id, self.name)

	@property
	def craftable(self):
		if isinstance(self.card_set, CardSet) and not self.card_set.craftable:
			return False
		if not self.type.craftable:
			return False
		if not self.rarity.craftable:
			return False
		return True

	@property
	def crafting_costs(self):
		if not self.craftable:
			return 0, 0
		return self.rarity.crafting_costs

	@property
	def disenchant_costs(self):
		if not self.craftable:
			return 0, 0
		return self.rarity.disenchant_costs

	@property
	def max_count_in_deck(self):
		"""
		The maximum amount of times the card can be present in a deck.
		"""
		if self.rarity == Rarity.LEGENDARY:
			return 1
		return 2

	##
	# Localized values

	name = _locstring(GameTag.CARDNAME)
	description = _locstring(GameTag.CARDTEXT_INHAND)
	flavortext = _locstring(GameTag.FLAVORTEXT)
	how_to_earn = _locstring(GameTag.HOW_TO_EARN)
	how_to_earn_golden = _locstring(GameTag.HOW_TO_EARN_GOLDEN)
	playtext = _locstring(GameTag.CardTextInPlay)
	targeting_arrow_text = _locstring(GameTag.TARGETING_ARROW_TEXT)

	@property
	def artist(self):
		return self.tags.get(GameTag.ARTISTNAME, "")

	@property
	def localization_notes(self):
		return self.tags.get(GameTag.LocalizationNotes, "")

	@property
	def classes(self):
		ret = []
		multiclass = self.multiple_classes
		if not multiclass:
			ret.append(self.card_class)
		else:
			i = 1
			while multiclass != 0:
				if (multiclass & 1) == 1 and i in CardClass._value2member_map_:
					ret.append(CardClass(i))
				multiclass >>= 1
				i += 1

		return ret

	##
	# Enums

	card_class = prop(GameTag.CLASS, CardClass)
	card_set = prop(GameTag.CARD_SET, CardSet)
	faction = prop(GameTag.FACTION, Faction)
	race = prop(GameTag.CARDRACE, Race)
	rarity = prop(GameTag.RARITY, Rarity)
	type = prop(GameTag.CARDTYPE, CardType)
	multi_class_group = prop(GameTag.MULTI_CLASS_GROUP, MultiClassGroup)

	##
	# Bools

	appear_functionally_dead = prop(GameTag.APPEAR_FUNCTIONALLY_DEAD, bool)
	autoattack = prop(GameTag.AUTOATTACK, bool)
	cant_be_fatigued = prop(GameTag.CANT_BE_FATIGUED, bool)
	collectible = prop(GameTag.COLLECTIBLE, bool)
	battlecry = prop(GameTag.BATTLECRY, bool)
	deathrattle = prop(GameTag.DEATHRATTLE, bool)
	discover = prop(GameTag.DISCOVER, bool)
	divine_shield = prop(GameTag.DIVINE_SHIELD, bool)
	double_spelldamage_bonus = prop(GameTag.RECEIVES_DOUBLE_SPELLDAMAGE_BONUS, bool)
	elite = prop(GameTag.ELITE, bool)
	evil_glow = prop(GameTag.EVIL_GLOW, bool)
	forgetful = prop(GameTag.FORGETFUL, bool)
	immune = prop(GameTag.IMMUNE, bool)
	inspire = prop(GameTag.INSPIRE, bool)
	jade_golem = prop(GameTag.JADE_GOLEM, bool)
	one_turn_effect = prop(GameTag.TAG_ONE_TURN_EFFECT, bool)
	poisonous = prop(GameTag.POISONOUS, bool)
	ritual = prop(GameTag.RITUAL, bool)
	secret = prop(GameTag.SECRET, bool)
	spare_part = prop(GameTag.SPARE_PART, bool)
	taunt = prop(GameTag.TAUNT, bool)
	topdeck = prop(GameTag.TOPDECK, bool)
	untouchable = prop(GameTag.UNTOUCHABLE, bool)

	##
	# Tags

	atk = prop(GameTag.ATK)
	durability = prop(GameTag.DURABILITY)
	cost = prop(GameTag.COST)
	health = prop(GameTag.HEALTH)
	windfury = prop(GameTag.WINDFURY)

	##
	# Auto-guessed extras

	overload = prop(GameTag.OVERLOAD)
	heropower_damage = prop(GameTag.HEROPOWER_DAMAGE)
	spell_damage = prop(GameTag.SPELLPOWER)

	##
	# Misc

	multiple_classes = prop(GameTag.MULTIPLE_CLASSES)
	script_data_num_1 = prop(GameTag.TAG_SCRIPT_DATA_NUM_1)

	# Faction bools
	grimy_goons = prop(GameTag.GRIMY_GOONS, bool)
	jade_lotus = prop(GameTag.JADE_LOTUS, bool)
	kabal = prop(GameTag.KABAL, bool)


def load(path=None, locale="enUS"):
	if path is None:
		from pkg_resources import resource_filename
		path = resource_filename("hearthstone", "CardDefs.xml")

	db = {}
	with open(path, "r", encoding="utf8") as f:
		xml = ElementTree.parse(f)
		for carddata in xml.findall("Entity"):
			card = CardXML(locale)
			card.load_xml(carddata)
			db[card.id] = card
	return db, xml
