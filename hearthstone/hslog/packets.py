from ..enums import GameTag, PowerType, Zone


def find_unknown_full_entity_in_hand(packets):
	"""
	Finds the first unknown in-hand entity in \a packets list.
	Returns its controller's ID.
	This is the behaviour used before patch 13619 to guess the friendly player.
	"""
	for packet in packets:
		if packet.power_type != PowerType.FULL_ENTITY:
			# We are past the initial FULL_ENTITY block
			return
		tags = dict(packet.tags)
		if tags[GameTag.ZONE] == Zone.HAND and not packet.cardid:
			return tags[GameTag.CONTROLLER]


def find_show_entity(packets):
	"""
	Finds the first SHOW_ENTITY in \a packets list (not in PLAY zone).
	Returns its controller's ID.
	This is the behaviour used as of patch 13619 to guess the friendly player.
	"""
	for packet in packets:
		if packet.power_type == PowerType.SHOW_ENTITY:
			if packet.entity.tags.get(GameTag.ZONE) == Zone.PLAY:
				# Ignore cards already in play (such as enchantments, common in TB)
				continue
			return packet.entity.tags[GameTag.CONTROLLER]
		elif packet.power_type == PowerType.BLOCK_START:
			ret = find_show_entity(packet.packets)
			if ret:
				return ret


class PacketTree:
	def __init__(self, ts):
		self.ts = ts
		self.packets = []
		self.parent = None

	def __iter__(self):
		for packet in self.packets:
			yield packet

	@property
	def start_time(self):
		for packet in self.packets:
			if packet.ts:
				return packet.ts

	@property
	def end_time(self):
		for packet in self.packets[::-1]:
			if packet.ts:
				return packet.ts

	def guess_friendly_player(self, attempt_old=False):
		"""
		Attempt to guess the friendly player in the game by
		looking for initial unrevealed cards.
		Will not work very early in game initialization and
		produce incorrect results if both hands are revealed.
		\a attempt_old should be True for pre-13619 logs.
		"""
		packets = self.packets[1:]

		if attempt_old:
			# Pre-13619: The first FULL_ENTITY packet which is in Zone.HAND and
			# does *not* have an ID is owned by the friendly player's *opponent*.
			controller = find_unknown_full_entity_in_hand(packets)
			if controller:
				# That controller is the enemy player - return its opponent.
				return controller % 2 + 1

		# Post-13619: The FULL_ENTITY packets no longer contain initial
		# card data, a SHOW_ENTITY always has to happen.
		# The first SHOW_ENTITY packet *will* be the friendly player's.
		return find_show_entity(packets)


class Packet:
	power_type = 0

	def __repr__(self):
		return "<%s>" % (self.__class__.__name__)


class Block(Packet):
	power_type = PowerType.BLOCK_START

	def __init__(self, ts, entity, type, index, effectid, effectindex, target):
		self.ts = ts
		self.entity = entity
		self.type = type
		self.index = index
		self.effectid = effectid
		self.effectindex = effectindex
		self.target = target
		self.ended = False
		self.packets = []

	def __iter__(self):
		for packet in self.packets:
			yield packet

	def __repr__(self):
		return "%s(entity=%r, type=%r, index=%r, target=%r)" % (
			self.__class__.__name__, self.entity, self.type, self.index, self.target
		)

	def end(self):
		self.ended = True


class MetaData(Packet):
	power_type = PowerType.META_DATA

	def __init__(self, ts, meta, data, count):
		self.ts = ts
		self.meta = meta
		self.data = data
		self.count = count
		self.info = []

	def __repr__(self):
		return "%s(meta=%r, data=%r)" % (self.__class__.__name__, self.meta, self.data)


class CreateGame(Packet):
	power_type = PowerType.CREATE_GAME

	class Player:
		def __init__(self, ts, entity, playerid, hi, lo):
			self.ts = ts
			self.entity = entity
			self.playerid = playerid
			self.hi = hi
			self.lo = lo
			self.name = ""
			self.tags = []

	def __init__(self, ts, entity):
		self.ts = ts
		self.entity = entity
		self.tags = []
		self.players = []


class HideEntity(Packet):
	power_type = PowerType.HIDE_ENTITY

	def __init__(self, ts, entity, zone):
		self.ts = ts
		self.entity = entity
		self.zone = zone


class FullEntity(Packet):
	power_type = PowerType.FULL_ENTITY

	def __init__(self, ts, entity, cardid):
		self.ts = ts
		self.entity = entity
		self.cardid = cardid
		self.tags = []


class ShowEntity(Packet):
	power_type = PowerType.SHOW_ENTITY

	def __init__(self, ts, entity, cardid):
		self.ts = ts
		self.entity = entity
		self.cardid = cardid
		self.tags = []


class ChangeEntity(Packet):
	power_type = PowerType.CHANGE_ENTITY

	def __init__(self, ts, entity, cardid):
		self.ts = ts
		self.entity = entity
		self.cardid = cardid
		self.tags = []


class TagChange(Packet):
	power_type = PowerType.TAG_CHANGE

	def __init__(self, ts, entity, tag, value):
		self.ts = ts
		self.entity = entity
		self.tag = tag
		self.value = value


class Choices(Packet):
	def __init__(self, ts, entity, id, tasklist, type, min, max):
		self.ts = ts
		self.entity = entity
		self.id = id
		self.tasklist = tasklist
		self.type = type
		self.min = min
		self.max = max
		self.source = None
		self.choices = []

	@property
	def player(self):
		return self.entity


class SendChoices(Packet):
	def __init__(self, ts, id, type):
		self.ts = ts
		self.entity = None
		self.id = id
		self.type = type
		self.choices = []


class ChosenEntities(Packet):
	def __init__(self, ts, entity, id):
		self.ts = ts
		self.entity = entity
		self.id = id
		self.choices = []


class Options(Packet):
	def __init__(self, ts, id):
		self.ts = ts
		self.entity = None
		self.id = id
		self.options = []


class Option(Packet):
	def __init__(self, ts, entity, id, type, optype):
		self.ts = ts
		self.entity = entity
		self.id = id
		self.type = type
		self.optype = optype
		self.options = []


class SendOption(Packet):
	def __init__(self, ts, option, suboption, target, position):
		self.ts = ts
		self.entity = None
		self.option = option
		self.suboption = suboption
		self.target = target
		self.position = position
