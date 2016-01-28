import re
from hearthstone import enums
from .utils import parse_enum, parse_tag
from .entities import Game, Player, Card


# Entity format
_E = r"(GameEntity|UNKNOWN HUMAN PLAYER|\[.+\]|\d+|.+)"
ENTITY_RE = re.compile("\[.*\s*id=(\d+)\s*.*\]")

# Line format
POWERLOG_LINE_RE = re.compile(r"^D ([\d:.]+) ([^(]+)\(\) - (.+)$")
OUTPUTLOG_LINE_RE = re.compile(r"\[Power\] ()([^(]+)\(\) - (.+)$")

# Game / Player
GAME_ENTITY_RE = re.compile(r"GameEntity EntityID=(\d+)")
PLAYER_ENTITY_RE = re.compile(r"Player EntityID=(\d+) PlayerID=(\d+) GameAccountId=\[hi=(\d+) lo=(\d+)\]$")

# Messages
CREATE_GAME_RE = re.compile(r"^CREATE_GAME$")
ACTION_START_RE = re.compile(r"ACTION_START Entity=%s (?:SubType|BlockType)=(\w+) Index=(-1|\d+) Target=%s$" % (_E, _E))
ACTION_END_RE = re.compile(r"^ACTION_END$")
FULL_ENTITY_CREATE_RE = re.compile(r"FULL_ENTITY - Creating ID=(\d+) CardID=(\w+)?$")
FULL_ENTITY_UPDATE_RE = re.compile(r"FULL_ENTITY - Updating %s CardID=(\w+)?$" % _E)
SHOW_ENTITY_RE = re.compile(r"SHOW_ENTITY - Updating Entity=%s CardID=(\w+)$" % _E)
HIDE_ENTITY_RE = re.compile(r"HIDE_ENTITY - Entity=%s tag=(\w+) value=(\w+)$" % _E)
TAG_CHANGE_RE = re.compile(r"TAG_CHANGE Entity=%s tag=(\w+) value=(\w+)" % _E)
META_DATA_RE = re.compile(r"META_DATA - Meta=(\w+) Data=%s Info=(\d+)" % _E)

# Message details
TAG_VALUE_RE = re.compile(r"tag=(\w+) value=(\w+)")
METADATA_INFO_RE = re.compile(r"Info\[(\d+)\] = %s" % _E)


MESSAGE_OPCODES = (
	"CREATE_GAME",
	"ACTION_START",
	"ACTION_END",
	"FULL_ENTITY",
	"SHOW_ENTITY",
	"HIDE_ENTITY",
	"TAG_CHANGE",
	"META_DATA",
)


class Action:  # :)
	def __init__(self, entity, type, index, target):
		self.entity = entity
		self.type = type
		self.index = index
		self.target = target
		self.ended = False
		self.packets = []

	def __repr__(self):
		return "%s(entity=%r, type=%r, index=%r, target=%r)" % (
			self.__class__.__name__, self.entity, self.type, self.index, self.target
		)

	def end(self):
		self.ended = True


class ActionMetaData:
	def __init__(self, type, entity):
		self.type = type
		self.entity = entity
		self.info = []

	def __repr__(self):
		return "%s(type=%r, entity=%r)" % (self.__class__.__name__, self.type, self.entity)


class LogBroadcastMixin:
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


