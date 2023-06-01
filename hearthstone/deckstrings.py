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
			instance.sideboard,
		) = parse_deckstring(deckstring)
		return instance

	def __init__(self):
		self.cards: CardIncludeList = []
		self.sideboard: SideboardList = []
		self.heroes: CardList = []
		self.format: FormatType = FormatType.FT_UNKNOWN

	@property
	def as_deckstring(self) -> str:
		return write_deckstring(self.cards, self.heroes, self.format, self.sideboard)

	def get_dbf_id_list(self) -> CardIncludeList:
		return sorted(self.cards, key=lambda x: x[0])

	def get_sideboard_dbf_id_list(self) -> SideboardList:
		return sorted(self.sideboard, key=lambda x: x[0])


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

	heroes: CardList = []
	num_heroes = _read_varint(data)
	for i in range(num_heroes):
		heroes.append(_read_varint(data))

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

	sideboard = []

	has_sideboard = data.read(1) == b"\1"

	if has_sideboard:
		num_sideboard_x1 = _read_varint(data)
		for i in range(num_sideboard_x1):
			card_id = _read_varint(data)
			sideboard_owner = _read_varint(data)
			sideboard.append((card_id, 1, sideboard_owner))

		num_sideboard_x2 = _read_varint(data)
		for i in range(num_sideboard_x2):
			card_id = _read_varint(data)
			sideboard_owner = _read_varint(data)
			sideboard.append((card_id, 2, sideboard_owner))

		num_sideboard_xn = _read_varint(data)
		for i in range(num_sideboard_xn):
			card_id = _read_varint(data)
			count = _read_varint(data)
			sideboard_owner = _read_varint(data)
			sideboard.append((card_id, count, sideboard_owner))

	return cards, heroes, format, sideboard


def write_deckstring(
	cards: CardIncludeList,
	heroes: CardList,
	format: FormatType,
	sideboard: Optional[SideboardList] = None,
) -> str:
	if sideboard is None:
		sideboard = []

	data = BytesIO()
	data.write(b"\0")
	_write_varint(data, DECKSTRING_VERSION)
	_write_varint(data, int(format))

	if len(heroes) != 1:
		raise ValueError("Unsupported hero count %i" % (len(heroes)))
	_write_varint(data, len(heroes))
	for hero in heroes:
		_write_varint(data, hero)

	cards_x1, cards_x2, cards_xn = trisort_cards(cards)

	for cardlist in cards_x1, cards_x2:
		_write_varint(data, len(cardlist))
		for cardid, _ in cardlist:
			_write_varint(data, cardid)

	_write_varint(data, len(cards_xn))
	for cardid, count in cards_xn:
		_write_varint(data, cardid)
		_write_varint(data, count)

	if len(sideboard) > 0:
		data.write(b"\1")

		sideboard_x1, sideboard_x2, sideboard_xn = trisort_cards(sideboard)

		for cardlist in sideboard_x1, sideboard_x2:
			_write_varint(data, len(cardlist))
			for cardid, _, sideboard_owner in cardlist:
				_write_varint(data, cardid)
				_write_varint(data, sideboard_owner)

		_write_varint(data, len(cards_xn))
		for cardid, count, sideboard_owner in sideboard_xn:
			_write_varint(data, cardid)
			_write_varint(data, count)
			_write_varint(data, sideboard_owner)

	else:
		data.write(b"\0")

	encoded = base64.b64encode(data.getvalue())
	return encoded.decode("utf-8")
