import logging
import re
from datetime import datetime
from hearthstone import enums
from ..enums import GameTag
from . import packets
from .utils import parse_enum, parse_tag
from .entities import Game, Player, Card


# Timestamp parsing
try:
	import dateutil.parser
	_default_date = datetime(1900, 1, 1)
	parse_timestamp = lambda ts: dateutil.parser.parse(ts, default=_default_date)
except ImportError:
	logging.warning(
		"python-dateutil is not installed. Timestamp parsing may not work properly."
	)
	def parse_timestamp(ts):
		# Unity logs have one character precision too much...
		return datetime.strptime(ts[:-1], TIMESTAMP_POWERLOG_FORMAT)


# Entity format
_E = r"(GameEntity|UNKNOWN HUMAN PLAYER|\[.+\]|\d+|.+)"
ENTITY_RE = re.compile("\[.*\s*id=(\d+)\s*.*\]")

# Line format
TIMESTAMP_POWERLOG_FORMAT = r"%H:%M:%S.%f"
TIMESTAMP_RE = re.compile(r"^D ([\d:.]+) (.+)$")
POWERLOG_LINE_RE = re.compile(r"([^(]+)\(\) - (.+)$")
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

# Choices
CHOICES_CHOICE_OLD_RE = re.compile(r"id=(\d+) PlayerId=(\d+) ChoiceType=(\w+) CountMin=(\d+) CountMax=(\d+)$")
CHOICES_CHOICE_RE = re.compile(r"id=(\d+) Player=%s TaskList=(\d+)? ChoiceType=(\w+) CountMin=(\d+) CountMax=(\d+)$" % _E)
CHOICES_SOURCE_RE = re.compile(r"Source=%s$" % _E)
CHOICES_ENTITIES_RE = re.compile(r"Entities\[(\d+)\]=(\[.+\])$")
SEND_CHOICES_CHOICE_RE = re.compile(r"id=(\d+) ChoiceType=(.+)$")
SEND_CHOICES_ENTITIES_RE = re.compile(r"m_chosenEntities\[(\d+)\]=(\[.+\])$")
ENTITIES_CHOSEN_RE = re.compile(r"id=(\d+) Player=%s EntitiesCount=(\d+)$" % _E)
ENTITIES_CHOSEN_ENTITIES_RE = re.compile(r"Entities\[(\d+)\]=%s$" % _E)

# Options
OPTIONS_ENTITY_RE = re.compile(r"id=(\d+)$")
OPTIONS_OPTION_RE = re.compile(r"option (\d+) type=(\w+) mainEntity=%s?$" % _E)
OPTIONS_SUBOPTION_RE = re.compile(r"(subOption|target) (\d+) entity=%s?$" % _E)
SEND_OPTION_RE = re.compile(r"selectedOption=(\d+) selectedSubOption=(-1|\d+) selectedTarget=(\d+) selectedPosition=(\d+)")

# Spectator mode
SPECTATOR_MODE_TOKEN = "=================="
SPECTATOR_MODE_BEGIN_GAME = "Begin Spectator Game"
SPECTATOR_MODE_BEGIN_FIRST = "Begin Spectating 1st player"
SPECTATOR_MODE_BEGIN_SECOND = "Begin Spectating 2nd player"
SPECTATOR_MODE_END_MODE = "End Spectator Mode"
SPECTATOR_MODE_END_GAME = "End Spectator Game"


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


