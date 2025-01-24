import tempfile
from typing import Any, Callable, Iterator, Optional, Sequence, Tuple

from .enums import (
	CardClass, CardSet, CardType, Faction, GameTag,
	MultiClassGroup, Race, Rarity, Role, SpellSchool
)
from .utils import ElementTree
from .xmlutils import download_to_tempfile_retry


LOCALIZED_TAGS = [
	GameTag.CARDNAME, GameTag.CARDTEXT_INHAND, GameTag.FLAVORTEXT,
	GameTag.HOW_TO_EARN, GameTag.HOW_TO_EARN_GOLDEN,
	GameTag.CardTextInPlay, GameTag.TARGETING_ARROW_TEXT,
]

STRING_TAGS = [GameTag.ARTISTNAME, GameTag.LocalizationNotes]


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
		value = self.strings[tag]
		if self.locale in value:
			return value[self.locale]
		return value.get("enUS", "")
	return property(_func)


def _make_tag_element(element, tagname, tag, value):
	e = ElementTree.SubElement(element, tagname, enumID=str(int(tag)))
	if not isinstance(tag, GameTag):
		try:
			tag = GameTag(tag)
			name = tag.name
			value = str(int(value))
		except ValueError:
			name = str(value)
			value = str(value)
	else:
		name = tag.name
		value = str(int(value))

	e.attrib["name"] = name
	e.attrib["type"] = "Int"
	e.attrib["value"] = value

	return e


def _unpack_tag_xml(e):
	value = int(e.attrib["enumID"])
	try:
		tag = GameTag(value)
	except ValueError:
		tag = value
	type = e.attrib.get("type", "Int")
	value = int(e.attrib.get("value") or 0)
	if type == "Bool":
		value = bool(value)
	return tag, type, value


