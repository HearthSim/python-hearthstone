import logging
import re
from datetime import datetime, timedelta
from aniso8601 import parse_time
from hearthstone import enums
from ..enums import GameTag, PowerType
from . import packets
from .player import LazyPlayer, PlayerManager
from .utils import parse_enum, parse_tag


# Entity format
GAME_ENTITY_TOKEN = "GameEntity"
_E = r"(%s|UNKNOWN HUMAN PLAYER|\[.+\]|\d+|.+)" % (GAME_ENTITY_TOKEN)
ENTITY_RE = re.compile("\[.*\s*id=(\d+)\s*.*\]")

# Line format
TIMESTAMP_POWERLOG_FORMAT = r"%H:%M:%S.%f"
TIMESTAMP_RE = re.compile(r"^(D|W) ([\d:.]+) (.+)$")
POWERLOG_LINE_RE = re.compile(r"([^(]+)\(\) - (.+)$")
OUTPUTLOG_LINE_RE = re.compile(r"\[Power\] ()([^(]+)\(\) - (.+)$")

# Game / Player
GAME_ENTITY_RE = re.compile(r"GameEntity EntityID=(\d+)")
PLAYER_ENTITY_RE = re.compile(r"Player EntityID=(\d+) PlayerID=(\d+) GameAccountId=\[hi=(\d+) lo=(\d+)\]$")

# Messages
CREATE_GAME_RE = re.compile(r"^CREATE_GAME$")
ACTION_START_OLD_RE = re.compile(r"ACTION_START Entity=%s (?:SubType|BlockType)=(\w+) Index=(-1|\d+) Target=%s$" % (_E, _E))
BLOCK_START_RE = re.compile(r"(?:ACTION|BLOCK)_START (?:SubType|BlockType)=(\w+) Entity=%s EffectCardId=(.*) EffectIndex=(-1|\d+) Target=%s$" % (_E, _E))  # Changed in 12051
BLOCK_END_RE = re.compile(r"^(?:ACTION|BLOCK)_END$")
FULL_ENTITY_CREATE_RE = re.compile(r"FULL_ENTITY - Creating ID=(\d+) CardID=(\w+)?$")
FULL_ENTITY_UPDATE_RE = re.compile(r"FULL_ENTITY - Updating %s CardID=(\w+)?$" % _E)
SHOW_ENTITY_RE = re.compile(r"SHOW_ENTITY - Updating Entity=%s CardID=(\w+)$" % _E)
HIDE_ENTITY_RE = re.compile(r"HIDE_ENTITY - Entity=%s tag=(\w+) value=(\w+)$" % _E)
CHANGE_ENTITY_RE = re.compile(r"CHANGE_ENTITY - Updating Entity=%s CardID=(\w+)$" % _E)
TAG_CHANGE_RE = re.compile(r"TAG_CHANGE Entity=%s tag=(\w+) value=(\w+)" % _E)
META_DATA_RE = re.compile(r"META_DATA - Meta=(\w+) Data=%s Info=(\d+)" % _E)

# Message details
TAG_VALUE_RE = re.compile(r"tag=(\w+) value=(\w+)")
METADATA_INFO_RE = re.compile(r"Info\[(\d+)\] = %s" % _E)

# Choices
CHOICES_CHOICE_OLD_1_RE = re.compile(r"id=(\d+) ChoiceType=(\w+)$")
CHOICES_CHOICE_OLD_2_RE = re.compile(r"id=(\d+) PlayerId=(\d+) ChoiceType=(\w+) CountMin=(\d+) CountMax=(\d+)$")
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
SPECTATOR_MODE_BEGIN_GAME = "Start Spectator Game"
SPECTATOR_MODE_BEGIN_FIRST = "Begin Spectating 1st player"
SPECTATOR_MODE_BEGIN_SECOND = "Begin Spectating 2nd player"
SPECTATOR_MODE_END_MODE = "End Spectator Mode"
SPECTATOR_MODE_END_GAME = "End Spectator Game"


def parse_entity_id(entity):
	if entity.isdigit():
		return int(entity)

	if entity == GAME_ENTITY_TOKEN:
		# GameEntity is always 1
		return 1

	sre = ENTITY_RE.match(entity)
	if sre:
		id = sre.groups()[0]
		return int(id)


