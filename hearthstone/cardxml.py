from xml.etree import ElementTree
from .enums import (
	CardClass, CardType, CardSet, Faction, GameTag, MultiClassGroup,
	Race, Rarity, PlayReq, Type
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


def _read_power_tag(e):
	ret = {"definition": e.attrib["definition"]}
	reqs = e.findall("PlayRequirement")
	if reqs is not None:
		ret["requirements"] = {}
		for pr in reqs:
			reqid = int(pr.attrib["reqID"])
			try:
				req = PlayReq(reqid)
			except ValueError:
				req = reqid
			ret["requirements"][req] = int(pr.attrib["param"] or 0)
	return ret


class CardXML(object):
	@classmethod
	def from_xml(cls, xml):
		id = xml.attrib["CardID"]
		self = cls(id)
		self.dbf_id = int(xml.attrib.get("ID", 0))

		self.tags = _build_tag_dict(xml, "./Tag")
		self.referenced_tags = _build_tag_dict(xml, "./ReferencedTag")

		e = xml.findall("MasterPower")
		self.master_power = e and e[0].text or None

		e = xml.findall("HeroPower")
		self.hero_power = e and e[0].attrib["cardID"] or None

		e = xml.findall("Texture")
		self.texture = e and e[0].text or ""

		e = xml.findall("Power")
		for power in e:
			self.powers.append(_read_power_tag(power))

		self.entourage = [t.attrib["cardID"] for t in xml.findall("EntourageCard")]
		return self

	def __init__(self, id, locale="enUS"):
		self.id = id
		self.dbf_id = 0
		self.tags = {}
		self.referenced_tags = {}
		self.master_power = None
		self.hero_power = None
		self.texture = ""
		self.entourage = []
		self.powers = []
		self.triggered_power_history_info = []

		self.locale = locale

	def __str__(self):
		return self.name

	def __repr__(self):
		return "<%s: %r>" % (self.id, self.name)

	def to_xml(self):
		ret = ElementTree.Element("Entity", CardID=self.id, ID=str(self.dbf_id), version="2")

		if self.master_power:
			master_power = ElementTree.SubElement(ret, "MasterPower")
			master_power.text = self.master_power

		for tag, value in self.tags.items():
			e = ElementTree.SubElement(ret, "Tag", enumID=str(int(tag)))
			if not isinstance(tag, GameTag):
				tag = GameTag(tag)

			e.attrib["name"] = tag.name

			if tag.type == Type.LOCSTRING:
				e.attrib["type"] = "LocString"
				for locale, localized_value in sorted(value.items()):
					loc_element = ElementTree.SubElement(e, locale)
					loc_element.text = localized_value
			elif tag.type == Type.STRING:
				e.attrib["type"] = "String"
				e.attrib["value"] = value
			else:
				e.attrib["type"] = "Int"
				e.attrib["value"] = str(int(value))

		if self.hero_power:
			ElementTree.SubElement(ret, "HeroPower", cardID=self.hero_power)

		for entourage in self.entourage:
			ElementTree.SubElement(ret, "EntourageCard", cardID=entourage)

		for power in self.powers:
			ep = ElementTree.SubElement(ret, "Power", definition=power["definition"])
			reqs = power.get("requirements", {})
			for reqid, param in reqs.items():
				er = ElementTree.SubElement(ep, "PlayRequirement", reqID=str(int(reqid)))
				if param:
					er.attrib["param"] = str(param)

		return ret

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

	@property
	def requirements(self):
		ret = {}
		for power in self.powers:
			for reqid, req in power.get("requirements", {}).items():
				ret[reqid] = req
		return ret

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
			card = CardXML.from_xml(carddata)
			card.locale = locale
			db[card.id] = card
	return db, xml
