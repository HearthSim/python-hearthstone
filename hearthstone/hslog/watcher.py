from ..enums import GameTag
from .parser import LogParser


class LogWatcher(LogParser):
	def on_entity_update(self, entity):
		pass

	def on_action(self, action):
		pass

	def on_metadata(self, metadata):
		pass

	def on_tag_change(self, entity, tag, value):
		pass

	def on_zone_change(self, entity, before, after):
		pass

	def on_game_ready(self, game, *players):
		pass

	def close_nodes(self):
		if self._entity_node:
			self.on_entity_update(self._entity_node)
		if self._metadata_node:
			self.on_metadata(self._metadata_node)
		super().close_nodes()

	def action_end(self, ts):
		action = super().action_end(ts)
		self.on_action(action)

	def full_entity(self, ts, id, cardid):
		super().full_entity(ts, id, cardid)
		# The first packet in a game is always FULL_ENTITY so
		# broadcast game_ready if we haven't yet for this game
		if not self.current_game._broadcasted:
			self.current_game._broadcasted = True
			self.on_game_ready(self.current_game, *self.current_game.players)

	def tag_change(self, ts, e, tag, value):
		entity = super().tag_change(ts, e, tag, value)

		if entity is not None:
			# Not broadcasting here when None simplifies our life
			self.on_tag_change(entity, tag, value)
			if tag == GameTag.ZONE:
				self.on_zone_change(entity, entity.zone, value)