def parse_initial_tag(data):
	"""
	Parse \a data, a line formatted as tag=FOO value=BAR
	Returns the values as int.
	"""
	sre = TAG_VALUE_RE.match(data)
	tag, value = sre.groups()
	return parse_tag(tag, value)


class PowerHandler(object):
	def __init__(self):
		super(PowerHandler, self).__init__()
		self.current_block = None
		self._metadata_node = None
		self._packets = None

	def _check_for_mulligan_hack(self, ts, tag, value):
		# Old game logs didn't handle asynchronous mulligans properly.
		# If we're missing an ACTION_END packet after the mulligan SendChoices,
		# we just close it out manually.
		if tag == enums.GameTag.MULLIGAN_STATE and value == enums.Mulligan.DEALING:
			assert self.current_block
			if isinstance(self.current_block, packets.Block):
				logging.warning("WARNING: Broken mulligan nesting. Working around...")
				self.block_end(ts)

	def find_callback(self, method):
		if method == self.parse_method("DebugPrintPower"):
			return self.handle_data

	def handle_data(self, ts, data):
		opcode = data.split()[0]

		if opcode in PowerType.__members__:
			return self.handle_power(ts, opcode, data)

		if opcode == "GameEntity":
			self.flush()
			sre = GAME_ENTITY_RE.match(data)
			id, = sre.groups()
			assert int(id) == 1, "GameEntity ID: Expected 1, got %r" % (id)
		elif opcode == "Player":
			self.flush()
			sre = PLAYER_ENTITY_RE.match(data)
			self.register_player(ts, *sre.groups())
		elif opcode.startswith("tag="):
			tag, value = parse_initial_tag(data)
			self._entity_packet.tags.append((tag, value))
			if tag == GameTag.CONTROLLER:
				# We need to know entity controllers for player name registration
				self._packets.manager.register_controller(self._entity_packet.entity, value)
		elif opcode.startswith("Info["):
			if not self._metadata_node:
				logging.warning("Metadata Info outside of META_DATA: %r", data)
				return
			sre = METADATA_INFO_RE.match(data)
			idx, entity = sre.groups()
			entity = self.parse_entity_or_player(entity)
			self._metadata_node.info.append(entity)
		else:
			raise NotImplementedError(data)

	def flush(self):
		super(PowerHandler, self).flush()
		if self._metadata_node:
			self._metadata_node = None

	def handle_power(self, ts, opcode, data):
		self.flush()

		if opcode == "CREATE_GAME":
			regex, callback = CREATE_GAME_RE, self.create_game
		elif opcode in ("ACTION_START", "BLOCK_START"):
			sre = BLOCK_START_RE.match(data)
			if sre is None:
				sre = ACTION_START_OLD_RE.match(data)
				entity, type, index, target = sre.groups()
				effectid, effectindex = None, None
			else:
				type, entity, effectid, effectindex, target = sre.groups()
				index = None
			self.block_start(ts, entity, type, index, effectid, effectindex, target)
			return
		elif opcode in ("ACTION_END", "BLOCK_END"):
			regex, callback = BLOCK_END_RE, self.block_end
		elif opcode == "FULL_ENTITY":
			if data.startswith("FULL_ENTITY - Updating"):
				regex, callback = FULL_ENTITY_UPDATE_RE, self.full_entity_update
			else:
				regex, callback = FULL_ENTITY_CREATE_RE, self.full_entity
		elif opcode == "SHOW_ENTITY":
			regex, callback = SHOW_ENTITY_RE, self.show_entity
		elif opcode == "HIDE_ENTITY":
			regex, callback = HIDE_ENTITY_RE, self.hide_entity
		elif opcode == "CHANGE_ENTITY":
			regex, callback = CHANGE_ENTITY_RE, self.change_entity
		elif opcode == "TAG_CHANGE":
			regex, callback = TAG_CHANGE_RE, self.tag_change
		elif opcode == "META_DATA":
			regex, callback = META_DATA_RE, self.meta_data
		else:
			raise NotImplementedError(data)

		sre = regex.match(data)
		if not sre:
			logging.warning("Could not correctly parse %r", data)
			return
		callback(ts, *sre.groups())

	# Messages
	def create_game(self, ts):
		entity_id = 1
		self._packets = packets.PacketTree(ts)
		self._packets.spectator_mode = self.spectator_mode
		self._packets.manager = PlayerManager()
		self._entity_packet = packets.CreateGame(ts, entity_id)
		self._game_packet = self._entity_packet
		self.current_block = self._packets
		self.current_block.packets.append(self._entity_packet)
		self.games.append(self._packets)
		return self._game_packet

	def block_start(self, ts, entity, type, index, effectid, effectindex, target):
		id = self.parse_entity_or_player(entity)
		type = parse_enum(enums.BlockType, type)
		if index is not None:
			index = int(index)
		target = self.parse_entity_or_player(target)
		block = packets.Block(ts, id, type, index, effectid, effectindex, target)
		block.parent = self.current_block
		self.current_block.packets.append(block)
		self.current_block = block
		return block

	def block_end(self, ts):
		if not self.current_block.parent:
			logging.warning("[%s] Orphaned BLOCK_END detected", ts)
			return self.current_block
		self.current_block.end()
		block = self.current_block
		self.current_block = self.current_block.parent
		return block

	def full_entity(self, ts, id, card_id):
		id = int(id)
		self._entity_packet = packets.FullEntity(ts, id, card_id)
		self.current_block.packets.append(self._entity_packet)
		return self._entity_packet

	def full_entity_update(self, ts, entity, card_id):
		id = parse_entity_id(entity)
		return self.full_entity(ts, id, card_id)

	def show_entity(self, ts, entity, card_id):
		id = parse_entity_id(entity)
		self._entity_packet = packets.ShowEntity(ts, id, card_id)
		self.current_block.packets.append(self._entity_packet)
		return self._entity_packet

	def hide_entity(self, ts, entity, tag, value):
		id = parse_entity_id(entity)
		tag, value = parse_tag(tag, value)
		assert tag == GameTag.ZONE
		packet = packets.HideEntity(ts, id, value)
		self.current_block.packets.append(packet)
		return packet

	def change_entity(self, ts, entity, card_id):
		id = self.parse_entity_or_player(entity)
		self._entity_packet = packets.ChangeEntity(ts, id, card_id)
		self.current_block.packets.append(self._entity_packet)
		return self._entity_packet

	def meta_data(self, ts, meta, data, info):
		meta = parse_enum(enums.MetaDataType, meta)
		if meta == enums.MetaDataType.JOUST:
			data = parse_entity_id(data)
		count = int(info)
		self._metadata_node = packets.MetaData(ts, meta, data, count)
		self.current_block.packets.append(self._metadata_node)
		return self._metadata_node

	def tag_change(self, ts, e, tag, value):
		id = self.parse_entity_or_player(e)
		tag, value = parse_tag(tag, value)
		self._check_for_mulligan_hack(ts, tag, value)

		if isinstance(id, LazyPlayer):
			id = self._packets.manager.register_player_name_on_tag_change(id, tag, value)

		packet = packets.TagChange(ts, id, tag, value)
		self.current_block.packets.append(packet)
		return packet


