import pytest
from io import StringIO
from hearthstone.enums import PowerType
from hearthstone.hslog import LogParser


EMPTY_GAME = """
D 02:59:14.6088620 GameState.DebugPrintPower() - CREATE_GAME
D 02:59:14.6149420 GameState.DebugPrintPower() -     GameEntity EntityID=1
D 02:59:14.6446530 GameState.DebugPrintPower() -     Player EntityID=2 PlayerID=1 GameAccountId=[hi=1 lo=0]
D 02:59:14.6481950 GameState.DebugPrintPower() -     Player EntityID=3 PlayerID=2 GameAccountId=[hi=3 lo=2]
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
