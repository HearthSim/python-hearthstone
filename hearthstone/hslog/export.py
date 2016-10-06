from .. import entities
from . import packets


class BaseExporter:
	def __init__(self, packet_tree):
		self.packet_tree = packet_tree
		self.dispatch = self.get_dispatch_dict()

	def get_dispatch_dict(self):
		# These methods all need to be implemented
		# Or get_dispatch_dict() needs to be overridden
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

	def export_packet(self, packet):
		packet_type = packet.__class__
		handler = self.dispatch.get(packet_type, None)
		if not handler:
			raise NotImplementedError("Don't know how to export %r" % (packet_type))
		handler(packet)


class EntityTreeExporter(BaseExporter):
	game_class = entities.Game
	player_class = entities.Player
	card_class = entities.Card

	def handle_create_game(self, packet):
		self.game = self.game_class(packet.entity)
		self.game.register_entity(self.game)
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
		self.game.register_entity(entity)
		return entity

	def handle_block(self, packet):
		for p in packet.packets:
			self.export_packet(p)

	def handle_full_entity(self, packet):
		entity = self.card_class(packet.entity, packet.card_id)
		entity.tags = dict(packet.tags)
		self.game.register_entity(entity)
		return entity

	def handle_hide_entity(self, packet):
		entity = self.game.find_entity_by_id(packet.entity)
		entity.hide()
		return entity

	def handle_show_entity(self, packet):
		entity = self.game.find_entity_by_id(packet.entity)
		assert entity, "Attempting SHOW_ENTITY on entity %r (not found)" % (packet.entity)
		entity.reveal(packet.card_id, dict(packet.tags))
		return entity

	def handle_change_entity(self, packet):
		entity = self.game.find_entity_by_id(packet.entity)
		assert entity, "Attempting CHANGE_ENTITY on entity %r (not found)" % (packet.entity)
		entity.change(packet.card_id, dict(packet.tags))
		return entity

	def handle_tag_change(self, packet):
		entity = self.game.find_entity_by_id(packet.entity)
		assert entity, "Attempting TAG_CHANGE on entity %r (not found)" % (packet.entity)
		entity.tag_change(packet.tag, packet.value)
		return entity

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