class OptionsHandler(object):
	def find_callback(self, method):
		if method == self.parse_method("SendOption"):
			return self.handle_send_option
		elif method == self.parse_method("DebugPrintOptions"):
			return self.handle_options

	def handle_options(self, ts, data):
		if data.startswith("id="):
			sre = OPTIONS_ENTITY_RE.match(data)
			id, = sre.groups()
			id = int(id)
			self._options_packet = packets.Options(ts, id)
			self.current_block.packets.append(self._options_packet)
		elif data.startswith("option "):
			sre = OPTIONS_OPTION_RE.match(data)
			id, type, entity = sre.groups()
			id = int(id)
			type = parse_enum(enums.OptionType, type)
			entity_id = parse_entity_id(entity) if entity else None
			self._option_packet = packets.Option(ts, entity_id, id, type, "option")
			self._options_packet.options.append(self._option_packet)
			self._suboption_packet = None
			return self._option_packet
		elif data.startswith(("subOption ", "target ")):
			sre = OPTIONS_SUBOPTION_RE.match(data)
			type, id, entity = sre.groups()
			id = int(id)
			entity_id = parse_entity_id(entity)
			packet = packets.Option(ts, entity_id, id, None, type)
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
			self.current_block.packets.append(packet)
			return packet
		raise NotImplementedError("Unhandled send option: %r" % (data))


