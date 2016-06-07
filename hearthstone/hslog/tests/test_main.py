import pytest
from io import StringIO
from hearthstone.enums import (
	CardType, GameTag, PlayState, PowerType, State, Step, Zone
)
from hearthstone.hslog import LogParser


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


def test_create_empty_game():
	parser = LogParser()
	parser.read(StringIO(EMPTY_GAME))

	# Test resulting game/entities
	assert len(parser.games) == 1
	game = parser.games[0]
	assert len(game.entities) == 3
	assert len(game.players) == 2
	assert game.entities[0] is game
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
	assert len(game.packets) == 1
	packet = game.packets[0]
	assert packet.type == PowerType.CREATE_GAME
	assert packet.entity is game

	# Player packet objects are not the same as players
	assert packet.players[0].entity is game.players[0]
	assert packet.players[0].playerid == game.players[0].player_id
	assert packet.players[1].entity is game.players[1]
	assert packet.players[1].playerid == game.players[1].player_id

	# All tags should be empty (we didn't pass any)
	assert not game.tags
	assert not game.players[0].tags
	assert not game.players[1].tags

	# Check some basic logic
	assert game.get_player(1) is game.players[0]
	assert game.get_player(2) is game.players[1]


def test_tag_value_parsing():
	parser = LogParser()

	tag, value = parser.parse_initial_tag("tag=ZONE value=PLAY")
	assert tag == GameTag.ZONE
	assert value == Zone.PLAY

	tag, value = parser.parse_initial_tag("tag=CARDTYPE value=PLAYER")
	assert tag == GameTag.CARDTYPE
	assert value == CardType.PLAYER

	tag, value = parser.parse_initial_tag("tag=1 value=2")
	assert tag == 1
	assert value == 2

	tag, value = parser.parse_initial_tag("tag=9999998 value=123")
	assert tag == 9999998
	assert value == 123


def test_game_initialization():
	parser = LogParser()
	parser.read(StringIO(INITIAL_GAME))
	parser.flush()

	assert len(parser.games) == 1
	game = parser.games[0]
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

	assert not game.guess_friendly_player()
