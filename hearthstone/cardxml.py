from xml.etree import ElementTree
from .enums import (
	CardClass, CardType, CardSet, Faction, Race, Rarity, GameTag, PlayReq
)


class CardXML(object):
	def __init__(self, xml, locale="enUS"):
		self.xml = xml
		self.locale = locale
		self._localized_tags = {}
		self.tags = {}
		for e in self.xml.findall("./Tag"):
			tag = int(e.attrib["enumID"])
			try:
				tag = GameTag(tag)
			except ValueError:
				pass
			self.tags[tag] = self._get_tag(e)

		e = self.xml.findall("HeroPower")
		self.hero_power = e and e[0].attrib["cardID"] or None

		e = self.xml.findall("Power[PlayRequirement]/PlayRequirement")
		self.requirements = {
			PlayReq(int(t.attrib["reqID"])): int(t.attrib["param"] or 0) for t in e
		}

		self.choose_cards = [t.attrib["cardID"] for t in xml.findall("ChooseCard")]
		self.entourage = [t.attrib["cardID"] for t in xml.findall("EntourageCard")]

	def __str__(self):
		return self.name

	def __repr__(self):
		return "<%s: %r>" % (self.id, self.name)

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
	def id(self):
		return self.xml.attrib["CardID"]

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
	def elite(self):
		return bool(self.tags.get(GameTag.ELITE, False))

	@property
	def forgetful(self):
		return bool(self.tags.get(GameTag.FORGETFUL, False))

	@property
	def one_turn_effect(self):
		return bool(self.tags.get(GameTag.TAG_ONE_TURN_EFFECT, False))

	@property
	def poisonous(self):
		return bool(self.tags.get(GameTag.POISONOUS, False))

	@property
	def secret(self):
		return bool(self.tags.get(GameTag.SECRET, False))

	@property
	def spare_part(self):
		return bool(self.tags.get(GameTag.SPARE_PART, False))

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


def load(path, locale="enUS"):
	db = {}
	with open(path, "r", encoding="utf8") as f:
		xml = ElementTree.parse(f)
		for carddata in xml.findall("Entity"):
			card = CardXML(carddata, locale)
			db[card.id] = card
	return db, xml
