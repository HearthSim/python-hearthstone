import logging
import re
from datetime import datetime, timedelta
from hearthstone import enums
from hearthstone.entities import Entity, Card, Game, Player
from ..enums import GameTag, PowerType
from . import packets
from .utils import parse_enum, parse_tag


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


class PowerHandler(object):
	def __init__(self):
		super(PowerHandler, self).__init__()
		self.current_block = None
		self._entity_node = None
		self._metadata_node = None

	def _check_for_mulligan_hack(self, ts, entity, tag, value):
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

	def parse_initial_tag(self, data):
		sre = TAG_VALUE_RE.match(data)
		tag, value = sre.groups()
		return parse_tag(tag, value)

	def handle_data(self, ts, data):
		opcode = data.split()[0]

		if opcode in PowerType.__members__:
			return self.handle_power(ts, opcode, data)

		if opcode == "GameEntity":
			self.flush()
			sre = GAME_ENTITY_RE.match(data)
			self.register_game(ts, *sre.groups())
		elif opcode == "Player":
			self.flush()
			sre = PLAYER_ENTITY_RE.match(data)
			self.register_player(ts, *sre.groups())
		elif opcode.startswith("tag="):
			tag, value = self.parse_initial_tag(data)
			self._entity_packet.tags.append((tag, value))
		elif opcode.startswith("Info["):
			if not self._metadata_node:
				logging.warning("Metadata Info outside of META_DATA: %r", data)
				return
			sre = METADATA_INFO_RE.match(data)
			idx, entity = sre.groups()
			entity = self.parse_entity(entity)
			self._metadata_node.info.append(entity)
		else:
			raise NotImplementedError(data)

	def flush(self):
		if self._entity_node:
			for k, v in self._entity_packet.tags:
				self._entity_node.tags[k] = v
			self._entity_node = None

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
		self.current_game = Game(0)
		packet_tree = packets.PacketTree(ts)
		packet_tree.spectator_mode = self.spectator_mode
		packet_tree.game = self.current_game
		self.games.append(packet_tree)
		self.current_block = packet_tree
		self._entity_packet = packets.CreateGame(ts, self.current_game)
		self._game_packet = self._entity_packet
		self.current_block.packets.append(self._entity_packet)

	def block_start(self, ts, entity, type, index, effectid, effectindex, target):
		entity = self.parse_entity(entity)
		type = parse_enum(enums.BlockType, type)
		if index is not None:
			index = int(index)
		target = self.parse_entity(target)
		block = packets.Block(ts, entity, type, index, effectid, effectindex, target)
		block.parent = self.current_block
		self.current_block.packets.append(block)
		self.current_block = block

	def block_end(self, ts):
		if not self.current_block.parent:
			logging.warning("[%s] Orphaned BLOCK_END detected" % (ts))
			return self.current_block
		self.current_block.end()
		block = self.current_block
		self.current_block = self.current_block.parent
		return block

	def full_entity(self, ts, id, cardid):
		id = int(id)
		entity = Card(id, cardid)
		self.current_game.register_entity(entity)
		self._entity_node = entity
		self._entity_packet = packets.FullEntity(ts, entity, cardid)
		self.current_block.packets.append(self._entity_packet)

	def full_entity_update(self, ts, entity, cardid):
		id = self.parse_entity_id(entity)
		return self.full_entity(ts, id, cardid)

	def show_entity(self, ts, entity, cardid):
		entity = self.parse_entity(entity)
		entity.reveal(cardid)
		self._entity_node = entity
		self._entity_packet = packets.ShowEntity(ts, entity, cardid)
		self.current_block.packets.append(self._entity_packet)

	def hide_entity(self, ts, entity, tag, value):
		entity = self.parse_entity(entity)
		entity.hide()
		tag, value = parse_tag(tag, value)
		assert tag == GameTag.ZONE
		packet = packets.HideEntity(ts, entity, value)
		self.current_block.packets.append(packet)

	def change_entity(self, ts, entity, cardid):
		entity = self.parse_entity(entity)
		entity.change(cardid)
		self._entity_node = entity
		self._entity_packet = packets.ChangeEntity(ts, entity, cardid)
		self.current_block.packets.append(self._entity_packet)

	def meta_data(self, ts, meta, data, info):
		meta = parse_enum(enums.MetaDataType, meta)
		if meta == enums.MetaDataType.JOUST:
			data = self.parse_entity(data)
		count = int(info)
		self._metadata_node = packets.MetaData(ts, meta, data, count)
		self.current_block.packets.append(self._metadata_node)

	def tag_change(self, ts, e, tag, value):
		entity = self.parse_entity(e)
		tag, value = parse_tag(tag, value)
		self._check_for_mulligan_hack(ts, entity, tag, value)

		if not isinstance(entity, Entity):
			entity = self.check_for_player_registration(tag, value, e)

		packet = packets.TagChange(ts, entity, tag, value)
		self.current_block.packets.append(packet)

		if not entity or not isinstance(entity, Entity):
			if tag == enums.GameTag.ENTITY_ID:
				self.register_player_name(self.current_game, e, value)
			else:
				self.buffer_packet_entity_update(packet, e)
		else:
			entity.tag_change(tag, value)
		return entity


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
			self.current_block.packets.append(packet)
			return packet
		raise NotImplementedError("Unhandled send option: %r" % (data))


