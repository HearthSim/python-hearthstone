from datetime import datetime
from enum import IntEnum


class GameTag(IntEnum):
	"GAME_TAG"

	TAG_SCRIPT_DATA_NUM_1 = 2
	TAG_SCRIPT_DATA_NUM_2 = 3
	TAG_SCRIPT_DATA_ENT_1 = 4
	TAG_SCRIPT_DATA_ENT_2 = 5
	MISSION_EVENT = 6
	TIMEOUT = 7
	TURN_START = 8
	TURN_TIMER_SLUSH = 9
	PREMIUM = 12
	GOLD_REWARD_STATE = 13
	PLAYSTATE = 17
	LAST_AFFECTED_BY = 18
	STEP = 19
	TURN = 20
	FATIGUE = 22
	CURRENT_PLAYER = 23
	FIRST_PLAYER = 24
	RESOURCES_USED = 25
	RESOURCES = 26
	HERO_ENTITY = 27
	MAXHANDSIZE = 28
	STARTHANDSIZE = 29
	PLAYER_ID = 30
	TEAM_ID = 31
	TRIGGER_VISUAL = 32
	RECENTLY_ARRIVED = 33
	PROTECTED = 34
	PROTECTING = 35
	DEFENDING = 36
	PROPOSED_DEFENDER = 37
	ATTACKING = 38
	PROPOSED_ATTACKER = 39
	ATTACHED = 40
	EXHAUSTED = 43
	DAMAGE = 44
	HEALTH = 45
	ATK = 47
	COST = 48
	ZONE = 49
	CONTROLLER = 50
	OWNER = 51
	DEFINITION = 52
	ENTITY_ID = 53
	HISTORY_PROXY = 54
	COPY_DEATHRATTLE = 55
	ELITE = 114
	MAXRESOURCES = 176
	CARD_SET = 183
	DURABILITY = 187
	SILENCED = 188
	WINDFURY = 189
	TAUNT = 190
	STEALTH = 191
	SPELLPOWER = 192
	DIVINE_SHIELD = 194
	CHARGE = 197
	NEXT_STEP = 198
	CLASS = 199
	CARDRACE = 200
	FACTION = 201
	CARDTYPE = 202
	RARITY = 203
	STATE = 204
	SUMMONED = 205
	FREEZE = 208
	ENRAGED = 212
	OVERLOAD = 215
	LOYALTY = 216
	DEATHRATTLE = 217
	BATTLECRY = 218
	SECRET = 219
	COMBO = 220
	CANT_HEAL = 221
	CANT_DAMAGE = 222
	CANT_SET_ASIDE = 223
	CANT_REMOVE_FROM_GAME = 224
	CANT_READY = 225
	CANT_ATTACK = 227
	CANT_DISCARD = 230
	CANT_PLAY = 231
	CANT_DRAW = 232
	CANT_BE_HEALED = 239
	IMMUNE = 240
	CANT_BE_SET_ASIDE = 241
	CANT_BE_REMOVED_FROM_GAME = 242
	CANT_BE_READIED = 243
	CANT_BE_ATTACKED = 245
	CANT_BE_TARGETED = 246
	CANT_BE_DESTROYED = 247
	CANT_BE_SUMMONING_SICK = 253
	FROZEN = 260
	JUST_PLAYED = 261
	LINKED_ENTITY = 262
	ZONE_POSITION = 263
	CANT_BE_FROZEN = 264
	COMBO_ACTIVE = 266
	CARD_TARGET = 267
	NUM_CARDS_PLAYED_THIS_TURN = 269
	CANT_BE_TARGETED_BY_OPPONENTS = 270
	NUM_TURNS_IN_PLAY = 271
	NUM_TURNS_LEFT = 272
	CURRENT_SPELLPOWER = 291
	ARMOR = 292
	MORPH = 293
	IS_MORPHED = 294
	TEMP_RESOURCES = 295
	OVERLOAD_OWED = 296
	NUM_ATTACKS_THIS_TURN = 297
	NEXT_ALLY_BUFF = 302
	MAGNET = 303
	FIRST_CARD_PLAYED_THIS_TURN = 304
	MULLIGAN_STATE = 305
	TAUNT_READY = 306
	STEALTH_READY = 307
	CHARGE_READY = 308
	CANT_BE_TARGETED_BY_SPELLS = 311
	SHOULDEXITCOMBAT = 312
	CREATOR = 313
	CANT_BE_SILENCED = 314
	PARENT_CARD = 316
	NUM_MINIONS_PLAYED_THIS_TURN = 317
	PREDAMAGE = 318
	COLLECTIBLE = 321
	ENCHANTMENT_BIRTH_VISUAL = 330
	ENCHANTMENT_IDLE_VISUAL = 331
	CANT_BE_TARGETED_BY_HERO_POWERS = 332
	HEALTH_MINIMUM = 337
	TAG_ONE_TURN_EFFECT = 338
	SILENCE = 339
	COUNTER = 340
	ZONES_REVEALED = 348
	ADJACENT_BUFF = 350
	FORCED_PLAY = 352
	LOW_HEALTH_THRESHOLD = 353
	SPELLPOWER_DOUBLE = 356
	HEALING_DOUBLE = 357
	NUM_OPTIONS_PLAYED_THIS_TURN = 358
	TO_BE_DESTROYED = 360
	AURA = 362
	POISONOUS = 363
	HERO_POWER_DOUBLE = 366
	AI_MUST_PLAY = 367
	NUM_MINIONS_PLAYER_KILLED_THIS_TURN = 368
	NUM_MINIONS_KILLED_THIS_TURN = 369
	AFFECTED_BY_SPELL_POWER = 370
	EXTRA_DEATHRATTLES = 371
	START_WITH_1_HEALTH = 372
	IMMUNE_WHILE_ATTACKING = 373
	MULTIPLY_HERO_DAMAGE = 374
	MULTIPLY_BUFF_VALUE = 375
	CUSTOM_KEYWORD_EFFECT = 376
	TOPDECK = 377
	CANT_BE_TARGETED_BY_BATTLECRIES = 379
	HERO_POWER = 380
	DEATHRATTLE_RETURN_ZONE = 382
	STEADY_SHOT_CAN_TARGET = 383
	DISPLAYED_CREATOR = 385
	POWERED_UP = 386
	SPARE_PART = 388
	FORGETFUL = 389
	CAN_SUMMON_MAXPLUSONE_MINION = 390
	OBFUSCATED = 391
	BURNING = 392
	OVERLOAD_LOCKED = 393
	NUM_TIMES_HERO_POWER_USED_THIS_GAME = 394
	CURRENT_HEROPOWER_DAMAGE_BONUS = 395
	HEROPOWER_DAMAGE = 396
	LAST_CARD_PLAYED = 397
	NUM_FRIENDLY_MINIONS_THAT_DIED_THIS_TURN = 398
	NUM_CARDS_DRAWN_THIS_TURN = 399
	AI_ONE_SHOT_KILL = 400
	EVIL_GLOW = 401
	HIDE_STATS = 402
	INSPIRE = 403
	RECEIVES_DOUBLE_SPELLDAMAGE_BONUS = 404
	HEROPOWER_ADDITIONAL_ACTIVATIONS = 405
	HEROPOWER_ACTIVATIONS_THIS_TURN = 406
	REVEALED = 410
	NUM_FRIENDLY_MINIONS_THAT_DIED_THIS_GAME = 412
	CANNOT_ATTACK_HEROES = 413
	LOCK_AND_LOAD = 414
	DISCOVER = 415
	SHADOWFORM = 416
	NUM_FRIENDLY_MINIONS_THAT_ATTACKED_THIS_TURN = 417
	NUM_RESOURCES_SPENT_THIS_GAME = 418
	CHOOSE_BOTH = 419
	ELECTRIC_CHARGE_LEVEL = 420
	HEAVILY_ARMORED = 421
	DONT_SHOW_IMMUNE = 422
	RITUAL = 424
	PREHEALING = 425
	APPEAR_FUNCTIONALLY_DEAD = 426
	OVERLOAD_THIS_GAME = 427
	SPELLS_COST_HEALTH = 431
	HISTORY_PROXY_NO_BIG_CARD = 432
	PROXY_CTHUN = 434
	TRANSFORMED_FROM_CARD = 435
	CTHUN = 436
	CAST_RANDOM_SPELLS = 437
	SHIFTING = 438
	JADE_GOLEM = 441
	EMBRACE_THE_SHADOW = 442
	CHOOSE_ONE = 443
	EXTRA_ATTACKS_THIS_TURN = 444
	SEEN_CTHUN = 445
	MINION_TYPE_REFERENCE = 447
	UNTOUCHABLE = 448
	RED_MANA_CRYSTALS = 449
	SCORE_LABELID_1 = 450
	SCORE_VALUE_1 = 451
	SCORE_LABELID_2 = 452
	SCORE_LABELID_3 = 454
	SCORE_VALUE_2 = 453
	SCORE_VALUE_3 = 455
	CANT_BE_FATIGUED = 456
	AUTOATTACK = 457
	ARMS_DEALING = 458
	PENDING_EVOLUTIONS = 461
	QUEST = 462
	TAG_LAST_KNOWN_COST_IN_HAND = 466
	DEFINING_ENCHANTMENT = 469
	FINISH_ATTACK_SPELL_ON_DAMAGE = 470
	MODULAR_ENTITY_PART_1 = 471
	MODULAR_ENTITY_PART_2 = 472
	MODIFY_DEFINITION_ATTACK = 473
	MODIFY_DEFINITION_HEALTH = 474
	MODIFY_DEFINITION_COST = 475
	MULTIPLE_CLASSES = 476
	ALL_TARGETS_RANDOM = 477
	MULTI_CLASS_GROUP = 480
	CARD_COSTS_HEALTH = 481
	GRIMY_GOONS = 482
	JADE_LOTUS = 483
	KABAL = 484
	ADDITIONAL_PLAY_REQS_1 = 515
	ADDITIONAL_PLAY_REQS_2 = 516
	ELEMENTAL_POWERED_UP = 532
	QUEST_PROGRESS = 534
	QUEST_PROGRESS_TOTAL = 535
	QUEST_CONTRIBUTOR = 541
	ADAPT = 546
	IS_CURRENT_TURN_AN_EXTRA_TURN = 547
	EXTRA_TURNS_TAKEN_THIS_GAME = 548
	SHIFTING_MINION = 549
	SHIFTING_WEAPON = 550
	DEATH_KNIGHT = 554
	BOSS = 556
	STAMPEDE = 564
	IS_VAMPIRE = 680
	CORRUPTED = 681
	LIFESTEAL = 685
	OVERRIDE_EMOTE_0 = 740
	OVERRIDE_EMOTE_1 = 741
	OVERRIDE_EMOTE_2 = 742
	OVERRIDE_EMOTE_3 = 743
	OVERRIDE_EMOTE_4 = 744
	OVERRIDE_EMOTE_5 = 745
	SCORE_FOOTERID = 751
	HERO_POWER_DISABLED = 777
	VALEERASHADOW = 779
	OVERRIDECARDNAME = 781
	OVERRIDECARDTEXTBUILDER = 782
	HIDDEN_CHOICE = 813
	ZOMBEAST = 823
	HERO_EMOTE_SILENCED = 832

	InvisibleDeathrattle = 335
	ImmuneToSpellpower = 349
	AttackVisualType = 251
	DevState = 268
	GrantCharge = 355
	HealTarget = 361

	# strings (all deleted?)
	CARDTEXT_INHAND = 184
	CARDNAME = 185
	ARTISTNAME = 342
	FLAVORTEXT = 351
	HOW_TO_EARN = 364
	HOW_TO_EARN_GOLDEN = 365
	CardTextInPlay = 252
	TARGETING_ARROW_TEXT = 325
	LocalizationNotes = 344

	# Renamed
	CANT_BE_DAMAGED = IMMUNE
	CANT_BE_DISPELLED = CANT_BE_SILENCED
	CANT_BE_TARGETED_BY_ABILITIES = CANT_BE_TARGETED_BY_SPELLS
	DEATH_RATTLE = DEATHRATTLE
	DEATHRATTLE_SENDS_BACK_TO_DECK = DEATHRATTLE_RETURN_ZONE
	HAND_REVEALED = ZONES_REVEALED
	HIDE_COST = HIDE_STATS
	KAZAKUS_POTION_POWER_1 = MODULAR_ENTITY_PART_1
	KAZAKUS_POTION_POWER_2 = MODULAR_ENTITY_PART_2
	LINKEDCARD = LINKED_ENTITY
	RECALL = OVERLOAD
	RECALL_OWED = OVERLOAD_OWED
	TAG_HERO_POWER_DOUBLE = HERO_POWER_DOUBLE
	TAG_AI_MUST_PLAY = AI_MUST_PLAY
	TREASURE = DISCOVER
	SHOWN_HERO_POWER = HERO_POWER
	OVERKILL = 380

	# Deleted
	IGNORE_DAMAGE = 1
	COPY_DEATHRATTLE_INDEX = 56
	CARD_ID = 186
	INCOMING_HEALING_MULTIPLIER = 233
	INCOMING_HEALING_ADJUSTMENT = 234
	INCOMING_HEALING_CAP = 235
	INCOMING_DAMAGE_MULTIPLIER = 236
	INCOMING_DAMAGE_ADJUSTMENT = 237
	INCOMING_DAMAGE_CAP = 238
	OUTGOING_DAMAGE_CAP = 273
	OUTGOING_DAMAGE_ADJUSTMENT = 274
	OUTGOING_DAMAGE_MULTIPLIER = 275
	OUTGOING_HEALING_CAP = 276
	OUTGOING_HEALING_ADJUSTMENT = 277
	OUTGOING_HEALING_MULTIPLIER = 278
	INCOMING_ABILITY_DAMAGE_ADJUSTMENT = 279
	INCOMING_COMBAT_DAMAGE_ADJUSTMENT = 280
	OUTGOING_ABILITY_DAMAGE_ADJUSTMENT = 281
	OUTGOING_COMBAT_DAMAGE_ADJUSTMENT = 282
	OUTGOING_ABILITY_DAMAGE_MULTIPLIER = 283
	OUTGOING_ABILITY_DAMAGE_CAP = 284
	INCOMING_ABILITY_DAMAGE_MULTIPLIER = 285
	INCOMING_ABILITY_DAMAGE_CAP = 286
	OUTGOING_COMBAT_DAMAGE_MULTIPLIER = 287
	OUTGOING_COMBAT_DAMAGE_CAP = 288
	INCOMING_COMBAT_DAMAGE_MULTIPLIER = 289
	INCOMING_COMBAT_DAMAGE_CAP = 290
	DIVINE_SHIELD_READY = 314
	IGNORE_DAMAGE_OFF = 354
	NUM_OPTIONS = 359

	# Missing, only present in logs
	WEAPON = 334

	CANT_BE_EXHAUSTED = 244
	CANT_EXHAUST = 226
	CANT_TARGET = 228
	CANT_DESTROY = 229
	# Enum number changed
	# HISTORY_PROXY_NO_BIG_CARD = 427

	@property
	def type(self):
		return TAG_TYPES.get(self, Type.NUMBER)

	@property
	def string_type(self):
		return self.type in (Type.LOCSTRING, Type.STRING)


