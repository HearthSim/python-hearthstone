from .. import entities
from ..enums import GameTag, Zone
from . import packets


class BaseExporter(object):
	def __init__(self, packet_tree):
		self.packet_tree = packet_tree
		self.dispatch = self.get_dispatch_dict()

	def get_dispatch_dict(self):
		return {
			packets.CreateGame: self.handle_create_game,
			packets.CreateGame.Player: self.handle_player,
			packets.Block: self.handle_block,
			packets.FullEntity: self.handle_full_entity,
			packets.HideEntity: self.handle_hide_entity,
			packets.ShowEntity: self.handle_show_entity,
			packets.ChangeEntity: self.handle_change_entity,
			packets.TagChange: self.handle_tag_change,
			packets.MetaData: self.handle_metadata,
			packets.Choices: self.handle_choices,
			packets.SendChoices: self.handle_send_choices,
			packets.ChosenEntities: self.handle_chosen_entities,
			packets.Options: self.handle_options,
			packets.Option: self.handle_option,
			packets.SendOption: self.handle_send_option,
		}

	def export(self):
		for packet in self.packet_tree:
			self.export_packet(packet)
		return self

	def export_packet(self, packet):
		packet_type = packet.__class__
		handler = self.dispatch.get(packet_type, None)
		if not handler:
			raise NotImplementedError("Don't know how to export %r" % (packet_type))
		handler(packet)

	def handle_create_game(self, packet):
		pass

	def handle_player(self, packet):
		pass

	def handle_block(self, packet):
		for p in packet.packets:
			self.export_packet(p)

	def handle_full_entity(self, packet):
		pass

	def handle_hide_entity(self, packet):
		pass

	def handle_show_entity(self, packet):
		pass

	def handle_change_entity(self, packet):
		pass

	def handle_tag_change(self, packet):
		pass

	def handle_metadata(self, packet):
		pass

	def handle_choices(self, packet):
		pass

	def handle_send_choices(self, packet):
		pass

	def handle_chosen_entities(self, packet):
		pass

	def handle_options(self, packet):
		pass

	def handle_option(self, packet):
		pass

	def handle_send_option(self, packet):
		pass


class EntityTreeExporter(BaseExporter):
	game_class = entities.Game
	player_class = entities.Player
	card_class = entities.Card

	class EntityNotFound(Exception):
		pass

	def find_entity(self, id, opcode):
		try:
			entity = self.game.find_entity_by_id(id)
		except RuntimeError as e:
			raise self.EntityNotFound("Error getting entity %r for %s" % (id, opcode))
		if not entity:
			raise self.EntityNotFound("Attempting %s on entity %r (not found)" % (opcode, id))
		return entity

	def handle_create_game(self, packet):
		self.game = self.game_class(packet.entity)
		self.game.create(packet.tags)
		for player in packet.players:
			self.export_packet(player)
		return self.game

	def handle_player(self, packet):
		id = int(packet.entity)
		if hasattr(self.packet_tree, "manager"):
			# If we have a PlayerManager, first we mutate the CreateGame.Player packet.
			# This will have to change if we're ever able to immediately get the names.
			player = self.packet_tree.manager.get_player_by_id(id)
			packet.name = player.name
		entity = self.player_class(id, packet.player_id, packet.hi, packet.lo, packet.name)
		entity.tags = dict(packet.tags)
		self.game.register_entity(entity)
		return entity

	def handle_full_entity(self, packet):
		entity = self.card_class(packet.entity, packet.card_id)
		entity.tags = dict(packet.tags)
		self.game.register_entity(entity)
		return entity

	def handle_hide_entity(self, packet):
		entity = self.find_entity(packet.entity, "HIDE_ENTITY")
		entity.hide()
		return entity

	def handle_show_entity(self, packet):
		entity = self.find_entity(packet.entity, "SHOW_ENTITY")
		entity.reveal(packet.card_id, dict(packet.tags))
		return entity

	def handle_change_entity(self, packet):
		entity = self.find_entity(packet.entity, "CHANGE_ENTITY")
		entity.change(packet.card_id, dict(packet.tags))
		return entity

	def handle_tag_change(self, packet):
		entity = self.find_entity(packet.entity, "TAG_CHANGE")
		entity.tag_change(packet.tag, packet.value)
		return entity


class FriendlyPlayerExporter(BaseExporter):
	"""
	An exporter that will attempt to guess the friendly player in the game by
	looking for initial unrevealed cards.
	May produce incorrect results in spectator mode if both hands are revealed.
	"""
	def __init__(self, packet_tree):
		super(FriendlyPlayerExporter, self).__init__(packet_tree)
		self._controller_map = {}
		self.friendly_player = None

	def export(self):
		for packet in self.packet_tree:
			self.export_packet(packet)
			if self.friendly_player:
				# Stop export once we have it
				break
		return self.friendly_player

	def handle_tag_change(self, packet):
		if packet.tag == GameTag.CONTROLLER:
			self._controller_map[packet.entity] = packet.value

	def handle_full_entity(self, packet):
		tags = dict(packet.tags)
		if GameTag.CONTROLLER in tags:
			self._controller_map[packet.entity] = tags[GameTag.CONTROLLER]

		# The following logic only works for pre-13619 logs
		# The first FULL_ENTITY packet which is in Zone.HAND and does *not*
		# have an ID is owned by the friendly player's *opponent*.
		if tags[GameTag.ZONE] == Zone.HAND and not packet.card_id:
			controller = self._controller_map[packet.entity]
			# That controller is the enemy player - return its opponent.
			self.friendly_player = controller % 2 + 1

	def handle_show_entity(self, packet):
		tags = dict(packet.tags)
		if GameTag.CONTROLLER in tags:
			self._controller_map[packet.entity] = tags[GameTag.CONTROLLER]

		if tags.get(GameTag.ZONE) == Zone.PLAY:
			# Ignore cards already in play (such as enchantments, common in TB)
			return

		# The first SHOW_ENTITY packet will always be the friendly player's.
		self.friendly_player = self._controller_map[packet.entity]
