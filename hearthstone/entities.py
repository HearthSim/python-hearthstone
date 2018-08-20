from typing import Iterable

from .enums import CardSet, CardType, GameTag, State, Step, Zone


PLAYABLE_CARD_TYPES = (
	CardType.HERO, CardType.MINION, CardType.SPELL, CardType.WEAPON
)
INITIAL_HERO_SETS = (CardSet.CORE, CardSet.HERO_SKINS)


class Entity:
	_args: Iterable[str] = ()

	def __init__(self, id):
		self.id = id
		self.game = None
		self.tags = {}
		self.initial_creator = 0
		self.initial_zone = Zone.INVALID
		self._initial_controller = 0

	def __repr__(self):
		return "%s(id=%r, %s)" % (
			self.__class__.__name__, self.id,
			", ".join("%s=%r" % (k, getattr(self, k)) for k in self._args)
		)

	@property
	def controller(self):
		return self.game.get_player(self.tags.get(GameTag.CONTROLLER, 0))

	@property
	def initial_controller(self):
		return self.game.get_player(
			self._initial_controller or self.tags.get(GameTag.CONTROLLER, 0)
		)

	@property
	def type(self):
		return self.tags.get(GameTag.CARDTYPE, CardType.INVALID)

	@property
	def zone(self):
		return self.tags.get(GameTag.ZONE, Zone.INVALID)

	def _update_tags(self, tags):
		for tag, value in tags.items():
			if tag == GameTag.CONTROLLER and not self._initial_controller:
				self._initial_controller = self.tags.get(GameTag.CONTROLLER, value)
		self.tags.update(tags)

	def reset(self):
		pass

	def tag_change(self, tag, value):
		self._update_tags({tag: value})


class Game(Entity):
	_args = ("players", )
	can_be_in_deck = False

	def __init__(self, id):
		super(Game, self).__init__(id)
		self.players = []
		self._entities = {}
		self.initial_entities = []
		self.initial_state = State.INVALID
		self.initial_step = Step.INVALID

	@property
	def entities(self):
		yield from self._entities.values()

	@property
	def current_player(self):
		for player in self.players:
			if player.tags.get(GameTag.CURRENT_PLAYER):
				return player

	@property
	def first_player(self):
		for player in self.players:
			if player.tags.get(GameTag.FIRST_PLAYER):
				return player

	@property
	def setup_done(self):
		return self.tags.get(GameTag.NEXT_STEP, 0) > Step.BEGIN_MULLIGAN

	def get_player(self, value):
		for player in self.players:
			if value in (player.player_id, player.name):
				return player

	def in_zone(self, zone):
		for entity in self.entities:
			if entity.zone == zone:
				yield entity

	def create(self, tags):
		self.tags = dict(tags)
		self.initial_state = self.tags.get(GameTag.STATE, State.INVALID)
		self.initial_step = self.tags.get(GameTag.STEP, Step.INVALID)
		self.register_entity(self)

	def register_entity(self, entity):
		entity.game = self
		self._entities[entity.id] = entity
		entity.initial_zone = entity.zone

		if isinstance(entity, Player):
			self.players.append(entity)
		elif not self.setup_done:
			self.initial_entities.append(entity)

	def reset(self):
		for entity in self.entities:
			if entity is self:
				continue
			entity.reset()

	def find_entity_by_id(self, id: int):
		# int() for LazyPlayer mainly...
		id = int(id)
		return self._entities.get(id)