class CardXML:
	@classmethod
	def from_xml(cls, xml):
		id = xml.attrib["CardID"]
		self = cls(id)
		self.dbf_id = int(xml.attrib.get("ID", 0))

		for e in xml.findall("./Tag"):
			tag, type, value = _unpack_tag_xml(e)
			if type == "String":
				self.strings[tag] = e.text
			elif type == "LocString":
				for loc_element in e:
					self.strings[tag][loc_element.tag] = loc_element.text
			else:
				if tag == GameTag.HERO_POWER:
					self.hero_power = e.attrib.get("cardID")
				self.tags[tag] = value

		for e in xml.findall("./ReferencedTag"):
			tag, type, value = _unpack_tag_xml(e)
			self.referenced_tags[tag] = value

		if self.hero_power is None and self.tags.get(GameTag.HERO_POWER):
			i = int(GameTag.HERO_POWER)
			t = xml.findall('./Tag[@enumID="%i"]' % (i))
			if t is not None:
				self.hero_power = t[0].attrib.get("cardID")

		return self

	def __init__(self, id, locale="enUS"):
		self.card_id = self.id = id
		self.dbf_id = 0
		self.version = 2
		self.tags = {}
		self.hero_power = None
		self.referenced_tags = {}

		self.locale = locale

		self.strings = {
			GameTag.CARDNAME: {},
			GameTag.CARDTEXT_INHAND: {},
			GameTag.FLAVORTEXT: {},
			GameTag.HOW_TO_EARN: {},
			GameTag.HOW_TO_EARN_GOLDEN: {},
			GameTag.CardTextInPlay: {},
			GameTag.TARGETING_ARROW_TEXT: {},
			GameTag.ARTISTNAME: "",
			GameTag.LocalizationNotes: "",
		}

	def __str__(self):
		return self.name

	def __repr__(self):
		return "<%s: %r>" % (self.id, self.name)

	def to_xml(
		self,
		tags: Optional[Sequence[GameTag]] = None,
		locales: Optional[Sequence[str]] = None
	):
		ret = ElementTree.Element("Entity", CardID=self.id, ID=str(self.dbf_id))
		if self.version:
			ret.attrib["version"] = str(self.version)

		for tag in LOCALIZED_TAGS:
			if tags is not None and tag not in tags:
				continue

			value = self.strings[tag]
			if value:
				e = ElementTree.SubElement(ret, "Tag", enumID=str(int(tag)), name=tag.name)
				e.attrib["type"] = "LocString"
				for locale, localized_value in sorted(value.items()):
					if locales is not None and locale not in locales:
						continue

					if localized_value:
						loc_element = ElementTree.SubElement(e, locale)
						loc_element.text = str(localized_value)

		for tag in STRING_TAGS:
			if tags is not None and tag not in tags:
				continue

			value = self.strings[tag]
			if value:
				e = ElementTree.SubElement(ret, "Tag", enumID=str(int(tag)), name=tag.name)
				e.attrib["type"] = "String"
				e.text = value

		for tag, value in sorted(self.tags.items()):
			if tags is not None and tag not in tags:
				continue

			if value:
				e = _make_tag_element(ret, "Tag", tag, value)

				if tag == GameTag.HERO_POWER and self.hero_power:
					e.attrib["type"] = "Card"
					e.attrib["cardID"] = self.hero_power

		for tag, value in sorted(self.referenced_tags.items()):
			if tags and tag not in tags:
				continue

			e = _make_tag_element(ret, "ReferencedTag", tag, value)

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
	def quest_reward(self):
		from .utils import QUEST_REWARDS
		return QUEST_REWARDS.get(self.card_id, "")

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
		return self.strings[GameTag.ARTISTNAME]

	@property
	def localization_notes(self):
		return self.strings[GameTag.LocalizationNotes]

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

	@property
	def races(self):
		ret = []

		for tag, value in self.tags.items():
			if tag == GameTag.CARDRACE:
				ret.append(Race(value))
				continue

			potential_race_tag = Race.get_race_for_game_tag(tag)
			if potential_race_tag is not None:
				ret.append(Race(potential_race_tag))

		return sorted(ret, key=lambda r: r.text_order)

	@property
	def english_name(self):
		return self.strings[GameTag.CARDNAME].get("enUS", "")

	@property
	def english_description(self):
		return self.strings[GameTag.CARDTEXT_INHAND].get("enUS", "")

	def is_functional_duplicate_of(self, other):
		"""
		This method can be used to check whether two cards are functionally identical from a
		Constructed gameplay perspective. For example, if cards have the same English name,
		description, stats and races, they're probably the same. However, if for example the
		mana costs differ, the card is different because one card is strictly better than
		another one and can be played in different circumstances.
		You can use this method catch cases where cards are reprinted in different sets and
		may otherwise appear as duplicates (e.g. by looking at
		GameTag.DECK_RULE_COUNT_AS_COPY_OF_CARD_ID).
		"""
		if not isinstance(other, CardXML):
			raise ValueError("other must be a CardXML instance")

		english_name = self.english_name
		return (
			english_name and
			other.english_name == english_name and
			other.description == self.description and
			other.cost == self.cost and
			other.health == self.health and
			other.atk == self.atk and
			other.type == self.type and
			set(other.races) == set(self.races)
		)

	##
	# Enums

	card_class = prop(GameTag.CLASS, CardClass)
	card_set = prop(GameTag.CARD_SET, CardSet)
	faction = prop(GameTag.FACTION, Faction)
	race = prop(GameTag.CARDRACE, Race)
	rarity = prop(GameTag.RARITY, Rarity)
	type = prop(GameTag.CARDTYPE, CardType)
	multi_class_group = prop(GameTag.MULTI_CLASS_GROUP, MultiClassGroup)
	spell_school = prop(GameTag.SPELL_SCHOOL, SpellSchool)
	role = prop(GameTag.LETTUCE_ROLE, Role)

	##
	# Bools

	adapt = prop(GameTag.ADAPT, bool)
	appear_functionally_dead = prop(GameTag.APPEAR_FUNCTIONALLY_DEAD, bool)
	autoattack = prop(GameTag.AUTOATTACK, bool)
	can_summon_maxplusone_minion = prop(GameTag.CAN_SUMMON_MAXPLUSONE_MINION, bool)
	cant_be_attacked = prop(GameTag.CANT_BE_ATTACKED, bool)
	cant_be_fatigued = prop(GameTag.CANT_BE_FATIGUED, bool)
	collectible = prop(GameTag.COLLECTIBLE, bool)
	colossal = prop(GameTag.COLOSSAL, bool)
	battlecry = prop(GameTag.BATTLECRY, bool)
	choose_one = prop(GameTag.CHOOSE_ONE, bool)
	combo = prop(GameTag.COMBO, bool)
	corrupt = prop(GameTag.CORRUPT, bool)
	deathrattle = prop(GameTag.DEATHRATTLE, bool)
	discover = prop(GameTag.DISCOVER, bool)
	divine_shield = prop(GameTag.DIVINE_SHIELD, bool)
	double_spelldamage_bonus = prop(GameTag.RECEIVES_DOUBLE_SPELLDAMAGE_BONUS, bool)
	dredge = prop(GameTag.DREDGE, bool)
	echo = prop(GameTag.ECHO, bool)
	elite = prop(GameTag.ELITE, bool)
	elusive = prop(GameTag.ELUSIVE, bool)
	evil_glow = prop(GameTag.EVIL_GLOW, bool)
	forge = prop(GameTag.FORGE, bool)
	forgetful = prop(GameTag.FORGETFUL, bool)
	ghostly = prop(GameTag.GHOSTLY, bool)
	hide_health = prop(GameTag.HIDE_HEALTH, bool)
	hide_stats = prop(GameTag.HIDE_STATS, bool)
	hide_cost = prop(GameTag.HIDE_COST, bool)
	immune = prop(GameTag.IMMUNE, bool)
	inspire = prop(GameTag.INSPIRE, bool)
	jade_golem = prop(GameTag.JADE_GOLEM, bool)
	lifesteal = prop(GameTag.LIFESTEAL, bool)
	magnetic = prop(GameTag.MODULAR, bool)
	miniaturize = prop(GameTag.MINIATURIZE, bool)
	one_turn_effect = prop(GameTag.TAG_ONE_TURN_EFFECT, bool)
	outcast = prop(GameTag.OUTCAST, bool)
	overheal = prop(GameTag.OVERHEAL, bool)
	overkill = prop(GameTag.OVERKILL, bool)
	poisonous = prop(GameTag.POISONOUS, bool)
	quest = prop(GameTag.QUEST, bool)
	reborn = prop(GameTag.REBORN, bool)
	ritual = prop(GameTag.RITUAL, bool)
	rush = prop(GameTag.RUSH, bool)
	secret = prop(GameTag.SECRET, bool)
	sidequest = prop(GameTag.SIDEQUEST, bool)
	spare_part = prop(GameTag.SPARE_PART, bool)
	spellburst = prop(GameTag.SPELLBURST, bool)
	start_of_game = prop(GameTag.START_OF_GAME, bool)
	taunt = prop(GameTag.TAUNT, bool)
	titan = prop(GameTag.TITAN, bool)
	topdeck = prop(GameTag.TOPDECK, bool)
	tradeable = prop(GameTag.TRADEABLE, bool)
	twinspell = prop(GameTag.TWINSPELL, bool)
	untouchable = prop(GameTag.UNTOUCHABLE, bool)
	venomous = prop(GameTag.VENOMOUS, bool)

	##
	# Tags

	armor = prop(GameTag.ARMOR)
	atk = prop(GameTag.ATK)
	avenge = prop(GameTag.AVENGE)
	durability = prop(GameTag.DURABILITY)
	cost = prop(GameTag.COST)
	health = prop(GameTag.HEALTH)
	manathirst = prop(GameTag.MANATHIRST)
	windfury = prop(GameTag.WINDFURY)
	quest_progress_total = prop(GameTag.QUEST_PROGRESS_TOTAL)
	cooldown = prop(GameTag.LETTUCE_COOLDOWN_CONFIG)

	##
	# Auto-guessed extras

	overload = prop(GameTag.OVERLOAD)
	heropower_damage = prop(GameTag.HEROPOWER_DAMAGE)
	spell_damage = prop(GameTag.SPELLPOWER)

	##
	# Misc

	multiple_classes = prop(GameTag.MULTIPLE_CLASSES)
	script_data_num_1 = prop(GameTag.TAG_SCRIPT_DATA_NUM_1)

	# Faction bools - deprecated, use multi_class_group instead
	grimy_goons = prop(GameTag.GRIMY_GOONS, bool)
	jade_lotus = prop(GameTag.JADE_LOTUS, bool)
	kabal = prop(GameTag.KABAL, bool)