class PowerHandler:
	def __init__(self):
		super().__init__()
		self.current_action = None
		self._entity_node = None
		self._metadata_node = None

	def add_data(self, ts, callback, msg):
		if callback == self.parse_method("DebugPrintPower"):
			self.handle_data(ts, msg)
			return True

	def handle_data(self, ts, data):
		opcode = data.split()[0]

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
			self._entity_packet.tags.append((tag, value))
		elif opcode.startswith("Info["):
			sre = METADATA_INFO_RE.match(data)
			idx, entity = sre.groups()
			entity = self.parse_entity(entity)
			self._metadata_node.info.append(entity)
		else:
			raise NotImplementedError(data)

	def close_nodes(self):
		if self._entity_node:
			for k, v in self._entity_packet.tags:
				self._entity_node.tags[k] = v
			self._entity_node = None

		if self._metadata_node:
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
			if data.startswith("FULL_ENTITY - Updating"):
				regex, callback = FULL_ENTITY_UPDATE_RE, self.full_entity_update
			else:
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

	# Messages
	def create_game(self, ts):
		self.current_action = None
		self.current_game = Game(0, ts)
		self.games.append(self.current_game)
		self.current_game._broadcasted = False
		self._entity_packet = packets.CreateGame(ts, self.current_game)
		self.current_node.packets.append(self._entity_packet)
		self._game_packet = self._entity_packet
		self.current_game.spectator_mode = self.spectator_mode

	def action_start(self, ts, entity, type, index, target):
		entity = self.parse_entity(entity)
		type = parse_enum(enums.PowSubType, type)
		index = int(index)
		target = self.parse_entity(target)
		action = packets.Action(ts, entity, type, index, target)
		action.parent = self.current_action
		self.current_node.packets.append(action)
		self.current_action = action

	def action_end(self, ts):
		self.current_action.end()
		action = self.current_action
		self.current_action = self.current_action.parent
		return action

	def full_entity(self, ts, id, cardid):
		id = int(id)
		entity = Card(id, cardid)
		self.current_game.register_entity(entity)
		self._entity_node = entity
		self._entity_packet = packets.FullEntity(ts, entity, cardid)
		self.current_node.packets.append(self._entity_packet)

	def full_entity_update(self, ts, entity, cardid):
		id = self.parse_entity_id(entity)
		return self.full_entity(ts, id, cardid)

	def show_entity(self, ts, entity, cardid):
		entity = self.parse_entity(entity)
		entity.reveal(cardid)
		self._entity_node = entity
		self._entity_packet = packets.ShowEntity(ts, entity, cardid)
		self.current_node.packets.append(self._entity_packet)

	def hide_entity(self, ts, entity, tag, value):
		entity = self.parse_entity(entity)
		entity.hide()
		tag, value = parse_tag(tag, value)
		assert tag == GameTag.ZONE
		packet = packets.HideEntity(ts, entity, value)
		self.current_node.packets.append(packet)

	def meta_data(self, ts, meta, data, info):
		type = parse_enum(enums.MetaDataType, meta)
		entity = self.parse_entity(data)
		count = int(info)
		self._metadata_node = packets.ActionMetaData(ts, entity, type, count)
		self.current_node.packets.append(self._metadata_node)

	def tag_change(self, ts, e, tag, value):
		entity = self.parse_entity(e)
		tag, value = parse_tag(tag, value)

		# Hack to register player names...
		if entity is None and tag == enums.GameTag.ENTITY_ID:
			self.register_player_name(self.current_game, e, value)
			entity = self.parse_entity(e)

		packet = packets.TagChange(ts, entity, tag, value)
		self.current_node.packets.append(packet)

		if not entity or isinstance(entity, str):
			if tag == enums.GameTag.ENTITY_ID:
				self.register_player_name(self.current_game, e, value)
			else:
				self.buffer_packet_entity_update(packet, e)
		else:
			entity.tag_change(tag, value)
		return entity


class OptionsHandler:
	def add_data(self, ts, callback, msg):
		if callback == self.parse_method("SendOption"):
			return self.handle_send_option(ts, msg)
		elif callback == self.parse_method("DebugPrintOptions"):
			return self.handle_options(ts, msg)

	def handle_options(self, ts, data):
		if data.startswith("id="):
			sre = OPTIONS_ENTITY_RE.match(data)
			id, = sre.groups()
			id = int(id)
			self._options_packet = packets.Options(ts, id)
			self.current_node.packets.append(self._options_packet)
		elif data.startswith("option "):
			sre = OPTIONS_OPTION_RE.match(data)
			id, type, entity = sre.groups()
			id = int(id)
			type = parse_enum(enums.OptionType, type)
			entity = self.parse_entity(entity) if entity else None
			self._option_packet = packets.Option(ts, entity, id, type, "option")
			self._options_packet.options.append(self._option_packet)
			self._suboption_packet = None
			return self._option_packet
		elif data.startswith(("subOption ", "target ")):
			sre = OPTIONS_SUBOPTION_RE.match(data)
			type, id, entity = sre.groups()
			id = int(id)
			entity = self.parse_entity(entity)
			packet = packets.Option(ts, entity, id, None, type)
			if type == "subOption":
				self._suboption_packet = packet
				node = self._option_packet
			elif type == "target":
				node = self._suboption_packet or self._option_packet
			node.options.append(packet)
			return packet

	def handle_send_option(self, ts, data):
		if data.startswith("selectedOption="):
			sre = SEND_OPTION_RE.match(data)
			option, suboption, target, position = sre.groups()
			packet = packets.SendOption(ts, int(option), int(suboption), int(target), int(position))
			self.current_node.packets.append(packet)
			return packet
		raise NotImplementedError("Unhandled send option: %r" % (data))