class ChoicesHandler(object):
	def __init__(self):
		super(ChoicesHandler, self).__init__()
		self._choice_packet = None
		self._chosen_packet = None
		self._send_choice_packet = None

	def find_callback(self, method):
		if method == self.parse_method("DebugPrintEntityChoices"):
			return self.handle_entity_choices
		elif method == self.parse_method("DebugPrintChoices"):
			return self.handle_entity_choices_old
		elif method == self.parse_method("SendChoices"):
			return self.handle_send_choices
		elif method == self.parse_method("DebugPrintEntitiesChosen"):
			return self.handle_entities_chosen

	def flush(self):
		if self._choice_packet:
			if self._choice_packet.type == enums.ChoiceType.MULLIGAN:
				self._packets.manager.register_player_name_mulligan(self._choice_packet)
			self._choice_packet = None
		if self._chosen_packet:
			self._chosen_packet = None
		if self._send_choice_packet:
			self._send_choice_packet = None

	def handle_entity_choices_old(self, ts, data):
		if data.startswith("id="):
			sre = CHOICES_CHOICE_OLD_1_RE.match(data)
			if sre:
				self.register_choices_old_1(ts, *sre.groups())
			else:
				sre = CHOICES_CHOICE_OLD_2_RE.match(data)
				self.register_choices_old_2(ts, *sre.groups())
		else:
			return self.handle_entity_choices(ts, data)

	def handle_entity_choices(self, ts, data):
		if data.startswith("id="):
			sre = CHOICES_CHOICE_RE.match(data)
			return self.register_choices(ts, *sre.groups())
		elif data.startswith("Source="):
			sre = CHOICES_SOURCE_RE.match(data)
			entity, = sre.groups()
			id = self.parse_entity_or_player(entity)
			self._choice_packet.source = id
			return id
		elif data.startswith("Entities["):
			sre = CHOICES_ENTITIES_RE.match(data)
			idx, entity = sre.groups()
			id = self.parse_entity_or_player(entity)
			assert id, "Missing choice entity %r (%r)" % (id, entity)
			self._choice_packet.choices.append(id)
			return id
		raise NotImplementedError("Unhandled entity choice: %r" % (data))

	def _register_choices(self, ts, id, player, tasklist, type, min, max):
		id = int(id)
		type = parse_enum(enums.ChoiceType, type)
		min, max = int(min), int(max)
		self._choice_packet = packets.Choices(ts, player, id, tasklist, type, min, max)
		self.current_block.packets.append(self._choice_packet)
		return self._choice_packet

	def register_choices_old_1(self, ts, id, type):
		player = None
		# XXX: We don't have a player here for old games.
		# Is it safe to assume CURRENT_PLAYER?
		tasklist = None
		min, max = 0, 0
		return self._register_choices(ts, id, player, tasklist, type, min, max)

	def register_choices_old_2(self, ts, id, player_id, type, min, max):
		player_id = int(player_id)
		player = self._packets.manager._players_by_player_id[player_id]
		tasklist = None
		return self._register_choices(ts, id, player, tasklist, type, min, max)

	def register_choices(self, ts, id, player, tasklist, type, min, max):
		player = self.parse_entity_or_player(player)
		if tasklist is not None:
			# Sometimes tasklist is empty
			tasklist = int(tasklist)
		return self._register_choices(ts, id, player, tasklist, type, min, max)

	def handle_send_choices(self, ts, data):
		if data.startswith("id="):
			sre = SEND_CHOICES_CHOICE_RE.match(data)
			id, type = sre.groups()
			id = int(id)
			type = parse_enum(enums.ChoiceType, type)
			self._send_choice_packet = packets.SendChoices(ts, id, type)
			self.current_block.packets.append(self._send_choice_packet)
			return self._send_choice_packet
		elif data.startswith("m_chosenEntities"):
			sre = SEND_CHOICES_ENTITIES_RE.match(data)
			idx, entity = sre.groups()
			id = self.parse_entity_or_player(entity)
			assert id, "Missing chosen entity %r (%r)" % (id, entity)
			self._send_choice_packet.choices.append(id)
			return id
		raise NotImplementedError("Unhandled send choice: %r" % (data))

	def handle_entities_chosen(self, ts, data):
		if data.startswith("id="):
			sre = ENTITIES_CHOSEN_RE.match(data)
			id, player, count = sre.groups()
			id = int(id)
			player = self.parse_entity_or_player(player)
			self._chosen_packet_count = int(count)
			self._chosen_packet = packets.ChosenEntities(ts, player, id)
			self.current_block.packets.append(self._chosen_packet)
			return self._chosen_packet
		elif data.startswith("Entities["):
			sre = ENTITIES_CHOSEN_ENTITIES_RE.match(data)
			idx, entity = sre.groups()
			id = self.parse_entity_or_player(entity)
			assert id, "Missing entity chosen %r (%r)" % (id, entity)
			self._chosen_packet.choices.append(id)
			assert len(self._chosen_packet.choices) <= self._chosen_packet_count
			return id
		raise NotImplementedError("Unhandled entities chosen: %r" % (data))


