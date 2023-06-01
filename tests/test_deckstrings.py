from hearthstone import deckstrings
from hearthstone.enums import FormatType


TEST_DECKSTRING_PRE_SIDEBOARD = (
	"AAEBAR8G+LEChwTmwgKhwgLZwgK7BQzquwKJwwKOwwKTwwK5tAK1A/4MqALsuwLrB86uAu0JAA=="
)
TEST_DECKSTRING = (
	"AAEBAR8GhwS7BfixAqHCAtnCAubCAgyoArUD6wftCf4Mzq4CubQC6rsC7LsCicMCjsMCk8MCAAA="
)
TEST_DECKSTRING_CARDLIST = [
	(40426, 2),  # Alleycat
	(41353, 2),  # Jeweled Macaw
	(39160, 1),  # Cat Trick
	(41358, 2),  # Crackling Razormaw
	(41363, 2),  # Dinomancy
	(519, 1),  # Freezing Trap
	(39481, 2),  # Kindly Grandmother
	(41318, 1),  # Stubborn Gastropod
	(437, 2),  # Animal Companion
	(1662, 2),  # Eaglehorn Bow
	(41249, 1),  # Eggnapper
	(296, 2),  # Kill Command
	(40428, 2),  # Rat Pack
	(1003, 2),  # Houndmaster
	(38734, 2),  # Infested Wolf
	(41305, 1),  # Nesting Roc
	(699, 1),  # Tundra Rhino
	(1261, 2),  # Savannah Highmane
]

TEST_SIDEBOARD_DECKSTRING = (
	"AAEBAZCaBgjlsASotgSX7wTvkQXipAX9xAXPxgXGxwUQvp8EobYElrcE+dsEuNwEutwE9v"
	"AEhoMFopkF4KQFlMQFu8QFu8cFuJ4Gz54G0Z4GAAED8J8E/cQFuNkE/cQF/+EE/cQFAAA="
)
TEST_SIDEBOARD_DECKSTRING_CARDLIST = [
	(102223, 2),  # Armor Vendor
	(69566, 2),  # Psychic Conjurer
	(102200, 2),  # Shard of the Naaru
	(71781, 1),  # Sir Finley, Sea Guide
	(77305, 2),  # The Light! It Burns!
	(86626, 1),  # Astalor Bloodsworn
	(91078, 1),  # Audio Amplifier
	(102225, 2),  # Dirty Rat
	(90644, 2),  # Mind Eater
	(91067, 2),  # Power Chord: Synchronize
	(82310, 2),  # Cathedral of Atonement
	(77368, 2),  # Identity Theft
	(90959, 1),  # Love Everlasting
	(85154, 2),  # Nerubian Vizier
	(79767, 1),  # Prince Renathal
	(86624, 2),  # Cannibalize
	(79990, 2),  # Demolition Renovator
	(90749, 1),  # E.T.C., Band Manager
	(72598, 2),  # School Teacher
	(77370, 2),  # Clean the Scene
	(90683, 2),  # Harmonic Pop
	(84207, 1),  # Sister Svalna
	(72488, 1),  # Blackwater Behemoth
	(72481, 2),  # Whirlpool
]
TEST_SIDEBOARD_DECKSTRING_SIDEBOARD = [
	(69616, 1, 90749),
	(76984, 1, 90749),
	(78079, 1, 90749),
]


DECKSTRING_TEST_DATA = [
	{
		"cards": [(1, 2), (2, 2), (3, 2), (4, 2)],
		"heroes": [7],  # Garrosh Hellscream
		"format": FormatType.FT_STANDARD,
		"deckstring": "AAECAQcABAECAwQAAA==",
	},
	{
		"cards": [(8, 1), (179, 1), (2009, 1)],
		"heroes": [7],
		"format": FormatType.FT_STANDARD,
		"deckstring": "AAECAQcDCLMB2Q8AAAA=",
	},
	{
		"cards": [(1, 3), (2, 3), (3, 3), (4, 3)],
		"heroes": [7],  # Garrosh Hellscream
		"format": FormatType.FT_WILD,
		"deckstring": "AAEBAQcAAAQBAwIDAwMEAwA=",
	},
	{
		"cards": [(1, 1), (2, 1), (3, 1), (4, 1)],
		"heroes": [40195],  # Maiev Shadowsong
		"format": FormatType.FT_WILD,
		"deckstring": "AAEBAYO6AgQBAgMEAAAA",
	},
	{
		# https://hsreplay.net/decks/mae2HTeLYbTIrSYZiALN9d/
		"cards": [
			(41323, 2),  # Fire Fly
			(376, 2),  # Inner Fire
			(1650, 2),  # Northshire Cleric
			(40373, 1),  # Potion of Madness
			(613, 2),  # Power Word: Shield
			(1361, 2),  # Divine Spirit
			(41176, 2),  # Radiant Elemental
			(41169, 2),  # Shadow Visions
			(1367, 2),  # Shadow Word: Pain
			(40432, 2),  # Kabal Talonpriest
			(1363, 2),  # Shadow Word: Death
			(41418, 2),  # Tar Creeper
			(41241, 2),  # Tol'vir Stoneshaper
			(41180, 1),  # Tortollan Shellraiser
			(42046, 1),  # Lyra the Sunshard
			(41410, 2),  # Servant of Kalimos
			(41928, 1),  # Blazecaller
		],
		"format": FormatType.FT_STANDARD,
		"heroes": [41887],  # Tyrande Whisperwind
		"deckstring": (
			"AAECAZ/HAgS1uwLcwQK+yALIxwIN68IC+ALyDOUE0QrYwQLRwQLXCvC7AtMKysMCmcICwsMCAAA="
		)
	},
	{
		"cards": [
			(455, 1),
			(585, 1),
			(699, 1),
			(921, 1),
			(985, 1),
			(1144, 1),
			(141, 2),
			(216, 2),
			(296, 2),
			(437, 2),
			(519, 2),
			(658, 2),
			(877, 2),
			(1003, 2),
			(1243, 2),
			(1261, 2),
			(1281, 2),
			(1662, 2)
		],
		"format": FormatType.FT_STANDARD,
		"heroes": [31],  # Rexxar
		"deckstring": (
			"AAECAR8GxwPJBLsFmQfZB/gIDI0B2AGoArUDhwSSBe0G6wfbCe0JgQr+DAAA"
		),
	}
]