TAG_NAMES = {
	GameTag.TRIGGER_VISUAL: "TriggerVisual",
	GameTag.HEALTH: "Health",
	GameTag.ATK: "Atk",
	GameTag.COST: "Cost",
	GameTag.ELITE: "Elite",
	GameTag.CARD_SET: "CardSet",
	GameTag.CARDTEXT_INHAND: "CardTextInHand",
	GameTag.CARDNAME: "CardName",
	GameTag.DURABILITY: "Durability",
	GameTag.WINDFURY: "Windfury",
	GameTag.TAUNT: "Taunt",
	GameTag.STEALTH: "Stealth",
	GameTag.SPELLPOWER: "Spellpower",
	GameTag.DIVINE_SHIELD: "Divine Shield",
	GameTag.CHARGE: "Charge",
	GameTag.CLASS: "Class",
	GameTag.CARDRACE: "Race",
	GameTag.FACTION: "Faction",
	GameTag.RARITY: "Rarity",
	GameTag.CARDTYPE: "CardType",
	GameTag.FREEZE: "Freeze",
	GameTag.ENRAGED: "Enrage",
	GameTag.RECALL: "Recall",
	GameTag.DEATHRATTLE: "Deathrattle",
	GameTag.BATTLECRY: "Battlecry",
	GameTag.SECRET: "Secret",
	GameTag.COMBO: "Combo",
	GameTag.IMMUNE: "Cant Be Damaged",
	GameTag.AttackVisualType: "AttackVisualType",
	GameTag.CardTextInPlay: "CardTextInPlay",
	GameTag.DevState: "DevState",
	GameTag.MORPH: "Morph",
	GameTag.COLLECTIBLE: "Collectible",
	GameTag.TARGETING_ARROW_TEXT: "TargetingArrowText",
	GameTag.ENCHANTMENT_BIRTH_VISUAL: "EnchantmentBirthVisual",
	GameTag.ENCHANTMENT_IDLE_VISUAL: "EnchantmentIdleVisual",
	GameTag.InvisibleDeathrattle: "InvisibleDeathrattle",
	GameTag.TAG_ONE_TURN_EFFECT: "OneTurnEffect",
	GameTag.SILENCE: "Silence",
	GameTag.COUNTER: "Counter",
	GameTag.ARTISTNAME: "ArtistName",
	GameTag.ImmuneToSpellpower: "ImmuneToSpellpower",
	GameTag.ADJACENT_BUFF: "AdjacentBuff",
	GameTag.FLAVORTEXT: "FlavorText",
	GameTag.HealTarget: "HealTarget",
	GameTag.AURA: "Aura",
	GameTag.POISONOUS: "Poisonous",
	GameTag.HOW_TO_EARN: "HowToGetThisCard",
	GameTag.HOW_TO_EARN_GOLDEN: "HowToGetThisGoldCard",
	GameTag.AI_MUST_PLAY: "AIMustPlay",
	GameTag.AFFECTED_BY_SPELL_POWER: "AffectedBySpellPower",
	GameTag.SPARE_PART: "SparePart",
	GameTag.HIDE_STATS: "HideStats",
	GameTag.DISCOVER: "Treasure",
	GameTag.AUTOATTACK: "AutoAttack",
}


