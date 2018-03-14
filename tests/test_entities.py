from hearthstone.entities import Game, Player


def test_player():
	game = Game(1)
	player = Player(2, 1, 0, 0, "Test Player")
	player.game = game

	assert player.starting_hero is None
