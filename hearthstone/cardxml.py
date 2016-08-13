from xml.etree import ElementTree
from .enums import (
	CardClass, CardType, CardSet, Faction, Race, Rarity, GameTag, PlayReq
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


class CardXML(object):
	def __init__(self, locale="enUS"):
		self.locale = locale
		self._localized_tags = {}

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

		self.tags = self._build_tag_dict("./Tag")
		self.referenced_tags = self._build_tag_dict("./ReferencedTag")

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

	def _build_tag_dict(self, xpath):
		tags = {}
		for e in self.xml.findall(xpath):
			tag = int(e.attrib["enumID"])
			try:
				tag = GameTag(tag)
			except ValueError:
				pass
			tags[tag] = self._get_tag(e)

		return tags

	def _find_tag(self, id):
		return self.xml.find('./Tag[@enumID="%i"]' % (id))

	def _get_tag(self, element):
		type = element.attrib.get("type", "Int")

		if type == "Card":
			return element.attrib["value"]

		if type == "String":
			return element.text

		if type == "LocString":
			e = element.find(self.locale)
			if e is None:
				e = element.find("enUS")
			return e.text

		value = int(element.attrib["value"])
		if type == "Bool":
			return bool(value)

		return value

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

	def get_localized_tag(self, tag):
		if tag not in self._localized_tags:
			self._localized_tags[tag] = {}
		if self.locale not in self._localized_tags[tag]:
			e = self.xml.find('./Tag[@enumID="%i"]' % (tag))
			if e is not None:
				value = self._get_tag(e)
				self._localized_tags[tag][self.locale] = value
		return self._localized_tags[tag].get(self.locale, "")

	@property
	def name(self):
		return self.get_localized_tag(GameTag.CARDNAME)

	@property
	def description(self):
		return self.get_localized_tag(GameTag.CARDTEXT_INHAND)

	@property
	def flavortext(self):
		return self.get_localized_tag(GameTag.FLAVORTEXT)

	@property
	def how_to_earn(self):
		return self.get_localized_tag(GameTag.HOW_TO_EARN)

	@property
	def how_to_earn_golden(self):
		return self.get_localized_tag(GameTag.HOW_TO_EARN_GOLDEN)

	@property
	def playtext(self):
		return self.get_localized_tag(GameTag.CardTextInPlay)

	@property
	def targeting_arrow_text(self):
		return self.get_localized_tag(GameTag.TARGETING_ARROW_TEXT)

	@property
	def artist(self):
		return self.tags.get(GameTag.ARTISTNAME, "")

	@property
	def localization_notes(self):
		return self.tags.get(GameTag.LocalizationNotes, "")

	##
	# Enums

	card_class = prop(GameTag.CLASS, CardClass)
	card_set = prop(GameTag.CARD_SET, CardSet)
	faction = prop(GameTag.FACTION, Faction)
	race = prop(GameTag.CARDRACE, Race)
	rarity = prop(GameTag.RARITY, Rarity)
	type = prop(GameTag.CARDTYPE, CardType)

	##
	# Bools

	appear_functionally_dead = prop(GameTag.APPEAR_FUNCTIONALLY_DEAD, bool)
	cant_be_fatigued = prop(GameTag.CANT_BE_FATIGUED, bool)
	collectible = prop(GameTag.Collectible, bool)
	battlecry = prop(GameTag.BATTLECRY, bool)
	deathrattle = prop(GameTag.DEATHRATTLE, bool)
	divine_shield = prop(GameTag.DIVINE_SHIELD, bool)
	double_spelldamage_bonus = prop(GameTag.RECEIVES_DOUBLE_SPELLDAMAGE_BONUS, bool)
	elite = prop(GameTag.ELITE, bool)
	evil_glow = prop(GameTag.EVIL_GLOW, bool)
	forgetful = prop(GameTag.FORGETFUL, bool)
	inspire = prop(GameTag.INSPIRE, bool)
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