##
# Card enums

class CardClass(IntEnum):
	"TAG_CLASS"

	INVALID = 0
	DEATHKNIGHT = 1
	DRUID = 2
	HUNTER = 3
	MAGE = 4
	PALADIN = 5
	PRIEST = 6
	ROGUE = 7
	SHAMAN = 8
	WARLOCK = 9
	WARRIOR = 10
	DREAM = 11
	NEUTRAL = 12

	@property
	def default_hero(self):
		from .utils import CARDCLASS_HERO_MAP
		return CARDCLASS_HERO_MAP.get(self, "")

	@property
	def is_playable(self):
		return bool(self.default_hero)

	@property
	def name_global(self):
		return "GLOBAL_CLASS_%s" % (self.name)


class CardSet(IntEnum):
	"TAG_CARD_SET"

	INVALID = 0
	TEST_TEMPORARY = 1
	CORE = 2
	EXPERT1 = 3
	HOF = 4
	MISSIONS = 5
	DEMO = 6
	NONE = 7
	CHEAT = 8
	BLANK = 9
	DEBUG_SP = 10
	PROMO = 11
	NAXX = 12
	GVG = 13
	BRM = 14
	TGT = 15
	CREDITS = 16
	HERO_SKINS = 17
	TB = 18
	SLUSH = 19
	LOE = 20
	OG = 21
	OG_RESERVE = 22
	KARA = 23
	KARA_RESERVE = 24
	GANGS = 25
	GANGS_RESERVE = 26
	UNGORO = 27
	ICECROWN = 1001
	LOOTAPALOOZA = 1004

	# Aliased from the original enums
	FP1 = 12
	PE1 = 13

	# Renamed
	FP2 = BRM
	PE2 = TEMP1 = TGT
	REWARD = HOF

	@property
	def craftable(self):
		return self in (
			CardSet.EXPERT1,
			CardSet.NAXX,
			CardSet.GVG,
			CardSet.BRM,
			CardSet.TGT,
			CardSet.LOE,
			CardSet.OG,
			CardSet.KARA,
			CardSet.GANGS,
			CardSet.UNGORO,
			CardSet.ICECROWN,
		)

	@property
	def name_global(self):
		return "GLOBAL_CARD_SET_%s" % (self.name)

	@property
	def short_name_global(self):
		return self.name_global + "_SHORT"

	@property
	def is_standard(self):
		return self in (
			CardSet.CORE,
			CardSet.EXPERT1,
			CardSet.OG,
			CardSet.KARA,
			CardSet.GANGS,
			CardSet.UNGORO,
			CardSet.ICECROWN,
		)