class SpectatorModeHandler(object):
	def __init__(self):
		super(SpectatorModeHandler, self).__init__()
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
		super(LogParser, self).__init__()
		self.games = []
		self.line_regex = POWERLOG_LINE_RE
		self._game_state_processor = "GameState"
		self._current_date = None
		self._synced_timestamp = False

	def parse_timestamp(self, ts, method):
		ret = parse_time(ts)

		if not self._synced_timestamp:
			# The first timestamp we parse requires syncing the time
			# (in case _current_date is greater than the start date)
			if self._current_date is not None:
				self._current_date = self._current_date.replace(
					hour=ret.hour,
					minute=ret.minute,
					second=ret.second,
					microsecond=ret.microsecond,
				)
			# Only do it once per parse tree
			self._synced_timestamp = True

		# Logs don't have dates :(
		if self._current_date is None:
			# No starting date is available. Return just the time.
			return ret

		ret = datetime.combine(self._current_date, ret)
		ret = ret.replace(tzinfo=self._current_date.tzinfo)
		if ret < self._current_date:
			# If the new date falls before the last saved date, that
			# means we rolled over and need to increment the day by 1.
			ret += timedelta(days=1)
		self._current_date = ret
		return ret

	def read(self, fp):
		for line in fp:
			self.read_line(line)

	def read_line(self, line):
		sre = TIMESTAMP_RE.match(line)
		if not sre:
			raise ValueError("Invalid line format: %r" % (line))

		level, ts, line = sre.groups()
		if line.startswith(SPECTATOR_MODE_TOKEN):
			line = line.replace(SPECTATOR_MODE_TOKEN, "").strip()
			return self.process_spectator_mode(line)

		sre = self.line_regex.match(line)
		if sre:
			method, msg = sre.groups()
			msg = msg.strip()
			if not self.current_block and "CREATE_GAME" not in msg:
				logging.warning("No game available - ignoring %r", line)
				return
			for handler in PowerHandler, ChoicesHandler, OptionsHandler:
				callback = handler.find_callback(self, method)
				if callback:
					ts = self.parse_timestamp(ts, method)
					return callback(ts, msg)

	def parse_entity_or_player(self, entity):
		id = parse_entity_id(entity)
		if id is None:
			# Only case where an id is None is if it's a Player name
			id = self._packets.manager.get_player_by_name(entity)
		return id

	def parse_method(self, m):
		return "%s.%s" % (self._game_state_processor, m)

	def register_player(self, ts, id, player_id, hi, lo):
		id = int(id)
		player_id = int(player_id)
		hi = int(hi)
		lo = int(lo)
		lazy_player = self._packets.manager.new_player(id, player_id, is_ai=lo == 0)
		self._entity_packet = packets.CreateGame.Player(ts, lazy_player, player_id, hi, lo)
		self._game_packet.players.append(self._entity_packet)
		return lazy_player