class ChoicesHandler:
	def add_data(self, ts, callback, msg):
		if callback == self.parse_method("DebugPrintEntityChoices"):
			return self.handle_entity_choices(ts, msg)
		elif callback == self.parse_method("DebugPrintChoices"):
			return self.handle_entity_choices_old(ts, msg)
		elif callback == self.parse_method("SendChoices"):
			return self.handle_send_choices(ts, msg)
		elif callback == self.parse_method("DebugPrintEntitiesChosen"):
			return self.handle_entities_chosen(ts, msg)

	def handle_entity_choices_old(self, ts, data):
		if data.startswith("id="):
			sre = CHOICES_CHOICE_OLD_RE.match(data)
			self.register_choices_old(ts, *sre.groups())
		else:
			return self.handle_entity_choices(ts, data)

	def handle_entity_choices(self, ts, data):
		if data.startswith("id="):
			sre = CHOICES_CHOICE_RE.match(data)
			return self.register_choices(ts, *sre.groups())
		elif data.startswith("Source="):
			sre = CHOICES_SOURCE_RE.match(data)
			entity, = sre.groups()
			entity = self.parse_entity(entity)
			self._choice_packet.source = entity
			return entity
		elif data.startswith("Entities["):
			sre = CHOICES_ENTITIES_RE.match(data)
			idx, entity = sre.groups()
			entity = self.parse_entity(entity)
			self._choice_packet.choices.append(entity)
			return entity
		raise NotImplementedError("Unhandled entity choice: %r" % (data))

	def _register_choices(self, ts, id, player, tasklist, type, min, max):
		id = int(id)
		type = parse_enum(enums.ChoiceType, type)
		min, max = int(min), int(max)
		self._choice_packet = packets.Choices(ts, player, id, tasklist, type, min, max)
		self.current_node.packets.append(self._choice_packet)
		return self._choice_packet

	def register_choices_old(self, ts, id, playerid, type, min, max):
		playerid = int(playerid)
		player = self.current_game.get_player(playerid)
		tasklist = None
		return self._register_choices(ts, id, player, tasklist, type, min, max)

	def register_choices(self, ts, id, player, tasklist, type, min, max):
		player = self.parse_entity(player)
		tasklist = int(tasklist)
		return self._register_choices(ts, id, player, tasklist, type, min, max)

	def handle_send_choices(self, ts, data):
		if data.startswith("id="):
			sre = SEND_CHOICES_CHOICE_RE.match(data)
			id, type = sre.groups()
			id = int(id)
			type = parse_enum(enums.ChoiceType, type)
			self._send_choice_packet = packets.SendChoices(ts, id, type)
			self.current_node.packets.append(self._send_choice_packet)
			return self._send_choice_packet
		elif data.startswith("m_chosenEntities"):
			sre = SEND_CHOICES_ENTITIES_RE.match(data)
			idx, entity = sre.groups()
			entity = self.parse_entity(entity)
			self._send_choice_packet.choices.append(entity)
			return entity
		raise NotImplementedError("Unhandled send choice: %r" % (data))

	def handle_entities_chosen(self, ts, data):
		if data.startswith("id="):
			sre = ENTITIES_CHOSEN_RE.match(data)
			id, player, count = sre.groups()
			id = int(id)
			player = self.parse_entity(player)
			self._chosen_packet_count = int(count)
			self._chosen_packet = packets.ChosenEntities(ts, player, id)
			self.current_node.packets.append(self._chosen_packet)
			return self._chosen_packet
		elif data.startswith("Entities["):
			sre = ENTITIES_CHOSEN_ENTITIES_RE.match(data)
			idx, entity = sre.groups()
			entity = self.parse_entity(entity)
			self._chosen_packet.choices.append(entity)
			assert len(self._chosen_packet.choices) <= self._chosen_packet_count
			return entity
		raise NotImplementedError("Unhandled entities chosen: %r" % (data))


