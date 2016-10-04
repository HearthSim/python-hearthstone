"""
Classes to provide lazy players that are treatable as an entity ID but
do not have to receive one immediately.
"""
from ..enums import GameTag


class LazyPlayer:
	def __init__(self, *args, **kwargs):
		self.id = None
		self.name = None

	def __repr__(self):
		return "%s(id=%r, name=%r)" % (self.__class__.__name__, self.id, self.name)

	def __int__(self):
		if not self.id:
			raise RuntimeError("Entity ID not available for player %r" % (self.name))
		return self.id


class PlayerManager:
	def __init__(self):
		self._players_by_id = {}
		self._players_by_name = {}
		self._players_by_player_id = {}
		self.registered_players = 0

	def get_player_by_id(self, id):
		assert id, "Expected an id for get_player_by_id (got %r)" % (id)
		if id not in self._players_by_id:
			lazy_player = LazyPlayer()
			lazy_player.id = id
			self._players_by_id[id] = lazy_player
		return self._players_by_id[id]

	def get_player_by_name(self, name):
		assert name, "Expected a name for get_player_by_name (got %r)" % (name)
		if name not in self._players_by_name:
			lazy_player = LazyPlayer()
			lazy_player.name = name
			self._players_by_name[name] = lazy_player
		return self._players_by_name[name]

	def new_player(self, id, player_id):
		lazy_player = self.get_player_by_id(id)
		self._players_by_player_id[player_id] = lazy_player
		return lazy_player

	def check_player_registration(self, tag, value, name):
		"""
		Trigger on a tag change if we did not find a corresponding entity.
		"""
		if tag == GameTag.ENTITY_ID:
			# This is the simplest check. When a player entity is declared,
			# its ENTITY_ID is not available immediately (in pre-6.0).
			# If we get a matching ENTITY_ID, then we can use that to match it.
			self.register_player_name(name, value)
			return value

		# If we still have nothing, return a LazyPlayer.
		return self.get_player_by_name(name)

	def register_player_name(self, name, id):
		"""
		Registers a link between \a name and \a id.
		Note that this does not support two different players with the same name.
		"""
		lazy_player_by_name = self.get_player_by_name(name)
		lazy_player_by_name.id = id
		lazy_player_by_id = self._players_by_id[id]
		lazy_player_by_id.name = name
		self.registered_players += 1
		# TODO: name alias re-registration (is_ai / UNKNOWN HUMAN PLAYER)
		return lazy_player_by_name

	def register_player_name_mulligan(self, packet):
		"""
		Attempt to register player names by looking at Mulligan choice packets.
		In Hearthstone 6.0+, registering a player name using tag changes is not
		available as early as before. That means games conceded at Mulligan no
		longer have player names.
		This technique uses the cards offered in Mulligan instead, registering
		the name of the packet's entity with the card's controller as PlayerID.
		"""
		lazy_player = packet.entity
		if isinstance(lazy_player, int) or lazy_player.id:
			# The player is already registered, ignore.
			return
		if not lazy_player.name:
			# If we don't have the player name, we can't use this at all
			return

		for choice in packet.choices:
			controller = choice.tags.get(GameTag.CONTROLLER, 0)
			if controller:
				# We need ENTITY_ID for register_player_name()
				# That's always PlayerID + 1
				entity_id = controller + 1
				packet.entity = entity_id
				return self.register_player_name(lazy_player.name, entity_id)
