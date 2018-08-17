from hearthstone.entities import Card, Game, Player
from hearthstone.enums import GameTag


def test_player():
	game = Game(1)
	player = Player(2, 1, 0, 0, "Test Player")
	player.game = game

	assert player.starting_hero is None


def test_cards():
	card1 = Card(4, "EX1_001")
	# The following should be instant.
	# If this test hangs, something's wrong in the caching mechanism...
	for i in range(1000):
		assert card1.base_tags.get(GameTag.HEALTH, 0) == 2


def test_change_entity():
	card = Card(4, "EX1_001")
	assert card.card_id == "EX1_001"
	assert card.initial_card_id == "EX1_001"
	assert card.is_original_entity

	card.change("NEW1_030", {})
	assert card.card_id == "NEW1_030"
	assert card.initial_card_id == "EX1_001"
	assert not card.is_original_entity

	weapon = Card(4, None)
	assert not weapon.initial_card_id
	assert weapon.is_original_entity

	weapon.reveal("CS2_091", {GameTag.TRANSFORMED_FROM_CARD: 41420})
	assert weapon.card_id == "CS2_091"
	assert weapon.initial_card_id == "UNG_929"
	assert not weapon.is_original_entity


def test_entities():
	game = Game(1)
	game.register_entity(game)

	assert game.find_entity_by_id(1) is game
	assert game.find_entity_by_id(2) is None