cardid_cache: dict = {}
dbf_cache: dict = {}


XML_URL = "https://api.hearthstonejson.com/v1/latest/CardDefs.xml"


def _bootstrap_from_web(parse: Callable[[Iterator[Tuple[str, Any]]], None], url=None):
	if url is None:
		url = XML_URL

	with tempfile.TemporaryFile(mode="rb+") as fp:
		if download_to_tempfile_retry(url, fp):
			fp.flush()
			fp.seek(0)

			parse(ElementTree.iterparse(fp, events=("start", "end",)))


def _bootstrap_from_library(parse: Callable[[Iterator[Tuple[str, Any]]], None], path=None):
	from hearthstone_data import get_carddefs_path

	if path is None:
		path = get_carddefs_path()

	with open(path, "rb") as f:
		parse(ElementTree.iterparse(f, events=("start", "end",)))


def _load(path, locale, cache, attr, url=None):
	cache_key = (path, locale)
	if cache_key not in cache:
		db = {}

		def parse(context: Iterator[Tuple[str, Any]]):
			nonlocal db
			root = None
			for action, elem in context:
				if action == "start" and elem.tag == "CardDefs":
					root = elem
					continue

				if action == "end" and elem.tag == "Entity":
					card = CardXML.from_xml(elem)
					card.locale = locale
					db[getattr(card, attr)] = card

					elem.clear()  # type: ignore
					root.clear()  # type: ignore

		if path is None:
			# Check if the hearthstone_data package exists locally
			has_lib = True
			try:
				import hearthstone_data  # noqa: F401
			except ImportError:
				has_lib = False

			if not has_lib:
				_bootstrap_from_web(parse, url=url)

		if not db:
			_bootstrap_from_library(parse, path=path)

		cache[cache_key] = (db, None)

	return cache[cache_key]


def load(path=None, locale="enUS", url=None):
	return _load(path, locale, cardid_cache, "id", url)


def load_dbf(path=None, locale="enUS", url=None):
	return _load(path, locale, dbf_cache, "dbf_id", url)