class SpectatorModeHandler:
	def __init__(self):
		super().__init__()
		self.spectating_first_player = False
		self.spectating_second_player = False

	@property
	def spectator_mode(self):
		return self.spectating_first_player or self.spectating_second_player

	def set_spectating(self, first, second=None):
		self.spectating_first_player = first
		if second is not None:
			self.spectating_second_player = second

	def process_spectator_mode(self, line):
		if line == SPECTATOR_MODE_BEGIN_GAME:
			self.set_spectating(True)
		elif line == SPECTATOR_MODE_BEGIN_FIRST:
			self.set_spectating(True, False)
		elif line == SPECTATOR_MODE_BEGIN_SECOND:
			self.set_spectating(True, True)
		elif line == SPECTATOR_MODE_END_MODE:
			self.set_spectating(False, False)
		elif line == SPECTATOR_MODE_END_GAME:
			self.set_spectating(False, False)
		else:
			raise NotImplementedError("Unhandled spectator mode: %r" % (line))


class LogParser(PowerHandler, ChoicesHandler, OptionsHandler, SpectatorModeHandler):
	def __init__(self):
		super().__init__()
		self.games = []
		self.line_regex = POWERLOG_LINE_RE
		self._game_state_processor = "GameState"
		self.current_game = None
		self._player_buffer = {}

	@property
	def current_node(self):
		return self.current_action or self.current_game

	def add_data(self, ts, callback, msg):
		msg = msg.strip()
		for handler in PowerHandler, ChoicesHandler, OptionsHandler:
			ret = handler.add_data(self, ts, callback, msg)
			if ret:
				break

	def parse_timestamp(self, ts):
		ret = parse_timestamp(ts)
		if ret.year == 1900:
			# Logs without date :(
			return ret.time()
		return ret

	def read(self, fp):
		for line in fp.readlines():
			self.read_line(line)

	def read_line(self, line):
		sre = TIMESTAMP_RE.match(line)
		if not sre:
			raise ValueError("Invalid line format: %r" % (line))

		ts, line = sre.groups()
		ts = self.parse_timestamp(ts)
		if line.startswith(SPECTATOR_MODE_TOKEN):
			line = line.replace(SPECTATOR_MODE_TOKEN, "").strip()
			return self.process_spectator_mode(line)

		sre = self.line_regex.match(line)
		if sre:
			self.add_data(ts, *sre.groups())

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
			return self.current_game.find_player(entity) or entity
		return self.current_game.entities[id]

	def buffer_packet_entity_update(self, packet, name):
		"""
		Add a packet with a missing player entity to a buffer.
		The buffer will be updated with the correct entity once
		the player's name is registered.
		"""
		if name not in self._player_buffer:
			self._player_buffer[name] = []
		self._player_buffer[name].append(packet)

	def register_player_name(self, game, name, id):
		"""
		Register a player entity with a specific name.
		This is needed before a player name can be parsed as an
		entity id from the log.
		"""
		game.entities[id].name = name

		# Flush the player's buffer by name
		if name in self._player_buffer:
			entity = self.parse_entity(name)
			for packet in self._player_buffer[name]:
				packet.entity = entity
			del self._player_buffer[name]

		# Update the player's packet name
		if id in self._player_buffer:
			for packet in self._player_buffer[id]:
				packet.name = name
			del self._player_buffer[id]

	def parse_method(self, m):
		return "%s.%s" % (self._game_state_processor, m)

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
		self._entity_packet = packets.CreateGame.Player(ts, id, playerid, hi, lo)
		self._game_packet.players.append(self._entity_packet)
		self.buffer_packet_entity_update(self._entity_packet, id)