class LogWatcher(LogBroadcastMixin):
	def __init__(self):
		self.games = []
		self.line_regex = POWERLOG_LINE_RE
		self._game_state_processor = "GameState"
		self.current_game = None
		self.current_action = None
		self._entity_node = None
		self._metadata_node = None

	def read(self, fp):
		for line in fp.readlines():
			sre = self.line_regex.match(line)
			if not sre:
				continue
			ts, method, msg = sre.groups()
			self.add_data(ts, method, msg)

	def parse_entity_id(self, entity):
		if entity.isdigit():
			return int(entity)

		if entity == "GameEntity":
			return self.current_game.id

		sre = ENTITY_RE.match(entity)
		if sre:
			id = sre.groups()[0]
			return int(id)

	def parse_entity(self, entity):
		id = self.parse_entity_id(entity)
		if not id:
			return self.current_game.find_player(entity)
		return self.current_game.entities[id]

	def parse_method(self, m):
		return "%s.%s" % (self._game_state_processor, m)

	def add_data(self, ts, callback, msg):
		if callback == self.parse_method("DebugPrintPower"):
			self.handle_data(ts, msg)

	def handle_data(self, ts, msg):
		data = msg.strip()
		opcode = msg.split()[0]

		if opcode in MESSAGE_OPCODES:
			return self.handle_action(ts, opcode, data)

		if opcode == "GameEntity":
			self.close_nodes()
			sre = GAME_ENTITY_RE.match(data)
			self.register_game(ts, *sre.groups())
		elif opcode == "Player":
			self.close_nodes()
			sre = PLAYER_ENTITY_RE.match(data)
			self.register_player(ts, *sre.groups())
		elif opcode.startswith("tag="):
			sre = TAG_VALUE_RE.match(data)
			tag, value = sre.groups()
			tag, value = parse_tag(tag, value)
			self._entity_node.tags[tag] = value
		elif opcode.startswith("Info["):
			sre = METADATA_INFO_RE.match(data)
			idx, entity = sre.groups()
			entity = self.parse_entity(entity)
			self._metadata_node.info.append(entity)
		else:
			raise NotImplementedError(data)

	def close_nodes(self):
		if self._entity_node:
			self.on_entity_update(self._entity_node)
			self._entity_node = None

		if self._metadata_node:
			self.on_metadata(self._metadata_node)
			self._metadata_node = None

	def handle_action(self, ts, opcode, data):
		self.close_nodes()

		if opcode == "CREATE_GAME":
			regex, callback = CREATE_GAME_RE, self.create_game
		elif opcode == "ACTION_START":
			regex, callback = ACTION_START_RE, self.action_start
		elif opcode == "ACTION_END":
			regex, callback = ACTION_END_RE, self.action_end
		elif opcode == "FULL_ENTITY":
			regex, callback = FULL_ENTITY_CREATE_RE, self.full_entity
		elif opcode == "SHOW_ENTITY":
			regex, callback = SHOW_ENTITY_RE, self.show_entity
		elif opcode == "HIDE_ENTITY":
			regex, callback = HIDE_ENTITY_RE, self.hide_entity
		elif opcode == "TAG_CHANGE":
			regex, callback = TAG_CHANGE_RE, self.tag_change
		elif opcode == "META_DATA":
			regex, callback = META_DATA_RE, self.meta_data
		else:
			raise NotImplementedError(data)

		sre = regex.match(data)
		callback(ts, *sre.groups())

	def register_game(self, ts, id):
		id = int(id)
		self.current_game.id = id
		self.current_game.register_entity(self.current_game)
		self._entity_node = self.current_game

	def register_player(self, ts, id, playerid, hi, lo):
		id = int(id)
		playerid = int(playerid)
		hi = int(hi)
		lo = int(lo)
		player = Player(id, playerid, hi, lo)
		self.current_game.register_entity(player)
		self._entity_node = player

	# Messages
	def create_game(self, ts):
		self.current_game = Game(0)
		self.games.append(self.current_game)
		self.current_game._broadcasted = False

	def action_start(self, ts, entity, type, index, target):
		entity = self.parse_entity(entity)
		type = parse_enum(enums.PowSubType, type)
		target = self.parse_entity(target)
		action = Action(entity, type, index, target)
		action.parent = self.current_action
		if self.current_action:
			self.current_action.packets.append(action)
		else:
			self.current_game.packets.append(action)
		self.current_action = action

	def action_end(self, ts):
		self.current_action.end()
		action = self.current_action
		self.current_action = self.current_action.parent
		self.on_action(action)

	def full_entity(self, ts, id, cardid):
		id = int(id)
		entity = Card(id, cardid)
		self.current_game.register_entity(entity)
		self._entity_node = entity

		# The first packet in a game is always FULL_ENTITY so
		# broadcast game_ready if we haven't yet for this game
		if not self.current_game._broadcasted:
			self.current_game._broadcasted = True
			self.on_game_ready(self.current_game, *self.current_game.players)

	def show_entity(self, ts, entity, cardid):
		entity = self.parse_entity(entity)
		entity.reveal(cardid)
		self._entity_node = entity

	def hide_entity(self, ts, entity, tag, value):
		entity = self.parse_entity(entity)
		entity.hide()

	def meta_data(self, ts, meta, data, info):
		type = parse_enum(enums.MetaDataType, meta)
		entity = self.parse_entity(data)
		self._metadata_node = ActionMetaData(type, entity)

	def tag_change(self, ts, e, tag, value):
		entity = self.parse_entity(e)
		tag, value = parse_tag(tag, value)

		# Hack to register player names...
		if entity is None and tag == enums.GameTag.ENTITY_ID:
			self.current_game.register_player_name(e, value)
			entity = self.parse_entity(e)

		if entity is not None:
			# Not broadcasting here when None simplifies our life
			self.on_tag_change(entity, tag, value)
			if tag == enums.GameTag.ZONE:
				self.on_zone_change(entity, entity.zone, value)

		if not entity:
			if tag == enums.GameTag.ENTITY_ID:
				self.current_game.register_player_name(e, value)
			else:
				# print("Warning: Unknown entity %r" % (e))
				pass
		else:
			entity.tag_change(tag, value)