class CardType(IntEnum):
	"TAG_CARDTYPE"

	INVALID = 0
	GAME = 1
	PLAYER = 2
	HERO = 3
	MINION = 4
	SPELL = 5
	ENCHANTMENT = 6
	WEAPON = 7
	ITEM = 8
	TOKEN = 9
	HERO_POWER = 10

	# Renamed
	ABILITY = SPELL

	@property
	def craftable(self):
		return self in (
			CardType.MINION,
			CardType.SPELL,
			CardType.WEAPON,
		)

	@property
	def name_global(self):
		if self.name == "HERO_POWER":
			return "GLOBAL_CARDTYPE_HEROPOWER"
		return "GLOBAL_CARDTYPE_%s" % (self.name)


class EnchantmentVisual(IntEnum):
	"TAG_ENCHANTMENT_VISUAL"

	INVALID = 0
	POSITIVE = 1
	NEGATIVE = 2
	NEUTRAL = 3


class Faction(IntEnum):
	"TAG_FACTION"

	INVALID = 0
	HORDE = 1
	ALLIANCE = 2
	NEUTRAL = 3


class PlayReq(IntEnum):
	"PlayErrors.ErrorType"

	INVALID = -1
	REQ_MINION_TARGET = 1
	REQ_FRIENDLY_TARGET = 2
	REQ_ENEMY_TARGET = 3
	REQ_DAMAGED_TARGET = 4
	REQ_MAX_SECRETS = 5
	REQ_FROZEN_TARGET = 6
	REQ_CHARGE_TARGET = 7
	REQ_TARGET_MAX_ATTACK = 8
	REQ_NONSELF_TARGET = 9
	REQ_TARGET_WITH_RACE = 10
	REQ_TARGET_TO_PLAY = 11
	REQ_NUM_MINION_SLOTS = 12
	REQ_WEAPON_EQUIPPED = 13
	REQ_ENOUGH_MANA = 14
	REQ_YOUR_TURN = 15
	REQ_NONSTEALTH_ENEMY_TARGET = 16
	REQ_HERO_TARGET = 17
	REQ_SECRET_ZONE_CAP = 18
	REQ_MINION_CAP_IF_TARGET_AVAILABLE = 19
	REQ_MINION_CAP = 20
	REQ_TARGET_ATTACKED_THIS_TURN = 21
	REQ_TARGET_IF_AVAILABLE = 22
	REQ_MINIMUM_ENEMY_MINIONS = 23
	REQ_TARGET_FOR_COMBO = 24
	REQ_NOT_EXHAUSTED_ACTIVATE = 25
	REQ_UNIQUE_SECRET_OR_QUEST = 26
	REQ_TARGET_TAUNTER = 27
	REQ_CAN_BE_ATTACKED = 28
	REQ_ACTION_PWR_IS_MASTER_PWR = 29
	REQ_TARGET_MAGNET = 30
	REQ_ATTACK_GREATER_THAN_0 = 31
	REQ_ATTACKER_NOT_FROZEN = 32
	REQ_HERO_OR_MINION_TARGET = 33
	REQ_CAN_BE_TARGETED_BY_SPELLS = 34
	REQ_SUBCARD_IS_PLAYABLE = 35
	REQ_TARGET_FOR_NO_COMBO = 36
	REQ_NOT_MINION_JUST_PLAYED = 37
	REQ_NOT_EXHAUSTED_HERO_POWER = 38
	REQ_CAN_BE_TARGETED_BY_OPPONENTS = 39
	REQ_ATTACKER_CAN_ATTACK = 40
	REQ_TARGET_MIN_ATTACK = 41
	REQ_CAN_BE_TARGETED_BY_HERO_POWERS = 42
	REQ_ENEMY_TARGET_NOT_IMMUNE = 43
	REQ_ENTIRE_ENTOURAGE_NOT_IN_PLAY = 44
	REQ_MINIMUM_TOTAL_MINIONS = 45
	REQ_MUST_TARGET_TAUNTER = 46
	REQ_UNDAMAGED_TARGET = 47
	REQ_CAN_BE_TARGETED_BY_BATTLECRIES = 48
	REQ_STEADY_SHOT = 49
	REQ_MINION_OR_ENEMY_HERO = 50
	REQ_TARGET_IF_AVAILABLE_AND_DRAGON_IN_HAND = 51
	REQ_LEGENDARY_TARGET = 52
	REQ_FRIENDLY_MINION_DIED_THIS_TURN = 53
	REQ_FRIENDLY_MINION_DIED_THIS_GAME = 54
	REQ_ENEMY_WEAPON_EQUIPPED = 55
	REQ_TARGET_IF_AVAILABLE_AND_MINIMUM_FRIENDLY_MINIONS = 56
	REQ_TARGET_WITH_BATTLECRY = 57
	REQ_TARGET_WITH_DEATHRATTLE = 58
	REQ_TARGET_IF_AVAILABLE_AND_MINIMUM_FRIENDLY_SECRETS = 59
	REQ_SECRET_ZONE_CAP_FOR_NON_SECRET = 60
	REQ_TARGET_EXACT_COST = 61
	REQ_STEALTHED_TARGET = 62
	REQ_MINION_SLOT_OR_MANA_CRYSTAL_SLOT = 63
	REQ_MAX_QUESTS = 64
	REQ_TARGET_IF_AVAILABE_AND_ELEMENTAL_PLAYED_LAST_TURN = 65
	REQ_TARGET_NOT_VAMPIRE = 66
	REQ_TARGET_NOT_DAMAGEABLE_ONLY_BY_WEAPONS = 67
	REQ_NOT_DISABLED_HERO_POWER = 68
	REQ_MUST_PLAY_OTHER_CARD_FIRST = 69
	REQ_HAND_NOT_FULL = 70
	REQ_DRAG_TO_PLAY = 71

	# Renamed
	REQ_ENCHANTED_TARGET = REQ_MAX_SECRETS
	REQ_UNIQUE_SECRET = REQ_UNIQUE_SECRET_OR_QUEST
	REQ_SECRET_CAP = REQ_SECRET_ZONE_CAP
	REQ_SECRET_CAP_FOR_NON_SECRET = REQ_SECRET_ZONE_CAP_FOR_NON_SECRET


