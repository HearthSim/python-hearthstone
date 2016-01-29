from hearthstone.enums import CardType, GameTag, Zone


class Entity:
	_args = ()

	def __init__(self, id):
		self.id = id
		self.game = None
		self.tags = {}

	def __repr__(self):
		return "%s(id=%r, %s)" % (
			self.__class__.__name__, self.id,
			", ".join("%s=%r" % (k, getattr(self, k)) for k in self._args)
		)

	@property
	def controller(self):
		return self.game.get_player(self.tags.get(GameTag.CONTROLLER, 0))

	@property
	def type(self):
		return self.tags.get(GameTag.CARDTYPE, CardType.INVALID)

	@property
	def zone(self):
		return self.tags.get(GameTag.ZONE, Zone.INVALID)

	def tag_change(self, tag, value):
		self.tags[tag] = value


class Game(Entity):
	_args = ("players", )

	def __init__(self, id, ts):
		super().__init__(id)
		self.players = []
		self.entities = {}
		self.packets = []
		self.ts = ts

	def __iter__(self):
		for packet in self.packets:
			yield packet

	def get_player(self, id):
		for player in self.players:
			if player.player_id == id:
				return player

	def in_zone(self, zone):
		for entity in self.entities:
			if entity.zone == zone:
				yield entity

	def register_entity(self, entity):
		entity.game = self
		self.entities[entity.id] = entity
		if isinstance(entity, Player):
			self.players.append(entity)

	def find_player(self, name):
		for player in self.players:
			if name == player.name:
				return player


class Player(Entity):
	_args = ("name", )

	def __init__(self, id, player_id, hi, lo):
		super().__init__(id)
		self.player_id = player_id
		self.account_hi = hi
		self.account_lo = lo
		self.name = None

	def in_zone(self, zone):
		for entity in self.game.entities:
			if entity.zone == zone and entity.controller == self:
				yield entity


class Card(Entity):
	_args = ("card_id", )

	def __init__(self, id, card_id):
		super().__init__(id)
		self.card_id = card_id
		self.revealed = False

	def reveal(self, id):
		self.revealed = True
		self.card_id = id

	def hide(self):
		self.revealed = False
