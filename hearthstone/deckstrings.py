"""
Blizzard Deckstring format support
"""

import base64
from io import BytesIO
from typing import IO, List, Optional, Sequence, Tuple

from .enums import FormatType


DECKSTRING_VERSION = 1


CardList = List[int]
CardIncludeList = List[Tuple[int, int]]
SideboardList = List[Tuple[int, int, int]]


def _read_varint(stream: IO) -> int:
	shift = 0
	result = 0
	while True:
		c = stream.read(1)
		if c == "":
			raise EOFError("Unexpected EOF while reading varint")
		i = ord(c)
		result |= (i & 0x7f) << shift
		shift += 7
		if not (i & 0x80):
			break

	return result


def _write_varint(stream: IO, i: int) -> int:
	buf = b""
	while True:
		towrite = i & 0x7f
		i >>= 7
		if i:
			buf += bytes((towrite | 0x80, ))
		else:
			buf += bytes((towrite, ))
			break

	return stream.write(buf)


class Deck:
	@classmethod
	def from_deckstring(cls, deckstring: str) -> "Deck":
		instance = cls()
		(
			instance.cards,
			instance.heroes,
			instance.format,
			instance.sideboards,
		) = parse_deckstring(deckstring)
		return instance

	def __init__(self):
		self.cards: CardIncludeList = []
		self.sideboards: SideboardList = []
		self.heroes: CardList = []
		self.format: FormatType = FormatType.FT_UNKNOWN

	@property
	def as_deckstring(self) -> str:
		return write_deckstring(self.cards, self.heroes, self.format, self.sideboards)

	def get_dbf_id_list(self) -> CardIncludeList:
		return sorted(self.cards, key=lambda x: x[0])

	def get_sideboard_dbf_id_list(self) -> SideboardList:
		return sorted(self.sideboards, key=lambda x: x[0])


def trisort_cards(cards: Sequence[tuple]) -> Tuple[
	List[tuple], List[tuple], List[tuple]
]:
	cards_x1: List[tuple] = []
	cards_x2: List[tuple] = []
	cards_xn: List[tuple] = []

	for card_elem in cards:
		sideboard_owner = None
		if len(card_elem) == 3:
			# Sideboard
			cardid, count, sideboard_owner = card_elem
		else:
			cardid, count = card_elem

		if count == 1:
			list = cards_x1
		elif count == 2:
			list = cards_x2
		else:
			list = cards_xn

		if len(card_elem) == 3:
			list.append((cardid, count, sideboard_owner))
		else:
			list.append((cardid, count))

	return cards_x1, cards_x2, cards_xn


def parse_deckstring(deckstring) -> (
	Tuple[CardIncludeList, CardList, FormatType, SideboardList]
):
	decoded = base64.b64decode(deckstring)
	data = BytesIO(decoded)

	# Header section

	if data.read(1) != b"\0":
		raise ValueError("Invalid deckstring")

	version = _read_varint(data)
	if version != DECKSTRING_VERSION:
		raise ValueError("Unsupported deckstring version %r" % (version))

	format = _read_varint(data)
	try:
		format = FormatType(format)
	except ValueError:
		raise ValueError("Unsupported FormatType in deckstring %r" % (format))

	# Heroes section

	heroes: CardList = []
	num_heroes = _read_varint(data)
	for i in range(num_heroes):
		heroes.append(_read_varint(data))
	heroes.sort()

	# Cards section

	cards: CardIncludeList = []

	num_cards_x1 = _read_varint(data)
	for i in range(num_cards_x1):
		card_id = _read_varint(data)
		cards.append((card_id, 1))

	num_cards_x2 = _read_varint(data)
	for i in range(num_cards_x2):
		card_id = _read_varint(data)
		cards.append((card_id, 2))

	num_cards_xn = _read_varint(data)
	for i in range(num_cards_xn):
		card_id = _read_varint(data)
		count = _read_varint(data)
		cards.append((card_id, count))

	cards.sort()

	# Sideboards section

	sideboards = []

	has_sideboards = data.read(1) == b"\1"

	if has_sideboards:
		num_sideboards_x1 = _read_varint(data)
		for i in range(num_sideboards_x1):
			card_id = _read_varint(data)
			sideboard_owner = _read_varint(data)
			sideboards.append((card_id, 1, sideboard_owner))

		num_sideboards_x2 = _read_varint(data)
		for i in range(num_sideboards_x2):
			card_id = _read_varint(data)
			sideboard_owner = _read_varint(data)
			sideboards.append((card_id, 2, sideboard_owner))

		num_sideboards_xn = _read_varint(data)
		for i in range(num_sideboards_xn):
			card_id = _read_varint(data)
			count = _read_varint(data)
			sideboard_owner = _read_varint(data)
			sideboards.append((card_id, count, sideboard_owner))

	sideboards.sort(key=lambda x: (x[2], x[0]))

	return cards, heroes, format, sideboards


def write_deckstring(
	cards: CardIncludeList,
	heroes: CardList,
	format: FormatType,
	sideboards: Optional[SideboardList] = None,
) -> str:
	if sideboards is None:
		sideboards = []

	data = BytesIO()
	data.write(b"\0")
	_write_varint(data, DECKSTRING_VERSION)
	_write_varint(data, int(format))

	if len(heroes) != 1:
		raise ValueError("Unsupported hero count %i" % (len(heroes)))
	_write_varint(data, len(heroes))
	for hero in sorted(heroes):
		_write_varint(data, hero)

	cards_x1, cards_x2, cards_xn = trisort_cards(cards)

	sort_key = lambda x: x[0]

	for cardlist in sorted(cards_x1, key=sort_key), sorted(cards_x2, key=sort_key):
		_write_varint(data, len(cardlist))
		for cardid, _ in cardlist:
			_write_varint(data, cardid)

	_write_varint(data, len(cards_xn))
	for cardid, count in sorted(cards_xn, key=sort_key):
		_write_varint(data, cardid)
		_write_varint(data, count)

	if len(sideboards) > 0:
		data.write(b"\1")

		sideboards_x1, sideboards_x2, sideboards_xn = trisort_cards(sideboards)

		sb_sort_key = lambda x: (x[2], x[0])

		for cardlist in (
			sorted(sideboards_x1, key=sb_sort_key),
			sorted(sideboards_x2, key=sb_sort_key)
		):
			_write_varint(data, len(cardlist))
			for cardid, _, sideboard_owner in cardlist:
				_write_varint(data, cardid)
				_write_varint(data, sideboard_owner)

		_write_varint(data, len(sideboards_xn))
		for cardid, count, sideboard_owner in sorted(sideboards_xn, key=sb_sort_key):
			_write_varint(data, cardid)
			_write_varint(data, count)
			_write_varint(data, sideboard_owner)

	else:
		data.write(b"\0")

	encoded = base64.b64encode(data.getvalue())
	return encoded.decode("utf-8")