class Race(IntEnum):
	"TAG_RACE"

	INVALID = 0
	BLOODELF = 1
	DRAENEI = 2
	DWARF = 3
	GNOME = 4
	GOBLIN = 5
	HUMAN = 6
	NIGHTELF = 7
	ORC = 8
	TAUREN = 9
	TROLL = 10
	UNDEAD = 11
	WORGEN = 12
	GOBLIN2 = 13
	MURLOC = 14
	DEMON = 15
	SCOURGE = 16
	MECHANICAL = 17
	ELEMENTAL = 18
	OGRE = 19
	BEAST = 20
	TOTEM = 21
	NERUBIAN = 22
	PIRATE = 23
	DRAGON = 24

	# Aliased
	PET = 20

	@property
	def name_global(self):
		if self.name == "BEAST":
			return "GLOBAL_RACE_PET"
		return "GLOBAL_RACE_%s" % (self.name)

	@property
	def visible(self):
		# XXX: Mech is only a visible tribe since GVG
		return self in VISIBLE_RACES


VISIBLE_RACES = [
	Race.MURLOC, Race.DEMON, Race.MECHANICAL, Race.BEAST,
	Race.TOTEM, Race.PIRATE, Race.DRAGON
]


class Rarity(IntEnum):
	"TAG_RARITY"

	INVALID = 0
	COMMON = 1
	FREE = 2
	RARE = 3
	EPIC = 4
	LEGENDARY = 5

	# TB_BlingBrawl_Blade1e (10956)
	UNKNOWN_6 = 6

	@property
	def craftable(self):
		return self in (
			Rarity.COMMON,
			Rarity.RARE,
			Rarity.EPIC,
			Rarity.LEGENDARY,
		)

	@property
	def crafting_costs(self):
		from .utils import CRAFTING_COSTS
		return CRAFTING_COSTS.get(self, (0, 0))

	@property
	def disenchant_costs(self):
		from .utils import DISENCHANT_COSTS
		return DISENCHANT_COSTS.get(self, (0, 0))

	@property
	def name_global(self):
		return "GLOBAL_RARITY_%s" % (self.name)


class Zone(IntEnum):
	"TAG_ZONE"

	INVALID = 0
	PLAY = 1
	DECK = 2
	HAND = 3
	GRAVEYARD = 4
	REMOVEDFROMGAME = 5
	SETASIDE = 6
	SECRET = 7


##
# Game enums