def _decksorted(cards):
	return sorted(cards, key=lambda x: x[0])


def test_empty_deckstring():
	deck = deckstrings.Deck()
	deck.heroes = [0]
	assert deck.as_deckstring == "AAEAAQAAAAAA"


def test_decode_pre_sideboard_deckstring():
	deck = deckstrings.Deck.from_deckstring(TEST_DECKSTRING_PRE_SIDEBOARD)
	assert deck.get_dbf_id_list() == _decksorted(TEST_DECKSTRING_CARDLIST)
	assert deck.get_sideboard_dbf_id_list() == []
	assert deck.format == FormatType.FT_WILD
	assert deck.heroes == [31]  # Rexxar


def test_decode_deckstring():
	deck = deckstrings.Deck.from_deckstring(TEST_DECKSTRING)
	assert deck.get_dbf_id_list() == _decksorted(TEST_DECKSTRING_CARDLIST)
	assert deck.get_sideboard_dbf_id_list() == []
	assert deck.format == FormatType.FT_WILD
	assert deck.heroes == [31]  # Rexxar


def test_encode_deckstring():
	deck = deckstrings.Deck()
	deck.cards = _decksorted(TEST_DECKSTRING_CARDLIST)
	deck.sideboard = []
	deck.format = FormatType.FT_WILD
	deck.heroes = [31]
	assert deck.as_deckstring == TEST_DECKSTRING


def test_reencode_deckstring():
	deck = deckstrings.Deck.from_deckstring(TEST_DECKSTRING)
	assert deck.as_deckstring == TEST_DECKSTRING


def test_decode_sideboard_deckstring():
	deck = deckstrings.Deck.from_deckstring(TEST_SIDEBOARD_DECKSTRING)
	assert deck.get_dbf_id_list() == _decksorted(TEST_SIDEBOARD_DECKSTRING_CARDLIST)
	assert deck.sideboard == _decksorted(TEST_SIDEBOARD_DECKSTRING_SIDEBOARD)
	assert deck.format == FormatType.FT_WILD
	assert deck.heroes == [101648]  # Hedanis


def test_encode_sideboard_deckstring():
	deck = deckstrings.Deck()
	deck.cards = _decksorted(TEST_SIDEBOARD_DECKSTRING_CARDLIST)
	deck.sideboard = _decksorted(TEST_SIDEBOARD_DECKSTRING_SIDEBOARD)
	deck.format = FormatType.FT_WILD
	deck.heroes = [101648]
	assert deck.as_deckstring == TEST_SIDEBOARD_DECKSTRING


def test_reencode_sideboard_deckstring():
	deck = deckstrings.Deck.from_deckstring(TEST_SIDEBOARD_DECKSTRING)
	assert deck.as_deckstring == TEST_SIDEBOARD_DECKSTRING


def test_deckstrings_regression():
	for deckdata in DECKSTRING_TEST_DATA:
		sideboard = deckdata.get("sideboard", [])

		# Encode tests
		deck = deckstrings.Deck()
		deck.cards = deckdata["cards"]
		deck.sideboard = sideboard
		deck.heroes = deckdata["heroes"]
		deck.format = deckdata["format"]

		assert deck.as_deckstring == deckdata["deckstring"]

		# Decode tests
		deck = deckstrings.Deck.from_deckstring(deckdata["deckstring"])
		assert _decksorted(deck.cards) == _decksorted(deckdata["cards"])
		assert _decksorted(deck.sideboard) == _decksorted(sideboard)
		assert deck.heroes == deckdata["heroes"]
		assert deck.format == deckdata["format"]
