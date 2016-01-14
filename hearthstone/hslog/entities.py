class Entity:
	def __init__(self, id):
		self.id = id
		self.tags = {}

	def tag_change(self, tag, value):
		self.tags[tag] = value


class Game(Entity):
	def __init__(self, id):
		super().__init__(id)
		self.players = []
		self.entities = {}
		self.actions = []

	def __repr__(self):
		return "%s(players=%r)" % (self.__class__.__name__, self.players)

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
	def __init__(self, id, player_id, hi, lo):
		super().__init__(id)
		self.player_id = player_id
		self.account_hi = hi
		self.account_lo = lo
		self.name = None

	def __repr__(self):
		return "%s(id=%r, name=%r)" % (self.__class__.__name__, self.id, self.name)


class Card(Entity):
	def __init__(self, id, card_id):
		super().__init__(id)
		self.card_id = card_id
		self.revealed = False

	def __repr__(self):
		return "%s(card_id=%r)" % (self.__class__.__name__, self.card_id)

	def reveal(self, id):
		self.revealed = True
		self.card_id = id

	def hide(self):
		self.revealed = False