class ChoiceType(IntEnum):
	"CHOICE_TYPE"

	INVALID = 0
	MULLIGAN = 1
	GENERAL = 2


class BnetGameType(IntEnum):
	"PegasusShared.BnetGameType"
	BGT_UNKNOWN = 0
	BGT_FRIENDS = 1
	BGT_RANKED_STANDARD = 2
	BGT_ARENA = 3
	BGT_VS_AI = 4
	BGT_TUTORIAL = 5
	BGT_ASYNC = 6
	BGT_CASUAL_STANDARD_NEWBIE = 9
	BGT_CASUAL_STANDARD_NORMAL = 10
	BGT_TEST1 = 11
	BGT_TEST2 = 12
	BGT_TEST3 = 13
	BGT_TAVERNBRAWL_PVP = 16
	BGT_TAVERNBRAWL_1P_VERSUS_AI = 17
	BGT_TAVERNBRAWL_2P_COOP = 18
	BGT_RANKED_WILD = 30
	BGT_CASUAL_WILD = 31
	BGT_FSG_BRAWL_VS_FRIEND = 40
	BGT_FSG_BRAWL_PVP = 41
	BGT_FSG_BRAWL_1P_VERSUS_AI = 42
	BGT_FSG_BRAWL_2P_COOP = 43
	# BGT_LAST = 43

	BGT_NEWBIE = BGT_CASUAL_STANDARD_NEWBIE
	BGT_CASUAL_STANDARD = BGT_CASUAL_STANDARD_NORMAL


STANDARD_GAME_TYPES = [
	BnetGameType.BGT_CASUAL_STANDARD,
	BnetGameType.BGT_RANKED_STANDARD,
]

WILD_GAME_TYPES = [
	BnetGameType.BGT_CASUAL_WILD,
	BnetGameType.BGT_RANKED_WILD,
]


class GameType(IntEnum):
	"PegasusShared.GameType"
	GT_UNKNOWN = 0
	GT_VS_AI = 1
	GT_VS_FRIEND = 2
	GT_TUTORIAL = 4
	GT_ARENA = 5
	GT_TEST = 6
	GT_RANKED = 7
	GT_CASUAL = 8
	GT_TAVERNBRAWL = 16
	GT_TB_1P_VS_AI = 17
	GT_TB_2P_COOP = 18
	GT_FSG_BRAWL_VS_FRIEND = 19
	GT_FSG_BRAWL = 20
	GT_FSG_BRAWL_1P_VS_AI = 21
	GT_FSG_BRAWL_2P_COOP = 22
	# GT_LAST = 22

	def as_bnet(self, wild=False):
		if self == GameType.GT_RANKED:
			return BnetGameType.BGT_RANKED_WILD if wild else BnetGameType.BGT_RANKED_STANDARD
		if self == GameType.GT_CASUAL:
			return BnetGameType.BGT_CASUAL_WILD if wild else BnetGameType.BGT_CASUAL_STANDARD

		return {
			GameType.GT_UNKNOWN: BnetGameType.BGT_UNKNOWN,
			GameType.GT_VS_AI: BnetGameType.BGT_VS_AI,
			GameType.GT_VS_FRIEND: BnetGameType.BGT_FRIENDS,
			GameType.GT_TUTORIAL: BnetGameType.BGT_TUTORIAL,
			GameType.GT_ARENA: BnetGameType.BGT_ARENA,
			GameType.GT_TEST: BnetGameType.BGT_TEST1,
			GameType.GT_TAVERNBRAWL: BnetGameType.BGT_TAVERNBRAWL_PVP,
			GameType.GT_TB_1P_VS_AI: BnetGameType.BGT_TAVERNBRAWL_1P_VERSUS_AI,
			GameType.GT_TB_2P_COOP: BnetGameType.BGT_TAVERNBRAWL_2P_COOP,
			# GameType.GT_LAST: BnetGameType.BGT_LAST,
		}[self]


class BnetRegion(IntEnum):
	"bgs.constants.BnetRegion"

	REGION_UNINITIALIZED = -1,
	REGION_UNKNOWN = 0
	REGION_US = 1
	REGION_EU = 2
	REGION_KR = 3
	REGION_TW = 4
	REGION_CN = 5
	REGION_LIVE_VERIFICATION = 40
	REGION_PTR_LOC = 41

	# Deleted
	REGION_MSCHWEITZER_BN11 = 52
	REGION_MSCHWEITZER_BN12 = 53
	REGION_DEV = 60
	REGION_PTR = 98

	@classmethod
	def from_account_hi(cls, hi):
		# AI: 0x200000000000000 (144115188075855872)
		# US: 0x200000157544347 (144115193835963207)
		# EU: 0x200000257544347 (144115198130930503)
		# KR: 0x200000357544347 (144115202425897799) (TW on same region)
		# CN: 0x200000557544347 (144115211015832391)
		return cls((hi >> 32) & 0xFF)


class GoldRewardState(IntEnum):
	"TAG_GOLD_REWARD_STATE"

	INVALID = 0
	ELIGIBLE = 1
	WRONG_GAME_TYPE = 2
	ALREADY_CAPPED = 3
	BAD_RATING = 4
	SHORT_GAME_BY_TIME = 5
	OVER_CAIS = 6

	# Renamed
	SHORT_GAME = SHORT_GAME_BY_TIME


class MetaDataType(IntEnum):
	"PegasusGame.HistoryMeta.Type"

	TARGET = 0
	DAMAGE = 1
	HEALING = 2
	JOUST = 3
	SHOW_BIG_CARD = 5
	EFFECT_TIMING = 6
	HISTORY_TARGET = 7
	OVERRIDE_HISTORY = 8
	HISTORY_TARGET_DONT_DUPLICATE_UNTIL_END = 9
	BEGIN_ARTIFICIAL_HISTORY_TILE = 10
	BEGIN_ARTIFICIAL_HISTORY_TRIGGER_TILE = 11
	END_ARTIFICIAL_HISTORY_TILE = 12

	# Renamed in 9786 from PowerHistoryMetaData.Type
	META_TARGET = TARGET
	META_DAMAGE = DAMAGE
	META_HEALING = HEALING

	# Deleted
	CLIENT_HISTORY = 4


