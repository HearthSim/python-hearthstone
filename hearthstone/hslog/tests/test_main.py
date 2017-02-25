from __future__ import unicode_literals
import pytest
from datetime import datetime, time, timedelta
from io import StringIO
from aniso8601 import parse_datetime
from hearthstone.enums import (
	CardType, ChoiceType, GameTag, PlayState, PowerType, State, Step, Zone
)
from hearthstone.hslog import LogParser
from hearthstone.hslog.exceptions import ParsingError
from hearthstone.hslog.export import FriendlyPlayerExporter
from hearthstone.hslog.parser import parse_initial_tag, parse_entity_id


EMPTY_GAME = """
D 02:59:14.6088620 GameState.DebugPrintPower() - CREATE_GAME
D 02:59:14.6149420 GameState.DebugPrintPower() -     GameEntity EntityID=1
D 02:59:14.6446530 GameState.DebugPrintPower() -     Player EntityID=2 PlayerID=1 GameAccountId=[hi=1 lo=0]
D 02:59:14.6481950 GameState.DebugPrintPower() -     Player EntityID=3 PlayerID=2 GameAccountId=[hi=3 lo=2]
""".strip()

INITIAL_GAME = """
D 02:59:14.6088620 GameState.DebugPrintPower() - CREATE_GAME
D 02:59:14.6149420 GameState.DebugPrintPower() -     GameEntity EntityID=1
D 02:59:14.6420450 GameState.DebugPrintPower() -         tag=TURN value=1
D 02:59:14.6428100 GameState.DebugPrintPower() -         tag=ZONE value=PLAY
D 02:59:14.6430430 GameState.DebugPrintPower() -         tag=ENTITY_ID value=1
D 02:59:14.6436240 GameState.DebugPrintPower() -         tag=NEXT_STEP value=BEGIN_MULLIGAN
D 02:59:14.6438920 GameState.DebugPrintPower() -         tag=CARDTYPE value=GAME
D 02:59:14.6442880 GameState.DebugPrintPower() -         tag=STATE value=RUNNING
D 02:59:14.6446530 GameState.DebugPrintPower() -     Player EntityID=2 PlayerID=1 GameAccountId=[hi=1 lo=0]
D 02:59:14.6450220 GameState.DebugPrintPower() -         tag=PLAYSTATE value=PLAYING
D 02:59:14.6463220 GameState.DebugPrintPower() -         tag=PLAYER_ID value=1
D 02:59:14.6466060 GameState.DebugPrintPower() -         tag=TEAM_ID value=1
D 02:59:14.6469080 GameState.DebugPrintPower() -         tag=ZONE value=PLAY
D 02:59:14.6470710 GameState.DebugPrintPower() -         tag=CONTROLLER value=1
D 02:59:14.6472580 GameState.DebugPrintPower() -         tag=ENTITY_ID value=2
D 02:59:14.6476340 GameState.DebugPrintPower() -         tag=CARDTYPE value=PLAYER
D 02:59:14.6481950 GameState.DebugPrintPower() -     Player EntityID=3 PlayerID=2 GameAccountId=[hi=3 lo=2]
D 02:59:14.6483770 GameState.DebugPrintPower() -         tag=PLAYSTATE value=PLAYING
D 02:59:14.6485530 GameState.DebugPrintPower() -         tag=CURRENT_PLAYER value=1
D 02:59:14.6486970 GameState.DebugPrintPower() -         tag=FIRST_PLAYER value=1
D 02:59:14.6492590 GameState.DebugPrintPower() -         tag=PLAYER_ID value=2
D 02:59:14.6493880 GameState.DebugPrintPower() -         tag=TEAM_ID value=2
D 02:59:14.6495200 GameState.DebugPrintPower() -         tag=ZONE value=PLAY
D 02:59:14.6496470 GameState.DebugPrintPower() -         tag=CONTROLLER value=2
D 02:59:14.6497780 GameState.DebugPrintPower() -         tag=ENTITY_ID value=3
D 02:59:14.6500380 GameState.DebugPrintPower() -         tag=CARDTYPE value=PLAYER
""".strip()

FULL_ENTITY = """D 22:25:48.0678873 GameState.DebugPrintPower() - FULL_ENTITY - Creating ID=4 CardID=
D 22:25:48.0678873 GameState.DebugPrintPower() -     tag=ZONE value=DECK
D 22:25:48.0678873 GameState.DebugPrintPower() -     tag=CONTROLLER value=1
D 22:25:48.0678873 GameState.DebugPrintPower() -     tag=ENTITY_ID value=4
""".strip()

