from .enums import (
	CardClass, CardSet, CardType, Faction, GameTag, MultiClassGroup, PlayReq, Race, Rarity
)
from .utils import ElementTree


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
			elif tag == GameTag.HERO_POWER:
				self.hero_power = e.attrib.get("cardID")
			else:
				self.tags[tag] = value

		for e in xml.findall("./ReferencedTag"):
			tag, type, value = _unpack_tag_xml(e)
			self.referenced_tags[tag] = value

		if self.tags.get(GameTag.HERO_POWER):
			i = int(GameTag.HERO_POWER)
			t = xml.findall('./Tag[@enumID="%i"]' % (i))
			if t is not None:
				self.hero_power = t[0].attrib.get("cardID")

		e = xml.findall("MasterPower")
		self.master_power = e[0] if e else None

		e = xml.findall("Power")
		for power in e:
			self.powers.append(_read_power_tag(power))

		self.entourage = [t.attrib["cardID"] for t in xml.findall("EntourageCard")]
		return self

	def __init__(self, id, locale="enUS"):
		self.card_id = self.id = id
		self.dbf_id = 0
		self.version = 2
		self.tags = {}
		self.hero_power = None
		self.referenced_tags = {}
		self.master_power = None
		self.entourage = []
		self.powers = []
		self.triggered_power_history_info = []

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

	def to_xml(self):
		ret = ElementTree.Element("Entity", CardID=self.id, ID=str(self.dbf_id))
		if self.version:
			ret.attrib["version"] = str(self.version)

		if self.master_power:
			master_power = ElementTree.SubElement(ret, "MasterPower")
			master_power.text = self.master_power

		for tag in LOCALIZED_TAGS:
			value = self.strings[tag]
			if value:
				e = ElementTree.SubElement(ret, "Tag", enumID=str(int(tag)), name=tag.name)
				e.attrib["type"] = "LocString"
				for locale, localized_value in sorted(value.items()):
					if localized_value:
						loc_element = ElementTree.SubElement(e, locale)
						loc_element.text = str(localized_value)

		for tag in STRING_TAGS:
			value = self.strings[tag]
			if value:
				e = ElementTree.SubElement(ret, "Tag", enumID=str(int(tag)), name=tag.name)
				e.attrib["type"] = "String"
				e.text = value

		for tag, value in sorted(self.tags.items()):
			if value:
				e = _make_tag_element(ret, "Tag", tag, value)

				if tag == GameTag.HERO_POWER and self.hero_power:
					e.attrib["type"] = "Card"
					e.attrib["cardID"] = self.hero_power

		for tag, value in sorted(self.referenced_tags.items()):
			e = _make_tag_element(ret, "ReferencedTag", tag, value)

		for entourage in self.entourage:
			ElementTree.SubElement(ret, "EntourageCard", cardID=entourage)

		for power in self.powers:
			ep = ElementTree.SubElement(ret, "Power", definition=power["definition"])
			reqs = power.get("requirements", {})
			for reqid, param in reqs.items():
				er = ElementTree.SubElement(ep, "PlayRequirement", reqID=str(int(reqid)))
				er.attrib["param"] = str(param or "")

		for tphi in self.triggered_power_history_info:
			e = ElementTree.SubElement(ret, "TriggeredPowerHistoryInfo")
			e.attrib["effectIndex"] = str(tphi["effectIndex"])
			e.attrib["showInHistory"] = str(tphi["showInHistory"])

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
	can_summon_maxplusone_minion = prop(GameTag.CAN_SUMMON_MAXPLUSONE_MINION, bool)
	cant_be_attacked = prop(GameTag.CANT_BE_ATTACKED, bool)
	cant_be_fatigued = prop(GameTag.CANT_BE_FATIGUED, bool)
	collectible = prop(GameTag.COLLECTIBLE, bool)
	battlecry = prop(GameTag.BATTLECRY, bool)
	deathrattle = prop(GameTag.DEATHRATTLE, bool)
	discover = prop(GameTag.DISCOVER, bool)
	divine_shield = prop(GameTag.DIVINE_SHIELD, bool)
	double_spelldamage_bonus = prop(GameTag.RECEIVES_DOUBLE_SPELLDAMAGE_BONUS, bool)
	echo = prop(GameTag.ECHO, bool)
	elite = prop(GameTag.ELITE, bool)
	evil_glow = prop(GameTag.EVIL_GLOW, bool)
	forgetful = prop(GameTag.FORGETFUL, bool)
	ghostly = prop(GameTag.GHOSTLY, bool)
	hide_health = prop(GameTag.HIDE_HEALTH, bool)
	hide_stats = prop(GameTag.HIDE_STATS, bool)
	immune = prop(GameTag.IMMUNE, bool)
	inspire = prop(GameTag.INSPIRE, bool)
	jade_golem = prop(GameTag.JADE_GOLEM, bool)
	one_turn_effect = prop(GameTag.TAG_ONE_TURN_EFFECT, bool)
	poisonous = prop(GameTag.POISONOUS, bool)
	quest = prop(GameTag.QUEST, bool)
	ritual = prop(GameTag.RITUAL, bool)
	rush = prop(GameTag.RUSH, bool)
	secret = prop(GameTag.SECRET, bool)
	spare_part = prop(GameTag.SPARE_PART, bool)
	taunt = prop(GameTag.TAUNT, bool)
	topdeck = prop(GameTag.TOPDECK, bool)
	twinspell = prop(GameTag.TWINSPELL, bool)
	untouchable = prop(GameTag.UNTOUCHABLE, bool)

	##
	# Tags

	armor = prop(GameTag.ARMOR)
	atk = prop(GameTag.ATK)
	durability = prop(GameTag.DURABILITY)
	cost = prop(GameTag.COST)
	health = prop(GameTag.HEALTH)
	windfury = prop(GameTag.WINDFURY)
	quest_progress_total = prop(GameTag.QUEST_PROGRESS_TOTAL)

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


cardid_cache: dict = {}
dbf_cache: dict = {}


def _load(path, locale, cache, attr):
	cache_key = (path, locale)
	if cache_key not in cache:
		from hearthstone_data import get_carddefs_path

		if path is None:
			path = get_carddefs_path()

		db = {}

		with open(path, "rb") as f:
			xml = ElementTree.parse(f)
			for carddata in xml.findall("Entity"):
				card = CardXML.from_xml(carddata)
				card.locale = locale
				db[getattr(card, attr)] = card

		cache[cache_key] = (db, xml)

	return cache[cache_key]


def load(path=None, locale="enUS"):
	return _load(path, locale, cardid_cache, "id")


def load_dbf(path=None, locale="enUS"):
	return _load(path, locale, dbf_cache, "dbf_id")