class Mulligan(IntEnum):
	"TAG_MULLIGAN"

	INVALID = 0
	INPUT = 1
	DEALING = 2
	WAITING = 3
	DONE = 4


class MultiClassGroup(IntEnum):
	"TAG_MULTI_CLASS_GROUP"

	INVALID = 0
	GRIMY_GOONS = 1
	JADE_LOTUS = 2
	KABAL = 3


class OptionType(IntEnum):
	"PegasusGame.Option.Type"

	PASS = 1
	END_TURN = 2
	POWER = 3


class PlayState(IntEnum):
	"TAG_PLAYSTATE"

	INVALID = 0
	PLAYING = 1
	WINNING = 2
	LOSING = 3
	WON = 4
	LOST = 5
	TIED = 6
	DISCONNECTED = 7
	CONCEDED = 8

	# Renamed in 10833
	QUIT = CONCEDED


class PowerType(IntEnum):
	"Network.PowerType"

	FULL_ENTITY = 1
	SHOW_ENTITY = 2
	HIDE_ENTITY = 3
	TAG_CHANGE = 4
	BLOCK_START = 5
	BLOCK_END = 6
	CREATE_GAME = 7
	META_DATA = 8
	CHANGE_ENTITY = 9

	# Renamed in 12574
	ACTION_START = BLOCK_START
	ACTION_END = BLOCK_END


class BlockType(IntEnum):
	"PegasusGame.HistoryBlock.Type"

	ATTACK = 1
	JOUST = 2
	POWER = 3
	TRIGGER = 5
	DEATHS = 6
	PLAY = 7
	FATIGUE = 8
	RITUAL = 9

	# Removed
	SCRIPT = 4
	ACTION = 99

	# Renamed
	CONTINUOUS = 2


class State(IntEnum):
	"TAG_STATE"

	INVALID = 0
	LOADING = 1
	RUNNING = 2
	COMPLETE = 3


class Step(IntEnum):
	"TAG_STEP"

	INVALID = 0
	BEGIN_FIRST = 1
	BEGIN_SHUFFLE = 2
	BEGIN_DRAW = 3
	BEGIN_MULLIGAN = 4
	MAIN_BEGIN = 5
	MAIN_READY = 6
	MAIN_RESOURCE = 7
	MAIN_DRAW = 8
	MAIN_START = 9
	MAIN_ACTION = 10
	MAIN_COMBAT = 11
	MAIN_END = 12
	MAIN_NEXT = 13
	FINAL_WRAPUP = 14
	FINAL_GAMEOVER = 15
	MAIN_CLEANUP = 16
	MAIN_START_TRIGGERS = 17


##
# Misc

class Booster(IntEnum):
	"BoosterDbId"

	INVALID = 0
	CLASSIC = 1
	GOBLINS_VS_GNOMES = 9
	THE_GRAND_TOURNAMENT = 10
	OLD_GODS = 11
	FIRST_PURCHASE = 17
	SIGNUP_INCENTIVE = 18
	MEAN_STREETS = 19
	UNGORO = 20
	FROZEN_THRONE = 21
	GOLDEN_CLASSIC_PACK = 23
	KOBOLDS_CATACOMBS = 30


class BrawlType(IntEnum):
	"PegasusShared.BrawlType"

	BRAWL_TYPE_UNKNOWN = 0
	BRAWL_TYPE_TAVERN_BRAWL = 1
	BRAWL_TYPE_FIRESIDE_GATHERING = 2
	BRAWL_TYPE_COUNT = 3
	# BRAWL_TYPE_FIRST = 1


class CardTextBuilderType(IntEnum):
	"CardTextBuilderType"

	DEFAULT = 0
	JADE_GOLEM = 1
	JADE_GOLEM_TRIGGER = 2
	MODULAR_ENTITY = 3
	KAZAKUS_POTION_EFFECT = 4
	DEPRECATED_5 = 5
	DEPRECATED_6 = 6
	SCRIPT_DATA_NUM_1 = 7
	PLACE_HOLDER_8 = 8
	DECORATE = 9
	PLACE_HOLDER_10 = 10
	PLACE_HOLDER_11 = 11
	PLACE_HOLDER_12 = 12
	PLACE_HOLDER_13 = 13
	ZOMBEAST = 14
	ZOMBEAST_ENCHANTMENT = 15
	HIDDEN_CHOICE = 16
	PLACE_HOLDER_17 = 17
	REFERENCE_CREATOR_ENTITY = 18
	REFERENCE_SCRIPT_DATA_NUM_1_ENTITY = 19

	# Renamed
	KAZAKUS_POTION = MODULAR_ENTITY
	PLACE_HOLDER_7 = SCRIPT_DATA_NUM_1


class DeckType(IntEnum):
	"PegasusShared.DeckType"

	UNKNOWN_DECK_TYPE = 0
	NORMAL_DECK = 1
	AI_DECK = 2
	DRAFT_DECK = 4
	PRECON_DECK = 5
	TAVERN_BRAWL_DECK = 6
	FSG_BRAWL_DECK = 7
	HIDDEN_DECK = 1000


class FormatType(IntEnum):
	"PegasusShared.FormatType"

	FT_UNKNOWN = 0
	FT_WILD = 1
	FT_STANDARD = 2

	@property
	def name_global(self):
		if self.name == "FT_WILD":
			return "GLOBAL_WILD"
		elif self.name == "FT_STANDARD":
			return "GLOBAL_STANDARD"


class Type(IntEnum):
	"TAG_TYPE"

	UNKNOWN = 0
	BOOL = 1
	NUMBER = 2
	COUNTER = 3
	ENTITY = 4
	PLAYER = 5
	TEAM = 6
	ENTITY_DEFINITION = 7
	STRING = 8

	# Not present at the time
	LOCSTRING = -2