INVALID_GAME = """
D 02:59:14.6088620 GameState.DebugPrintPower() - CREATE_GAME
D 02:59:14.6149420 GameState.DebugPrintPower() -     GameEntity EntityID=1
D 02:59:14.6428100 GameState.DebugPrintPower() -         tag=ZONE value=PLAY
D 02:59:14.6481950 GameState.DebugPrintPower() -     Player EntityID=3 PlayerID=2 GameAccountId=[hi=3 lo=2]
D 02:59:14.6483770 GameState.DebugPrintPower() -         tag=PLAYSTATE value=PLAYING
D 02:59:14.6492590 GameState.DebugPrintPower() -         tag=PLAYER_ID value=2
""".strip() + "\n" + FULL_ENTITY

CONTROLLER_CHANGE = """
D 22:25:48.0708939 GameState.DebugPrintPower() - TAG_CHANGE Entity=4 tag=CONTROLLER value=2
""".strip()


def test_create_empty_game():
	parser = LogParser()
	parser.read(StringIO(EMPTY_GAME))
	parser.flush()

	# Test resulting game/entities
	assert len(parser.games) == 1

	packet_tree = parser.games[0]
	game = packet_tree.export().game
	assert len(game.entities) == 3
	assert len(game.players) == 2
	assert game.entities[0] is game
	assert game.entities[0].id == 1
	assert game.entities[1] is game.players[0]
	assert game.entities[2] is game.players[1]

	# Test player objects
	assert game.players[0].id == 2
	assert game.players[0].player_id == 1
	assert game.players[0].account_hi == 1
	assert game.players[0].account_lo == 0
	assert game.players[0].is_ai
	assert not game.players[0].name

	assert game.players[1].id == 3
	assert game.players[1].player_id == 2
	assert game.players[1].account_hi == 3
	assert game.players[1].account_lo == 2
	assert not game.players[1].is_ai
	assert not game.players[1].name

	# Test packet structure
	assert len(packet_tree.packets) == 1
	packet = packet_tree.packets[0]
	assert packet.power_type == PowerType.CREATE_GAME
	assert packet.entity == game.id == 1

	# Player packet objects are not the same as players
	assert int(packet.players[0].entity) == game.players[0].id
	assert packet.players[0].player_id == game.players[0].player_id
	assert int(packet.players[1].entity) == game.players[1].id
	assert packet.players[1].player_id == game.players[1].player_id

	# All tags should be empty (we didn't pass any)
	assert not game.tags
	assert not game.players[0].tags
	assert not game.players[1].tags

	# Check some basic logic
	assert game.get_player(1) is game.players[0]
	assert game.get_player(2) is game.players[1]


def test_tag_value_parsing():
	tag, value = parse_initial_tag("tag=ZONE value=PLAY")
	assert tag == GameTag.ZONE
	assert value == Zone.PLAY

	tag, value = parse_initial_tag("tag=CARDTYPE value=PLAYER")
	assert tag == GameTag.CARDTYPE
	assert value == CardType.PLAYER

	tag, value = parse_initial_tag("tag=1 value=2")
	assert tag == 1
	assert value == 2

	tag, value = parse_initial_tag("tag=9999998 value=123")
	assert tag == 9999998
	assert value == 123


def test_game_initialization():
	parser = LogParser()
	parser.read(StringIO(INITIAL_GAME))
	parser.flush()

	assert len(parser.games) == 1
	packet_tree = parser.games[0]
	game = packet_tree.export().game
	assert len(game.entities) == 3
	assert len(game.players) == 2

	assert game.tags == {
		GameTag.TURN: 1,
		GameTag.ZONE: Zone.PLAY,
		GameTag.ENTITY_ID: 1,
		GameTag.NEXT_STEP: Step.BEGIN_MULLIGAN,
		GameTag.CARDTYPE: CardType.GAME,
		GameTag.STATE: State.RUNNING,
	}

	assert game.players[0].tags == {
		GameTag.PLAYSTATE: PlayState.PLAYING,
		GameTag.PLAYER_ID: 1,
		GameTag.TEAM_ID: 1,
		GameTag.ZONE: Zone.PLAY,
		GameTag.CONTROLLER: 1,
		GameTag.ENTITY_ID: 2,
		GameTag.CARDTYPE: CardType.PLAYER,
	}

	assert game.players[1].tags == {
		GameTag.PLAYSTATE: PlayState.PLAYING,
		GameTag.CURRENT_PLAYER: 1,
		GameTag.FIRST_PLAYER: 1,
		GameTag.PLAYER_ID: 2,
		GameTag.TEAM_ID: 2,
		GameTag.ZONE: Zone.PLAY,
		GameTag.CONTROLLER: 2,
		GameTag.ENTITY_ID: 3,
		GameTag.CARDTYPE: CardType.PLAYER,
	}

	# Test that there should be no friendly player
	fpe = FriendlyPlayerExporter(packet_tree)
	friendly_player = fpe.export()
	assert not friendly_player


