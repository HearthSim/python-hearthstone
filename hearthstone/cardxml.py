from xml.etree import ElementTree
from .enums import (
	CardClass, CardType, CardSet, Faction, Race, Rarity, GameTag, PlayReq
)


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
		self.requirements = {
			PlayReq(int(t.attrib["reqID"])): int(t.attrib["param"] or 0) for t in e
		}

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
		if not self.card_set.craftable:
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

	@property
	def card_class(self):
		return CardClass(self.tags.get(GameTag.CLASS, 0))

	@property
	def card_set(self):
		return CardSet(self.tags.get(GameTag.CARD_SET, 0))

	@property
	def faction(self):
		return Faction(self.tags.get(GameTag.FACTION, 0))

	@property
	def race(self):
		return Race(self.tags.get(GameTag.CARDRACE, 0))

	@property
	def rarity(self):
		return Rarity(self.tags.get(GameTag.RARITY, 0))

	@property
	def type(self):
		return CardType(self.tags.get(GameTag.CARDTYPE, 0))

	##
	# Bools

	@property
	def collectible(self):
		return bool(self.tags.get(GameTag.Collectible, False))

	@property
	def deathrattle(self):
		return bool(self.tags.get(GameTag.DEATHRATTLE, False))

	@property
	def double_spelldamage_bonus(self):
		return bool(self.tags.get(GameTag.RECEIVES_DOUBLE_SPELLDAMAGE_BONUS, False))

	@property
	def elite(self):
		return bool(self.tags.get(GameTag.ELITE, False))

	@property
	def evil_glow(self):
		return bool(self.tags.get(GameTag.EVIL_GLOW, False))

	@property
	def forgetful(self):
		return bool(self.tags.get(GameTag.FORGETFUL, False))

	@property
	def inspire(self):
		return bool(self.tags.get(GameTag.INSPIRE, False))

	@property
	def one_turn_effect(self):
		return bool(self.tags.get(GameTag.TAG_ONE_TURN_EFFECT, False))

	@property
	def poisonous(self):
		return bool(self.tags.get(GameTag.POISONOUS, False))

	@property
	def ritual(self):
		return bool(self.tags.get(GameTag.RITUAL, False))

	@property
	def secret(self):
		return bool(self.tags.get(GameTag.SECRET, False))

	@property
	def spare_part(self):
		return bool(self.tags.get(GameTag.SPARE_PART, False))

	@property
	def topdeck(self):
		return bool(self.tags.get(GameTag.TOPDECK, False))

	##
	# Tags

	@property
	def atk(self):
		return self.tags.get(GameTag.ATK, 0)

	@property
	def durability(self):
		return self.tags.get(GameTag.DURABILITY, 0)

	@property
	def cost(self):
		return self.tags.get(GameTag.COST, 0)

	@property
	def health(self):
		return self.tags.get(GameTag.HEALTH, 0)

	##
	# Auto-guessed extras

	@property
	def overload(self):
		return self.tags.get(GameTag.OVERLOAD, 0)

	@property
	def heropower_damage(self):
		return self.tags.get(GameTag.HEROPOWER_DAMAGE, 0)

	@property
	def spell_damage(self):
		return self.tags.get(GameTag.SPELLPOWER, 0)


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