TAG_TYPES = {
	GameTag.TRIGGER_VISUAL: Type.BOOL,
	GameTag.ELITE: Type.BOOL,
	GameTag.CARD_SET: CardSet,
	GameTag.CARDTEXT_INHAND: Type.LOCSTRING,
	GameTag.CARDNAME: Type.LOCSTRING,
	GameTag.WINDFURY: Type.BOOL,
	GameTag.TAUNT: Type.BOOL,
	GameTag.STEALTH: Type.BOOL,
	GameTag.SPELLPOWER: Type.BOOL,
	GameTag.DIVINE_SHIELD: Type.BOOL,
	GameTag.CHARGE: Type.BOOL,
	GameTag.CLASS: CardClass,
	GameTag.CARDRACE: Race,
	GameTag.FACTION: Faction,
	GameTag.RARITY: Rarity,
	GameTag.CARDTYPE: CardType,
	GameTag.FREEZE: Type.BOOL,
	GameTag.ENRAGED: Type.BOOL,
	GameTag.DEATHRATTLE: Type.BOOL,
	GameTag.BATTLECRY: Type.BOOL,
	GameTag.SECRET: Type.BOOL,
	GameTag.COMBO: Type.BOOL,
	GameTag.IMMUNE: Type.BOOL,
	# GameTag.AttackVisualType: AttackVisualType,
	GameTag.CardTextInPlay: Type.LOCSTRING,
	# GameTag.DevState: DevState,
	GameTag.MORPH: Type.BOOL,
	GameTag.COLLECTIBLE: Type.BOOL,
	GameTag.TARGETING_ARROW_TEXT: Type.LOCSTRING,
	GameTag.ENCHANTMENT_BIRTH_VISUAL: EnchantmentVisual,
	GameTag.ENCHANTMENT_IDLE_VISUAL: EnchantmentVisual,
	GameTag.InvisibleDeathrattle: Type.BOOL,
	GameTag.TAG_ONE_TURN_EFFECT: Type.BOOL,
	GameTag.SILENCE: Type.BOOL,
	GameTag.COUNTER: Type.BOOL,
	GameTag.ARTISTNAME: Type.STRING,
	GameTag.LocalizationNotes: Type.STRING,
	GameTag.ImmuneToSpellpower: Type.BOOL,
	GameTag.ADJACENT_BUFF: Type.BOOL,
	GameTag.FLAVORTEXT: Type.LOCSTRING,
	GameTag.HealTarget: Type.BOOL,
	GameTag.AURA: Type.BOOL,
	GameTag.POISONOUS: Type.BOOL,
	GameTag.HOW_TO_EARN: Type.LOCSTRING,
	GameTag.HOW_TO_EARN_GOLDEN: Type.LOCSTRING,
	GameTag.AI_MUST_PLAY: Type.BOOL,
	GameTag.AFFECTED_BY_SPELL_POWER: Type.BOOL,
	GameTag.SPARE_PART: Type.BOOL,
	GameTag.PLAYSTATE: PlayState,
	GameTag.ZONE: Zone,
	GameTag.STEP: Step,
	GameTag.NEXT_STEP: Step,
	GameTag.STATE: State,
	GameTag.MULLIGAN_STATE: Mulligan,
	GameTag.AUTOATTACK: Type.BOOL,
}


LOCALIZED_TAGS = [k for k, v in TAG_TYPES.items() if v == Type.LOCSTRING]


class Locale(IntEnum):
	"Locale"

	UNKNOWN = -1
	enUS = 0
	enGB = 1
	frFR = 2
	deDE = 3
	koKR = 4
	esES = 5
	esMX = 6
	ruRU = 7
	zhTW = 8
	zhCN = 9
	itIT = 10
	ptBR = 11
	plPL = 12
	ptPT = 13
	jaJP = 14
	thTH = 15

	@property
	def unused(self):
		return self.name in ("UNKNOWN", "enGB", "ptPT")

	@property
	def name_global(self):
		if self.name == "enGB":
			return "GLOBAL_LANGUAGE_NATIVE_ENUS"
		return "GLOBAL_LANGUAGE_NATIVE_%s" % (self.name.upper())


def get_localized_name(v, locale="enUS"):
	name_global = getattr(v, "name_global", "")
	if not name_global:
		return ""

	from .stringsfile import load_globalstrings

	globalstrings = load_globalstrings(locale)
	return globalstrings.get(name_global, {}).get("TEXT", "")


class ZodiacYear(IntEnum):
	INVALID = -1
	PRE_STANDARD = 0
	KRAKEN = 1
	MAMMOTH = 2

	@property
	def standard_card_sets(self):
		from .utils import STANDARD_SETS
		return STANDARD_SETS.get(self, [])

	@classmethod
	def as_of_date(self, date=None):
		from .utils import ZODIAC_ROTATION_DATES

		if date is None:
			date = datetime.now()

		ret = ZodiacYear.INVALID
		rotation_dates = sorted(ZODIAC_ROTATION_DATES.items(), key=lambda x: x[1])
		for enum_value, rotation_date in rotation_dates:
			if rotation_date > date:
				break
			ret = enum_value

		return ret


if __name__ == "__main__":
	import sys
	import json

	enums = {
		k: dict(v.__members__) for k, v in globals().items() if (
			isinstance(v, type) and issubclass(v, IntEnum) and k != "IntEnum"
		)
	}

	def _print_enums(enums, format):
		ret = []
		linefmt = "\t%s = %i,"
		for enum in sorted(enums):
			sorted_pairs = sorted(enums[enum].items(), key=lambda k: k[1])
			lines = "\n".join(linefmt % (name, value) for name, value in sorted_pairs)
			ret.append(format % (enum, lines))
		print("\n\n".join(ret))

	if len(sys.argv) >= 2:
		format = sys.argv[1]
	else:
		format = "--json"

	if format == "--ts":
		_print_enums(enums, "export const enum %s {\n%s\n}")
	elif format == "--cs":
		_print_enums(enums, "public enum %s {\n%s\n}")
	else:
		print(json.dumps(enums, sort_keys=True))