def test_timestamp_parsing():
	parser = LogParser()
	parser.read(StringIO(INITIAL_GAME))
	parser.flush()

	assert parser.games[0].packets[0].ts == time(2, 59, 14, 608862)

	# Test with an initial datetime
	parser2 = LogParser()
	parser2._current_date = datetime(2015, 1, 1)
	parser2.read(StringIO(INITIAL_GAME))
	parser2.flush()

	assert parser2.games[0].packets[0].ts == datetime(2015, 1, 1, 2, 59, 14, 608862)

	# Same test, with timezone
	parser2 = LogParser()
	parser2._current_date = parse_datetime("2015-01-01T02:58:00+0200")
	parser2.read(StringIO(INITIAL_GAME))
	parser2.flush()

	ts = parser2.games[0].packets[0].ts
	assert ts.year == 2015
	assert ts.hour == 2
	assert ts.second == 14
	assert ts.tzinfo
	assert ts.utcoffset() == timedelta(hours=2)


def test_info_outside_of_metadata():
	parser = LogParser()
	parser.read(StringIO(INITIAL_GAME))
	parser.flush()

	info = "D 02:59:14.6500380 GameState.DebugPrintPower() -             Info[0] = 99"
	parser.read(StringIO(info))
	parser.flush()


def test_empty_entity_in_options():
	parser = LogParser()
	parser.read(StringIO(INITIAL_GAME))
	parser.flush()

	data = "target 0 entity="
	with pytest.raises(ParsingError):
		# This can happen, but the game is corrupt
		parser.handle_options(None, data)


def test_warn_level():
	parser = LogParser()
	parser.read(StringIO(INITIAL_GAME))
	parser.flush()

	line = "W 09:09:23.1428700 GameState.ReportStuck() - Stuck for 10s 89ms. {...}"
	parser.read(StringIO(line))
	parser.flush()


def test_empty_tasklist():
	parser = LogParser()
	parser.read(StringIO(INITIAL_GAME))
	parser.flush()

	ts = datetime.now()
	msg = "id=4 Player=The Innkeeper TaskList=1 ChoiceType=GENERAL CountMin=1 CountMax=1"
	choices = parser.handle_entity_choices(ts, msg)
	assert choices
	assert choices.id == 4
	assert choices.player.name == "The Innkeeper"
	assert choices.tasklist == 1
	assert choices.type == ChoiceType.GENERAL
	assert choices.min == 1
	assert choices.max == 1

	# Test empty tasklist
	msg = "id=4 Player=The Innkeeper TaskList= ChoiceType=GENERAL CountMin=1 CountMax=1"
	choices = parser.handle_entity_choices(ts, msg)
	assert choices.tasklist is None


def test_tag_change_unknown_entity_format():
	# Format changed in 15590
	parser = LogParser()
	parser.read(StringIO(INITIAL_GAME))
	parser.flush()

	entity_format = "[name=UNKNOWN ENTITY [cardType=INVALID] id=24 zone=DECK zonePos=0 cardId= player=1]"
	id = parse_entity_id(entity_format)
	assert id == 24

	data = "TAG_CHANGE Entity=%s tag=ZONE value=HAND" % (entity_format)
	packet = parser.handle_power(None, "TAG_CHANGE", data)
	assert packet.power_type == PowerType.TAG_CHANGE
	assert packet.entity == id
	assert packet.tag == GameTag.ZONE
	assert packet.value == Zone.HAND


def test_initial_deck_initial_controller():
	parser = LogParser()
	parser.read(StringIO(INITIAL_GAME))
	parser.read(StringIO(FULL_ENTITY))
	parser.flush()
	packet_tree = parser.games[0]
	game = packet_tree.export().game

	assert len(list(game.players[0].initial_deck)) == 1
	assert len(list(game.players[1].initial_deck)) == 0

	parser = LogParser()
	parser.read(StringIO(INITIAL_GAME))
	parser.read(StringIO(FULL_ENTITY))
	parser.read(StringIO(CONTROLLER_CHANGE))
	parser.flush()
	packet_tree = parser.games[0]
	game = packet_tree.export().game

	assert len(list(game.players[0].initial_deck)) == 1
	assert len(list(game.players[1].initial_deck)) == 0


def test_invalid_game_one_player():
	parser = LogParser()
	with pytest.raises(ParsingError):
		parser.read(StringIO(INVALID_GAME))