class ChoicesHandler:
	def find_callback(self, method):
		if method == self.parse_method("DebugPrintEntityChoices"):
			return self.handle_entity_choices
		elif method == self.parse_method("DebugPrintChoices"):
			return self.handle_entity_choices_old
		elif method == self.parse_method("SendChoices"):
			return self.handle_send_choices
		elif method == self.parse_method("DebugPrintEntitiesChosen"):
			return self.handle_entities_chosen

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
		self.current_block.packets.append(self._choice_packet)
		return self._choice_packet

	def register_choices_old_1(self, ts, id, type):
		player = None
		# XXX: We don't have a player here for old games.
		# Is it safe to assume CURRENT_PLAYER?
		tasklist = None
		min, max = 0, 0
		return self._register_choices(ts, id, player, tasklist, type, min, max)

	def register_choices_old_2(self, ts, id, playerid, type, min, max):
		playerid = int(playerid)
		player = self.current_game.get_player(playerid)
		tasklist = None
		return self._register_choices(ts, id, player, tasklist, type, min, max)

	def register_choices(self, ts, id, player, tasklist, type, min, max):
		player = self.parse_entity(player)
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
			self.current_block.packets.append(self._chosen_packet)
			return self._chosen_packet
		elif data.startswith("Entities["):
			sre = ENTITIES_CHOSEN_ENTITIES_RE.match(data)
			idx, entity = sre.groups()
			entity = self.parse_entity(entity)
			self._chosen_packet.choices.append(entity)
			assert len(self._chosen_packet.choices) <= self._chosen_packet_count
			return entity
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
		self.current_game = None
		self._player_buffer = {}
		self._current_date = None
		self._synced_timestamp = False

	def parse_timestamp(self, ts, method):
		ret = parse_timestamp(ts)

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

		if ret.year == 1900:
			# Logs without date :(
			if self._current_date is None:
				return ret.time()
			else:
				ret = ret.replace(
					year=self._current_date.year,
					month=self._current_date.month,
					day=self._current_date.day,
					tzinfo=self._current_date.tzinfo,
				)
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
		if id is None:
			return self.current_game.get_player(entity) or entity
		return self.current_game.find_entity_by_id(id)

	def buffer_packet_entity_update(self, packet, name):
		"""
		Add a packet with a missing player entity to a buffer.
		The buffer will be updated with the correct entity once
		the player's name is registered.
		"""
		if name not in self._player_buffer:
			self._player_buffer[name] = []
		self._player_buffer[name].append(packet)

	def check_for_player_registration(self, tag, value, e):
		"""
		Trigger on a tag change if we did not find a corresponding entity.
		"""
		# Double check whether both player names are already set
		if all(player.name for player in self.current_game.players):
			# If both players are already registered, there is a possibility
			# that "The Innkeeper" has been renamed.
			# It is also possible a previously-unknown entity is now known.
			for player in self.current_game.players:
				if player.is_ai or player.name == "UNKNOWN HUMAN PLAYER":
					# Transform the name to the new one.
					logging.warning("Re-registering %r as %r", player, e)
					self.register_player_name(self.current_game, e, player.id)
					return
			else:
				logging.warning("Unexpected player name: %r", e)
				assert False

		if tag == GameTag.ENTITY_ID:
			self.register_player_name(self.current_game, e, value	)
		elif tag == GameTag.CURRENT_PLAYER and self.current_game.setup_done:
			# Fallback hack (eg. in case of reconnected games)
			self.register_current_player_name(self.current_game, e, value)

		return self.parse_entity(e)

	def register_current_player_name(self, game, e, value):
		"""
		If we reconnect to a game, we watch for the CURRENT_PLAYER tag changes.
		When the current player changes, CURRENT_PLAYER is first *unset* on the
		current player and *then* set on the next player.
		"""
		current_player = game.current_player
		if not value:
			# First, this. We register the name to the current player.
			assert current_player
			self.register_player_name(game, e, current_player.id)
		elif not current_player:
			# And now, this. The name is registered to the non-current player
			# (meaning the one left without a name)
			for player in game.players:
				if not player.name:
					self.register_player_name(game, e, player.id)
					break
			else:
				# There is one remaining case: When the name "changes". This can
				# only happen if the name was unknown during setup.
				for player in game.players:
					if player.name == "UNKNOWN HUMAN PLAYER":
						self.register_player_name(game, e, player.id)
		else:
			# EDGE CASE! Seen in Decks Assemble.
			# If this happens, CURRENT_PLAYER is set to what it was already set to.
			# So the one being set is the current player already.
			self.register_player_name(game, e, current_player.id)

	def register_player_name(self, game, name, id):
		"""
		Register a player entity with a specific name.
		This is needed before a player name can be parsed as an
		entity id from the log.
		"""
		entity = game.find_entity_by_id(id)
		entity.name = name

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
		self._entity_packet = packets.CreateGame.Player(ts, player, playerid, hi, lo)
		self._game_packet.players.append(self._entity_packet)
		self.buffer_packet_entity_update(self._entity_packet, id)
