class Entity:
	_args = ()

	def __init__(self, id):
		self.id = id
		self.tags = {}

	def __repr__(self):
		return "%s(id=%r, %s)" % (
			self.__class__.__name__, self.id,
			", ".join("%s=%r" % (k, getattr(self, k)) for k in self._args)
		)

	def tag_change(self, tag, value):
		self.tags[tag] = value


class Game(Entity):
	_args = ("players", )

	def __init__(self, id):
		super().__init__(id)
		self.players = []
		self.entities = {}
		self.actions = []

	def register_entity(self, entity):
		self.entities[entity.id] = entity
		if isinstance(entity, Player):
			self.players.append(entity)

	def register_player_name(self, name, id):
		self.entities[id].name = name

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
