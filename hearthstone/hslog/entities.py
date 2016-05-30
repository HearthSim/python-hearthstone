from hearthstone.enums import CardType, GameTag, Step, Zone


class Entity(object):
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
		super(Game, self).__init__(id)
		self.players = []
		self.entities = []
		self.packets = []
		self.ts = ts
		self.mulligan = {}

	def __iter__(self):
		for packet in self.packets:
			yield packet

	@property
	def start_time(self):
		for packet in self.packets:
			if packet.ts:
				return packet.ts

	@property
	def end_time(self):
		for packet in self.packets[::-1]:
			if packet.ts:
				return packet.ts

	@property
	def current_player(self):
		for player in self.players:
			if player.tags.get(GameTag.CURRENT_PLAYER):
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

	def register_entity(self, entity):
		entity.game = self
		self.entities.append(entity)
		if isinstance(entity, Player):
			self.players.append(entity)

	def find_entity_by_id(self, id):
		for entity in self.entities:
			if entity.id == id:
				return entity
			elif entity.id > id:
				# It's just not there...
				return


class Player(Entity):
	_args = ("name", )

	def __init__(self, id, player_id, hi, lo):
		super(Player, self).__init__(id)
		self.player_id = player_id
		self.account_hi = hi
		self.account_lo = lo
		self.name = None

	@property
	def initial_deck(self):
		for entity in self.entities:
			if 3 < entity.id < 68:
				if entity.tags.get(GameTag.CARDTYPE) not in (
					CardType.HERO, CardType.HERO_POWER
				):
					yield entity

	@property
	def entities(self):
		for entity in self.game.entities:
			if entity.controller == self:
				yield entity

	@property
	def heroes(self):
		for entity in self.entities:
			if entity.type == CardType.HERO:
				yield entity

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
		self.card_id = card_id
		self.revealed = False

	def reveal(self, id):
		self.revealed = True
		self.card_id = id

	def hide(self):
		self.revealed = False

	def change(self, id):
		self.card_id = id
		self.tags = {}