class Player(Entity):
	_args = ("name", )
	UNKNOWN_HUMAN_PLAYER = "UNKNOWN HUMAN PLAYER"
	can_be_in_deck = False

	def __init__(self, id, player_id, hi, lo, name=None):
		super(Player, self).__init__(id)
		self.player_id = player_id
		self.account_hi = hi
		self.account_lo = lo
		self.name = name
		self.initial_hero_entity_id = 0

	def __str__(self):
		return self.name or ""

	@property
	def names(self):
		"""
		Returns the player's name and real name.
		Returns two empty strings if the player is unknown.
		AI real name is always an empty string.
		"""
		if self.name == self.UNKNOWN_HUMAN_PLAYER:
			return "", ""

		if not self.is_ai and " " in self.name:
			return "", self.name

		return self.name, ""

	@property
	def initial_deck(self):
		for entity in self.game.initial_entities:
			# Exclude entities that aren't initially owned by the player
			if entity.initial_controller != self:
				continue

			# Exclude entities that aren't initially in the deck
			if entity.initial_zone != Zone.DECK:
				continue

			# Exclude entity types that cannot be in the deck
			if not entity.can_be_in_deck:
				continue

			# Allow CREATOR=1 because of monster hunt decks.
			# Everything else is likely a false positive.
			if entity.initial_creator > 1:
				continue

			yield entity

	@property
	def entities(self):
		for entity in self.game.entities:
			if entity.controller == self:
				yield entity

	@property
	def hero(self):
		entity_id = self.tags.get(GameTag.HERO_ENTITY, 0)
		if entity_id:
			return self.game.find_entity_by_id(entity_id)
		else:
			# Fallback that should never trigger
			for entity in self.in_zone(Zone.PLAY):
				if entity.type == CardType.HERO:
					return entity

	@property
	def heroes(self):
		for entity in self.entities:
			if entity.type == CardType.HERO:
				yield entity

	@property
	def starting_hero(self):
		if self.initial_hero_entity_id:
			return self.game.find_entity_by_id(self.initial_hero_entity_id)

		# Fallback
		heroes = list(self.heroes)
		if not heroes:
			return

		return heroes[0]

	@property
	def is_ai(self):
		return self.account_lo == 0

	def in_zone(self, zone):
		for entity in self.entities:
			if entity.zone == zone:
				yield entity


class Card(Entity):
	_args = ("card_id", )

	def __init__(self, id, card_id):
		super(Card, self).__init__(id)
		self.is_original_entity = True
		self.initial_card_id = card_id
		self.card_id = card_id
		self.revealed = False

	@property
	def base_tags(self) -> dict:
		if not self.card_id:
			return {}

		from .cardxml import load
		db, _ = load()
		return db[self.card_id].tags

	@property
	def can_be_in_deck(self) -> bool:
		card_type = self.type
		if not card_type:
			# If we don't know the card type, assume yes
			return True
		elif card_type == CardType.HERO:
			tags = self.base_tags
			return (
				tags.get(GameTag.CARD_SET, 0) not in INITIAL_HERO_SETS and
				tags.get(GameTag.COLLECTIBLE, 0)
			)

		return card_type in PLAYABLE_CARD_TYPES

	def _capture_card_id(self, card_id, tags):
		if self.initial_card_id:
			return

		transformed_from_card = tags.get(GameTag.TRANSFORMED_FROM_CARD, 0)
		if transformed_from_card:
			from .cardxml import load_dbf
			db, _ = load_dbf()
			card = db.get(transformed_from_card)
			if card:
				self.initial_card_id = card.card_id
				return

		self.initial_card_id = card_id

	def _update_tags(self, tags):
		super()._update_tags(tags)
		if self.is_original_entity and self.initial_creator is None:
			creator = tags.get(GameTag.CREATOR, 0)
			if creator:
				self.initial_creator = creator

	def reveal(self, card_id, tags):
		self.revealed = True
		self.card_id = card_id
		self._capture_card_id(card_id, tags)
		if tags.get(GameTag.TRANSFORMED_FROM_CARD, 0):
			self.is_original_entity = False
		self._update_tags(tags)

	def hide(self):
		self.revealed = False

	def change(self, card_id, tags):
		self.is_original_entity = False
		self._capture_card_id(card_id, tags)
		self.card_id = card_id
		self._update_tags(tags)

	def reset(self):
		self.card_id = None
		self.revealed = False
