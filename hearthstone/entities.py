from typing import Dict, Iterable, Iterator, List, Optional, Tuple, Union, cast

from hearthstone.utils import MAESTRA_DISGUISE_DBF_ID, get_original_card_id

from .enums import CardSet, CardType, GameTag, State, Step, Zone
from .types import GameTagsDict


STARTING_HERO_SETS = (CardSet.HERO_SKINS, )


class Entity:
	_args: Iterable[str] = ()

	def __init__(self, id):
		self.id = id
		self.game = None
		self.tags: GameTagsDict = {}
		self.initial_creator = 0
		self.initial_zone: Zone = Zone.INVALID
		self._initial_controller = 0

	def __repr__(self):
		return "%s(id=%r, %s)" % (
			self.__class__.__name__, self.id,
			", ".join("%s=%r" % (k, getattr(self, k)) for k in self._args)
		)

	@property
	def controller(self) -> Optional["Player"]:
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
		self.players: List[Player] = []
		self._entities: Dict[int, Entity] = {}
		self.initial_entities: List[Entity] = []
		self.initial_state: State = State.INVALID
		self.initial_step: Step = Step.INVALID

	@property
	def entities(self) -> Iterator[Entity]:
		yield from self._entities.values()

	@property
	def current_player(self) -> Optional["Player"]:
		for player in self.players:
			if player.tags.get(GameTag.CURRENT_PLAYER):
				return player
		return None

	@property
	def first_player(self) -> Optional["Player"]:
		for player in self.players:
			if player.tags.get(GameTag.FIRST_PLAYER):
				return player
		return None

	@property
	def setup_done(self) -> bool:
		return self.tags.get(GameTag.NEXT_STEP, 0) > Step.BEGIN_MULLIGAN

	def get_player(self, value: Union[int, str]) -> Optional["Player"]:
		for player in self.players:
			if value in (player.player_id, player.name):
				return player
		return None

	def in_zone(self, zone: Zone) -> Iterator[Entity]:
		for entity in self.entities:
			if entity.zone == zone:
				yield entity

	def create(self, tags: GameTagsDict) -> None:
		self.tags = dict(tags)
		self.initial_state = cast(State, self.tags.get(GameTag.STATE, State.INVALID))
		self.initial_step = cast(Step, self.tags.get(GameTag.STEP, Step.INVALID))
		self.register_entity(self)

	def register_entity(self, entity: Entity) -> None:
		entity.game = self
		self._entities[entity.id] = entity
		entity.initial_zone = entity.zone

		if isinstance(entity, Player):
			self.players.append(entity)
		elif not self.setup_done:
			self.initial_entities.append(entity)

		# Update player.starting_hero for Maestra of the Masquerade
		if (
			entity.type == CardType.HERO and
			entity.tags.get(GameTag.CREATOR_DBID) == MAESTRA_DISGUISE_DBF_ID
		):
			player = entity.controller
			if player is not None:
				# The player was playing Maestra, which created a fake hero at the start of
				# the game. After playing a Rogue card, the real hero is revealed, which
				# creates a new hero entity. To ensure that player.starting_hero returns the
				# "correct" Rogue hero, we overwrite the initial_hero_entity_id with the new
				# one.
				player.initial_hero_entity_id = entity.id

				# At this point we know that Maestra must be in the starting of the player,
				# because otherwise the reveal would not happen. Manually add it to the list
				# of starting cards
				player._known_starting_card_ids.add("SW_050")

	def reset(self) -> None:
		for entity in self.entities:
			if entity is self:
				continue
			entity.reset()

	def find_entity_by_id(self, id: int) -> Optional[Entity]:
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
		self._known_starting_card_ids = set()

	def __str__(self) -> str:
		return self.name or ""

	@property
	def names(self) -> Tuple[str, str]:
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
	def initial_deck(self) -> Iterator["Card"]:
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
	def known_starting_deck_list(self) -> List[str]:
		"""
		Returns a list of card ids that were present in the player's deck at the start of
		game (before Mulligan). May contain duplicates if same card is present multiple
		times in the deck. This attempts to reverse revealed transforms (e.g. Zerus, Molten
		Blade) and well-known transforms (e.g. Spellstones, Unidentified Objects, Worgens)
		so that the initial card id is included rather than the final card id.
		"""
		ret = list(self._known_starting_card_ids)

		original_card_ids = [
			get_original_card_id(entity.initial_card_id)
			for entity in self.initial_deck if entity.initial_card_id
		]
		ret = ret + [card_id for card_id in original_card_ids if card_id not in ret]

		return ret

	@property
	def entities(self) -> Iterator[Entity]:
		for entity in self.game.entities:
			if entity.controller == self:
				yield entity

	@property
	def hero(self) -> Optional["Card"]:
		entity_id = self.tags.get(GameTag.HERO_ENTITY, 0)
		if entity_id:
			return self.game.find_entity_by_id(entity_id)
		else:
			# Fallback that should never trigger
			for entity in self.in_zone(Zone.PLAY):
				if entity.type == CardType.HERO:
					return cast(Card, entity)
		return None

	@property
	def heroes(self) -> Iterator["Card"]:
		for entity in self.entities:
			if entity.type == CardType.HERO:
				yield cast(Card, entity)

	@property
	def starting_hero(self) -> Optional["Card"]:
		if self.initial_hero_entity_id:
			return cast(Card, self.game.find_entity_by_id(self.initial_hero_entity_id))

		# Fallback
		heroes = list(self.heroes)
		if not heroes:
			return None

		return heroes[0]

	@property
	def is_ai(self) -> bool:
		return self.account_lo == 0

	def in_zone(self, zone) -> Iterator["Entity"]:
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
	def base_tags(self) -> GameTagsDict:
		if not self.card_id:
			return {}

		from .cardxml import load
		db, _ = load()
		return db[self.card_id].tags

	def _get_initial_base_tags(self) -> GameTagsDict:
		if not self.initial_card_id:
			return {}

		from .cardxml import load
		db, _ = load()
		return db[self.initial_card_id].tags

	@property
	def can_be_in_deck(self) -> bool:
		card_type = self.type
		if not card_type:
			# If we don't know the card type, assume yes
			return True
		elif card_type == CardType.HERO:
			tags = self._get_initial_base_tags()
			return (
				tags.get(GameTag.CARD_SET, 0) not in STARTING_HERO_SETS and
				bool(tags.get(GameTag.COLLECTIBLE, 0))
			)

		return CardType(card_type).playable

	def _capture_initial_card_id(self, card_id: str, tags: GameTagsDict) -> None:
		if self.initial_card_id:
			# If we already know a previous card id, we do not want to change it.
			return

		transformed_from_card = tags.get(GameTag.TRANSFORMED_FROM_CARD, 0)
		if transformed_from_card:
			from .cardxml import load_dbf
			db, _ = load_dbf()
			card = db.get(transformed_from_card)
			if card:
				self.initial_card_id = card.card_id
				return

		if not self.is_original_entity:
			# If we know this card was transformed and we don't have an initial_card_id by
			# now, it is too late - any card_id we'd capture now would not reflect initial
			# one and be wrong.
			return

		self.initial_card_id = card_id

	def _update_tags(self, tags: GameTagsDict) -> None:
		super()._update_tags(tags)
		if self.is_original_entity and self.initial_creator is None:
			creator = tags.get(GameTag.CREATOR, 0)
			if creator:
				self.initial_creator = creator

	def reveal(self, card_id: str, tags: GameTagsDict) -> None:
		self.revealed = True
		self.card_id = card_id

		if (
			tags.get(GameTag.CREATOR_DBID, 0) or
			tags.get(GameTag.DISPLAYED_CREATOR, 0) or
			tags.get(GameTag.TRANSFORMED_FROM_CARD, 0)
		):
			# Cards that are revealed with a creator most likely have been transformed.
			self.is_original_entity = False

		self._capture_initial_card_id(card_id, tags)
		self._update_tags(tags)

	def hide(self) -> None:
		self.revealed = False

	def change(self, card_id: str, tags) -> None:
		self._capture_initial_card_id(card_id, tags)
		self.is_original_entity = False
		self.card_id = card_id
		self._update_tags(tags)

	def reset(self) -> None:
		self.card_id = None
		self.revealed = False
